
from gvsig import *
from gvsig.commonsdialog import *
import os
import subprocess

from org.gvsig.andami import PluginsLocator 

def getPluginFolder(): 
  pluginsManager = PluginsLocator.getManager() 
  plugin = pluginsManager.getPlugin("org.gvsig.r.app.mainplugin") 
  f = plugin.getPluginDirectory()
  return f.getAbsolutePath()
  
def isexe(fpath):
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        
def RShellWindows():
  RExe = os.path.abspath(os.path.join(getPluginFolder(),"R","bin","x64","R.exe"))
  subprocess.Popen(["start", "cmd", "/K", RExe,"--ess", "--no-restore", "--no-save"],shell=True)

def RShellLinux():
  RExe = os.path.abspath(os.path.join(getPluginFolder(),"R","bin","R"))
  if isexe("/usr/bin/konsole"):
    cmd = '/usr/bin/konsole -e "%s" --interactive --no-restore --no-save &' % RExe
  else:
    cmd='xterm -sb -rightbar -sl 1000 -fg gray -bg black -e "%s" --interactive --no-restore --no-save &' % RExe
  os.system(cmd)
  
def rshell():
  from org.gvsig.tools import ToolsLocator
  pkgmanager = ToolsLocator.getPackageManager()
  operatingSystem = pkgmanager.getOperatingSystemFamily()
  #architecture = pkgmanager.getArchitecture()

  if operatingSystem == "win":
    RShellWindows()
  
  elif operatingSystem == "lin":
    RShellLinux()

  else:
    msgbox("Can't launch R console, don't identify the OS (%s)." % operatingSystem)
    
def main(*args):
    rshell()
    

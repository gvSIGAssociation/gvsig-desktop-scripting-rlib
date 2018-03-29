
import StringIO
import time
import os, os.path
import sys
import subprocess
from org.gvsig.tools import ToolsLocator
#from org.gvsig.andami import Utilities

import rlib_base
 
class REngine_SimplePopen(rlib_base.REngine_base):

  def __init__(self, consoleListener=None):
    rlib_base.REngine_base.__init__(self,consoleListener)

    self.__dict__["_child"] = None
    self.__dict__["_script"] = None

    self.run()

  def run(self):
    self._script = StringIO.StringIO()
    return True

  def eval(self,expr):
    self._script.write(expr)
    self._script.write("\n")
    return None

  def get(self, name):
    return None

  def set(self, name, value):
    if isinstance(value,str) or isinstance(value,unicode) :
      value = '"' + repr(value)[1:-1] + '"'
    else:
      value = str(value)
    self.eval("%s <- %s" % (name,value))

  def setwd(self,path):
    self.eval('setwd("%s")' % self.getPathName(path))
    
  def source(self, pathname):
    return self.eval('source("%s")' % self.getPathName(pathname))

  def call(self, funcname, *args):
    cmd = StringIO.StringIO()
    cmd.write(funcname)
    cmd.write("(")
    n = 0
    for arg in args:
      if n>0 and n<len(args):
        cmd.write(", ")
      if isinstance(arg,str) :
        arg = '"' + repr(arg)[1:-1] + '"'
      elif isinstance(arg,unicode) :
        arg = '"' + repr(arg)[2:-1] + '"'
      else:
        arg = str(arg)
      cmd.write(arg)
      n+=1
    cmd.write(")")
    cmd = cmd.getvalue()
    return self.eval(cmd)

  def abort(self):
    rlib_base.REngine_base.abort(self)
    self._script = None
    
    
  def end(self):
    if self._script == None:
      return
    folderManager = ToolsLocator.getFoldersManager()
    folderManager.createTemporaryFolder()
    t = time.time()
    script = self._script.getvalue()
    scriptFileName = folderManager.createTemporaryFile("rtest-%08x.r" % t, script)
    self._child = subprocess.Popen([self.getRExecPathname(),"-f",scriptFileName.getAbsolutePath()],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in self._child.stdout:
        self.console_output(i)
    self._child = None
    rlib_base.REngine_base.end(self)
  
def getREngine(consoleListener=None):
    return REngine_SimplePopen(consoleListener)


  
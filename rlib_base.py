
from gvsig import *

from org.apache.commons.io import FilenameUtils
from org.gvsig.andami import Utilities

class REngine_base(object):
  def __init__(self, consoleListener=None):
    self.__dict__["_consoleListeners"] = None
    self.__dict__["_architecture"] = None
    self.__dict__["_operatingSystem"] = None
    
    self._consoleListeners = list()
    self.addConsoleListener(consoleListener)

  def source(self,pathname):
    return None

  def eval(self,expresion):
    return None

  def end(self):
    self._consoleListeners = list()

  def abort(self):
    pass
    
  def get(self, name):
    pass

  def set(self,name,value):
    pass

  def call(self, funcname, *args):
    pass
    
  def run(self):
    return True

  def getTemp(self,basename=None):
    if basename == None:
      return Utilities.TEMPDIRECTORYPATH
    return Utilities.TEMPDIRECTORYPATH + "/" + basename
    
  def addConsoleListener(self, function):
    if function == None:
      return
    self._consoleListeners.append(function)

  def console_output(self, text, otype=0):
    for listener in self._consoleListeners:
      try:
        listener(text,otype)
      except Exception as ex:
        print "Error calling console listener %s. %s" % (repr(listener), str(ex))

  def getArchitecture(self):
    if self._architecture == None:
      from org.gvsig.tools import ToolsLocator

      pkgmanager = ToolsLocator.getPackageManager()
      self._operatingSystem = pkgmanager.getOperatingSystemFamily()
      self._architecture = pkgmanager.getArchitecture()
    return self._architecture
    
  def getOperatingSystem(self):
    if self._operatingSystem == None:
      from org.gvsig.tools import ToolsLocator

      pkgmanager = ToolsLocator.getPackageManager()
      self._operatingSystem = pkgmanager.getOperatingSystemFamily()
      self._architecture = pkgmanager.getArchitecture()
    return self._operatingSystem
    
  def getRExecPathname(self):
    from java.io import File
    from org.gvsig.andami import PluginsLocator
    
    if self.getArchitecture() != "x86_64":  
      raise Exception("Architecture not supported.")
      
    plugin = PluginsLocator.getManager().getPlugin("org.gvsig.r.app.mainplugin")
    pluginFolder = plugin.getPluginDirectory()
    
    if self.getOperatingSystem() == "win":  
      f = File(pluginFolder,"R/bin/x64/R.exe")
      return f.getAbsolutePath().replace("\\","/")
  
    if self.getOperatingSystem() == "lin":  
      f = File(pluginFolder,"R/bin/R")
      return f.getAbsolutePath()
  
    raise Exception("Operating system not supported.")


  def isLayerSupported(self,layer):
    return self.getPathName(layer)!=None

  def getLayerDSN(self,pathname):
    pathname = self.getPathName(pathname)
    return FilenameUtils.getFullPath(pathname)

  def getLayerName(self,pathname):
    pathname = self.getPathName(pathname)
    return FilenameUtils.getBaseName(pathname)

  def getPathName(self,pathname):
    getDataStore = getattr(pathname,"getDataStore", None)
    if getDataStore == None:
      getAbsolutePath = getattr(pathname,"getAbsolutePath",None)
      if getAbsolutePath!=None:
        pathname = getAbsolutePath()
    else:
      store = getDataStore()
      getParameters = getattr(store,"getParameters",None)
      if getParameters == None:
        return None
      parameters = getParameters()
      getFile = getattr(parameters,"getFile",None)
      if getFile == None:
        return None
      pathname = getFile()
      if pathname == None:
        return None
      pathname = pathname.getAbsolutePath()

    if isinstance(pathname,str) or isinstance(pathname,unicode):
      return pathname.replace("\\","/")
    return None




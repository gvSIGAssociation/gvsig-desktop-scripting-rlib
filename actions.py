# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import load_icon
from gvsig import getResource
from org.gvsig.tools import ToolsLocator
from javax.swing import AbstractAction, Action
from org.gvsig.scripting.swing.api import ScriptingSwingLocator
from RShell import rshell

class RConsoleAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"R Console")
    self.putValue(Action.ACTION_COMMAND_KEY, "RConsole")
    self.putValue(Action.SMALL_ICON, load_icon(getResource(__file__,"images","rconsole.png")))
    self.putValue(Action.SHORT_DESCRIPTION, "Show R Console")

  def actionPerformed(self,e):
    rshell()

def selfRegister():
  i18nManager = ToolsLocator.getI18nManager()
  manager = ScriptingSwingLocator.getUIManager()
  action = RConsoleAction()
  manager.addComposerTool(action)
  manager.addComposerMenu(i18nManager.getTranslation("Tools"),action)
  
def main(*args):

    selfRegister()

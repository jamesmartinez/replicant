import command

import cmdconfig
import cmdgrep
import cmdirc
import cmdping
import cmdquery
import cmdresults

modules = [
    cmdconfig,
    cmdgrep,
    cmdirc,
    cmdping,
    cmdquery,
    cmdresults,
]

def register_commands():
  for module in modules:
    module.register_commands()

def reload_commands():
  for module in modules:
    reload(module)
  register_commands()

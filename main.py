from twisted.enterprise import adbapi 
from twisted.internet import reactor

import os

import command
import config
import factory
import proto
import request
import userdb

def to_utf8(s):
  if isinstance(s, unicode):
    return s.encode('utf-8')
  return s

if __name__ == '__main__':
  conf = config.Configuration('bot.conf')
  conf.load()
  databases = {}
  servers = {}
  lines = config.load_history()

  for db_name, db_config in conf['databases'].iteritems():
    databases[db_name] = adbapi.ConnectionPool(*db_config)

  for server, server_config in conf['servers'].iteritems():
    servers[server] = f = factory.BotFactory()
    f.db = databases[server_config['database']]

    f.channels = [to_utf8(c) for c in server_config['channels']]
    f.irc_host = to_utf8(server_config['host'])
    f.irc_port = to_utf8(server_config['port'])
    f.nickname = to_utf8(server_config['nickname'])
    f.realname = to_utf8(server_config['realname'])
    f.password = to_utf8(server_config['password'])
    f.username = to_utf8(server_config['username'])
    f.prefix = to_utf8(server_config['command_prefix'])

    f.conf = conf
    f.lines = lines
    f.users = userdb.UserDB(f.db)
    f.request_factory = request.Request
    f.protocol = proto.BotProtocol
    f.handler = command.CommandHandler(f.db, f.users, lines, conf)
    reactor.connectTCP(f.irc_host, f.irc_port, f)

  reactor.run()

  config.save_history(lines)

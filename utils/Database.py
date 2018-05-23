import aiohttp
import asyncio
import MySQLdb

class Database:
  db = MySQLdb.connect(host='localhost', user='root', passwd='jinsooftw', db='matchBot')
  cur = db.cursor()

  async def get(self, command, nick):
    log = command % nick
    print('get: %s' % log)

    #  BROKEN. (nick), (nick,), nor [nick] will work :( :( :(
    body = self.cur.execute(command, (nick, ))
    self.db.commit()

    return body

  async def execute(self, command, seq):
    log = command % seq
    print('execute: %s' % log)

    self.cur.execute(command, (seq, ))
    self.db.commit()

  def __del__(self):
    self.db.close()


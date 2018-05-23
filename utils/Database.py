import aiohttp
import asyncio
import MySQLdb
from config import DB_HOST, DB_USER, DB_PW, DB_NAME

class Database:
  db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PW, db=DB_NAME)
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

    # This is starting to break as well :eyes:
    self.cur.execute(command, (seq, ))
    self.db.commit()

  def __del__(self):
    self.db.close()


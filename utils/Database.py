import aiohttp
import asyncio
import MySQLdb
from config import DB_HOST, DB_USER, DB_PW, DB_NAME

class Database:
  db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PW, db=DB_NAME)
  cur = db.cursor()

  async def contains(self, command, seq):
    log = command % seq
    print('contains: %s' % log)

    #  BROKEN. (nick), (nick,), nor [nick] will work :( :( :(
    amount = self.cur.execute(log)
    self.db.commit()

    return amount

  async def execute(self, command, seq):
    log = command % seq
    print('execute: %s' % log)

    # This is starting to break as well :eyes:
    self.cur.execute(log)
    self.db.commit()

  def __del__(self):
    self.db.close()

  async def get(self, command):
    print('get: %s' % command)

    self.cur.execute(command)
    self.db.commit()

    return self.cur.fetchall()
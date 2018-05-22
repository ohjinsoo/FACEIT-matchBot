import aiohttp
import asyncio
import MySQLdb

class Database:
  db = MySQLdb.connect(host='localhost', user='root', passwd='jinsooftw', db='matchBot')
  cur = db.cursor()

  async def get(self, command, seq):
    log = command % seq
    print('get: %s' % log)
    body = self.cur.execute(command, seq)
    db.commit()
    return body

  async def execute(self, command, seq):
    log = command % seq
    print('execute: %s' % log)
    self.cur.execute(command, seq)
    self.db.commit()

  def __del__(self):
    self.db.close()


import aiohttp
import asyncio
import MySQLdb

class Database:
  db = MySQLdb.connect(host='localhost', user='root', passwd='jinsooftw', db='matchBot')
  cur = db.cursor()

  async def get(self, command):
    print('get: %s' % command)
    body = self.cur.execute(command)
    db.commit()
    return body


# bug where its telling me db doesnt exist when i try db.commit()   :( :( :(
  async def execute(self, command):
    print('execute: %s' % command)
    self.cur.execute(command)
    db.commit()



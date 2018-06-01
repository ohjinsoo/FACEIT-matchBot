import aiohttp
import asyncio
import MySQLdb
from config import DB_HOST, DB_USER, DB_PW, DB_NAME

class Database:
  db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PW, db=DB_NAME)
  cur = db.cursor()

  def __del__(self):
    currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
    print(currentTime + "::: Closing MySQL connection...")

    self.cur.close()
    self.db.close()

  def query(self, sql, var):
    run = self.cur.execute(sql, var)
    self.db.commit()

    return run

  def contains(self, command, seq):
    log = command % seq
    currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
    print(currentTime + '::: contains: ' + log)

    return self.query(command, seq)

  def execute(self, command, seq):
    log = command % seq
    currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
    print(currentTime + '::: execute: ' + log)

    self.query(command, seq)

  def get(self, command, seq):
    log = command % seq
    currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
    print(currentTime + '::: get: ' + log)
    
    self.query(command, seq)
    return [
      dict(
        zip([column[0] for column in self.cur.description], row)
      ) for row in self.cur.fetchall()
    ]

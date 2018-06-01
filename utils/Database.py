import aiohttp
import asyncio
import MySQLdb
from utils.Logger import log

from config import DB_HOST, DB_USER, DB_PW, DB_NAME

class Database:
  db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PW, db=DB_NAME)
  cur = db.cursor()

  def __del__(self):
    log("::: Closing MySQL connection...")

    self.cur.close()
    self.db.close()

  def query(self, sql, var):
    run = self.cur.execute(sql, var)
    self.db.commit()

    return run

  def contains(self, command, seq):
    logString = command % seq
    log('contains: ' + logString)

    return self.query(command, seq)

  def execute(self, command, seq):
    logString = command % seq
    log('execute: ' + logString)

    self.query(command, seq)

  def get(self, command, seq):
    logString = command % seq
    log('get: ' + logString)

    self.query(command, seq)
    return [
      dict(
        zip([column[0] for column in self.cur.description], row)
      ) for row in self.cur.fetchall()
    ]

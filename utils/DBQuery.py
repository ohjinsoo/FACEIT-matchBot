import asyncio
from utils.Database import Database

db = Database()

class DBQuery:
  @staticmethod
  def getPlayer(faceit_id):
    seq = { 
        'faceit_id' : faceit_id 
    }
    cmd = """
      SELECT * FROM players WHERE faceit_id = %(faceit_id)s;
    """

    return db.contains(cmd, seq)

  @staticmethod
  def insertOrUpdate(faceit_id, nickname):
    seq = {
        'faceit_id': faceit_id,
        'nickname': nickname,
    }
    cmd = """
      INSERT INTO players
        (faceit_id, nickname)  VALUES (%(faceit_id)s, %(nickname)s)
      ON DUPLICATE KEY UPDATE
        nickname = %(nickname)s
    """
    db.execute(cmd, seq)

  @staticmethod
  def insertPlayer(faceit_id, nickname, kills, deaths, wins, matches):
    seq = {
      'faceit_id': faceit_id,
      'nickname': nickname,
      'kills': kills,
      'deaths': deaths,
      'wins': wins,
      'matches': matches
    }
    cmd = """
    INSERT INTO players
      (`faceit_id`, `nickname`, `kills`, `deaths`, `wins`, `matches`)
      VALUES
      (%(faceit_id)s, %(nickname)s, %(kills)s, %(deaths)s, %(wins)s, %(matches)s);
    """
    db.execute(cmd, seq)

  @staticmethod
  def addToPlayer(faceit_id, kills, deaths, wins, matches):
    seq = {
      'faceit_id': faceit_id,
      'kills': kills,
      'deaths': deaths,
      'wins': wins,
      'matches': matches
    }
    cmd = """
      UPDATE players
        SET kills = kills + %(kills)s,
          deaths = deaths + %(deaths)s,
          wins = wins + %(wins)s,
          matches = matches + %(matches)s
        WHERE faceit_id = %(faceit_id)s;
    """
    db.execute(cmd, seq)

  @staticmethod
  def removePlayer(faceit_id):
    seq = {'faceit_id': faceit_id}
    cmd = "DELETE FROM players WHERE faceit_id = %(faceit_id)s;"
    db.execute(cmd, seq)

  @staticmethod
  def getRanking(column = 'kills', order = 'DESC'):
    seq = {}
    cmd = """
      SELECT
        nickname, kills, deaths, wins, matches
      FROM players
      ORDER BY %(column)s %(order)s;
    """ % {'column': column, 'order': order}
    return db.get(cmd, seq)

DROP TABLE IF EXISTS players;

CREATE TABLE players (
faceit_id varchar(40) NOT NULL,
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
nickname VARCHAR(20) NOT NULL,
kills INT UNSIGNED NOT NULL,
deaths INT UNSIGNED NOT NULL,
wins INT UNSIGNED NOT NULL,
matches INT UNSIGNED NOT NULL
);

UPDATE players SET kills  = kills + %s, deaths = deaths + %s, wins = wins + %s, matches = matches + %s WHERE faceit_id = '%s';
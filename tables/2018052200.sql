CREATE TABLE players (
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
nickname VARCHAR(20) NOT NULL,
kills INT UNSIGNED NOT NULL,
deaths INT UNSIGNED NOT NULL,
wins INT UNSIGNED NOT NULL,
matches INT UNSIGNED NOT NULL
);

UPDATE table1 SET col_a='k1', col_b='foo' WHERE key_col='1';

TRUNCATE TABLE players; # this deletes all table data, for jinsoo
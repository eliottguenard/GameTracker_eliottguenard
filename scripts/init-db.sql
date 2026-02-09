-- Initialisation de la base de données GameTracker
CREATE DATABASE IF NOT EXISTS gametracker;
USE gametracker;

-- Accorder tous les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON gametracker.* TO 'gameuser'@'%';
FLUSH PRIVILEGES;

-- Table des joueurs
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    registration_date DATE,
    country VARCHAR(100),
    level INT
);

-- Table des scores (clé étrangère vers players)
CREATE TABLE IF NOT EXISTS scores (
    score_id VARCHAR(20) PRIMARY KEY,
    player_id INT,
    game VARCHAR(100),
    score INT,
    duration_minutes INT,
    played_at DATETIME,
    platform VARCHAR(50),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

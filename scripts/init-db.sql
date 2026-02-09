-- Initialisation de la base de données GameTracker
CREATE DATABASE IF NOT EXISTS gametracker;
USE gametracker;

-- Accorder tous les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON gametracker.* TO 'gameuser'@'%';
FLUSH PRIVILEGES;

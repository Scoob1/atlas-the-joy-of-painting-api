CREATE DATABASE joy_of_painting;
USE joy_of_painting;

CREATE TABLE seasons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    season_number INT NOT NULL
);

CREATE TABLE episodes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    season_id INT,
    episode_number INT NOT NULL,
    title VARCHAR(255),
    painting_name VARCHAR(255),
    FOREIGN KEY (season_id) REFERENCES seasons(id)
);


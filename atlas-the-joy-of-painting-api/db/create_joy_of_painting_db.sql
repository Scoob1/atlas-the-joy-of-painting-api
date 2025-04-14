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
    broadcast_date DATE,
    FOREIGN KEY (season_id) REFERENCES seasons(id)
);

CREATE TABLE colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE episode_colors (
    episode_id INT,
    color_id INT,
    PRIMARY KEY (episode_id, color_id),
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES colors(id) ON DELETE CASCADE
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE episode_subjects (
    episode_id INT,
    subject_id INT,
    PRIMARY KEY (episode_id, subject_id),
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

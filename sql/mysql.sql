DROP DATABASE IF EXISTS gymfitness;

CREATE DATABASE gymfitness;
USE gymfitness;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    birth VARCHAR(50) NOT NULL,
    height DOUBLE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE evaluations (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    uid INT NOT NULL,
    date DATE NOT NULL,
    weight DOUBLE NOT NULL,
    height DOUBLE NOT NULL,
    imc DOUBLE NOT NULL,

    FOREIGN KEY (uid) REFERENCES users (id)
);
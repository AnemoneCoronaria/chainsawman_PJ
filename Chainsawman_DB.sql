create database chainsawman;
use chainsawman;

CREATE TABLE Team (
    team_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL
);


CREATE TABLE Human (
    human_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    status ENUM('ACTIVE','INACTIVE','RETIRED','DEAD') DEFAULT 'ACTIVE',
    team_id BIGINT NULL,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE Demon (
    demon_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    grade ENUM('C','B','A','S','SS') NOT NULL,
    bounty INT NOT NULL,
    civilian_killed_total INT DEFAULT 0,
    civilian_injured_total INT DEFAULT 0
);

CREATE TABLE Contract (
    contract_id INT PRIMARY KEY AUTO_INCREMENT,
    human_id INT NOT NULL,
    demon_id INT NOT NULL,
    cost_type ENUM('LIFE','MEMORY','EMOTION','OTHER') NOT NULL,
    cost_desc VARCHAR(255) NOT NULL,
    status ENUM('ACTIVE','BROKEN','EXPIRED') DEFAULT 'ACTIVE',
    FOREIGN KEY (human_id) REFERENCES Human(human_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (demon_id) REFERENCES Demon(demon_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Mission (
    mission_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    team_id BIGINT NOT NULL,
    objective VARCHAR(255) NOT NULL,
    target_desc VARCHAR(255) NOT NULL,
    status ENUM('PLANNED','IN_PROGRESS','SUCCESS','FAIL') DEFAULT 'PLANNED',
    created_at DATE NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE Battle (
    battle_id INT PRIMARY KEY AUTO_INCREMENT,
    mission_id BIGINT NULL,
    demon_id INT NOT NULL,
    started_at DATETIME NOT NULL,
    ended_at DATETIME NULL,
    location VARCHAR(150) NOT NULL,
    outcome ENUM('HUMAN_WIN','DEMON_WIN','DRAW','ESCAPE') NOT NULL,
    civilian_killed INT DEFAULT 0,
    civilian_injured INT DEFAULT 0,
    notes TEXT NULL,
    FOREIGN KEY (mission_id) REFERENCES Mission(mission_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (demon_id) REFERENCES Demon(demon_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE BountyClaim (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    battle_id INT NOT NULL,
    demon_id INT NOT NULL,
    human_id INT NOT NULL,
    amount INT NOT NULL,
    claim_date DATETIME NOT NULL,
    notes VARCHAR(255) NULL,
    FOREIGN KEY (battle_id) REFERENCES Battle(battle_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (demon_id) REFERENCES Demon(demon_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (human_id) REFERENCES Human(human_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE Account (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    hunter_id INT NOT NULL,
    balance INT DEFAULT 0,
    total_income INT DEFAULT 0,
    total_spent INT DEFAULT 0,
    last_tx_type ENUM('IN','OUT') NULL,
    last_tx_amount INT NULL,
    last_tx_desc VARCHAR(255) NULL,
    history TEXT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (hunter_id) REFERENCES Human(human_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

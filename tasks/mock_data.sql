-- Drop existing tables in reverse order of creation or use CASCADE
DROP TABLE IF EXISTS missing_players CASCADE;
DROP TABLE IF EXISTS team_form CASCADE;
DROP TABLE IF EXISTS player_statistics CASCADE;
DROP TABLE IF EXISTS match_players CASCADE;
DROP TABLE IF EXISTS player_teams CASCADE;
DROP TABLE IF EXISTS team_tournaments CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS seasons CASCADE;
DROP TABLE IF EXISTS unique_tournaments CASCADE;
DROP TABLE IF EXISTS venues CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS sports CASCADE;

-- DDL Statements
CREATE TABLE sports (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE countries (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    alpha2 CHAR(2),
    alpha3 CHAR(3),
    flag VARCHAR(50)
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL REFERENCES countries(id)
);

CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    sport_id INT NOT NULL REFERENCES sports(id),
    country_id INT NOT NULL REFERENCES countries(id),
    flag VARCHAR(50),
    alpha2 CHAR(2)
);

CREATE TABLE venues (
    id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200),
    capacity INT,
    city_id INT REFERENCES cities(id),
    country_id INT REFERENCES countries(id),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE unique_tournaments (
    id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    category_id INT NOT NULL REFERENCES categories(id),
    user_count INT DEFAULT 0,
    primary_color_hex VARCHAR(7),
    secondary_color_hex VARCHAR(7),
    has_event_player_statistics BOOLEAN DEFAULT FALSE,
    has_performance_graph_feature BOOLEAN DEFAULT FALSE,
    display_inverse_home_away_teams BOOLEAN DEFAULT FALSE
);

CREATE TABLE seasons (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    year VARCHAR(10) NOT NULL,
    editor BOOLEAN DEFAULT FALSE
);

CREATE TABLE tournaments (
    id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    unique_tournament_id INT NOT NULL REFERENCES unique_tournaments(id),
    season_id INT REFERENCES seasons(id),
    is_live BOOLEAN DEFAULT FALSE,
    is_group BOOLEAN DEFAULT FALSE,
    priority INT
);

CREATE TABLE teams (
    id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    short_name VARCHAR(100),
    full_name VARCHAR(200),
    name_code VARCHAR(10),
    type INT DEFAULT 0, -- 0 for club, 1 for national team
    gender CHAR(1) DEFAULT 'M', -- M for male, F for female
    country_id INT NOT NULL REFERENCES countries(id),
    venue_id INT REFERENCES venues(id),
    user_count INT DEFAULT 0,
    national BOOLEAN DEFAULT FALSE,
    disabled BOOLEAN DEFAULT FALSE,
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    text_color VARCHAR(7)
);

CREATE TABLE players (
    id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    short_name VARCHAR(200),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    height INT, -- in cm
    country_id INT NOT NULL REFERENCES countries(id),
    position CHAR(1), -- G, D, M, F
    shirt_number INT,
    jersey_number VARCHAR(5), -- Can be non-numeric sometimes
    preferred_foot VARCHAR(10), -- Left, Right, Both
    date_of_birth_timestamp BIGINT, -- Unix timestamp
    contract_until_timestamp BIGINT, -- Unix timestamp
    retired BOOLEAN DEFAULT FALSE,
    deceased BOOLEAN DEFAULT FALSE,
    user_count INT DEFAULT 0,
    market_value_currency VARCHAR(3) DEFAULT 'EUR',
    proposed_market_value DECIMAL(15,2) -- Proposed market value by users
);

CREATE TABLE matches (
    id INT PRIMARY KEY,
    slug VARCHAR(200) NOT NULL UNIQUE,
    tournament_id INT NOT NULL REFERENCES tournaments(id),
    season_id INT REFERENCES seasons(id),
    home_team_id INT NOT NULL REFERENCES teams(id),
    away_team_id INT NOT NULL REFERENCES teams(id),
    start_timestamp BIGINT NOT NULL,
    home_score_current INT DEFAULT 0,
    away_score_current INT DEFAULT 0,
    home_score_period1 INT DEFAULT 0,
    away_score_period1 INT DEFAULT 0,
    home_score_period2 INT DEFAULT 0,
    away_score_period2 INT DEFAULT 0,
    home_score_normaltime INT DEFAULT 0,
    away_score_normaltime INT DEFAULT 0,
    status_code INT NOT NULL,
    status_type VARCHAR(20) NOT NULL, -- e.g., "finished", "inprogress", "notstarted"
    status_description VARCHAR(50),
    winner_code INT, -- 1 for home, 2 for away, 3 for draw
    round_number INT,
    injury_time1 INT DEFAULT 0,
    injury_time2 INT DEFAULT 0,
    home_red_cards INT DEFAULT 0,
    away_red_cards INT DEFAULT 0,
    final_result_only BOOLEAN DEFAULT FALSE,
    has_global_highlights BOOLEAN DEFAULT FALSE,
    has_event_player_heat_map BOOLEAN DEFAULT FALSE,
    has_event_player_statistics BOOLEAN DEFAULT FALSE
);

CREATE TABLE team_tournaments (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id),
    tournament_id INT NOT NULL REFERENCES tournaments(id),
    season_id INT REFERENCES seasons(id),
    is_primary BOOLEAN DEFAULT FALSE,
    UNIQUE (team_id, tournament_id, season_id)
);

CREATE TABLE player_teams (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id),
    team_id INT NOT NULL REFERENCES teams(id),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE
);

CREATE TABLE match_players (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id),
    player_id INT NOT NULL REFERENCES players(id),
    team_id INT NOT NULL REFERENCES teams(id), -- Team player played for in this match
    position VARCHAR(2), -- G, D, M, F or more specific like CB, LW, etc.
    shirt_number INT,
    jersey_number VARCHAR(5),
    is_substitute BOOLEAN DEFAULT FALSE,
    is_captain BOOLEAN DEFAULT FALSE,
    formation_position VARCHAR(20), -- e.g., 4-3-3 LWF
    UNIQUE (match_id, player_id)
);

CREATE TABLE player_statistics (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id),
    player_id INT NOT NULL REFERENCES players(id),
    team_id INT NOT NULL REFERENCES teams(id), -- Team for which player got stats in this match
    rating DECIMAL(3,1),
    minutes_played INT DEFAULT 0,
    goals INT DEFAULT 0,
    goal_assist INT DEFAULT 0,
    total_pass INT DEFAULT 0,
    accurate_pass INT DEFAULT 0,
    total_long_balls INT DEFAULT 0,
    accurate_long_balls INT DEFAULT 0,
    total_cross INT DEFAULT 0,
    accurate_cross INT DEFAULT 0,
    key_pass INT DEFAULT 0,
    total_tackle INT DEFAULT 0,
    total_clearance INT DEFAULT 0,
    interception_won INT DEFAULT 0,
    outfielder_block INT DEFAULT 0,
    duel_won INT DEFAULT 0,
    duel_lost INT DEFAULT 0,
    aerial_won INT DEFAULT 0,
    aerial_lost INT DEFAULT 0,
    touches INT DEFAULT 0,
    shot_off_target INT DEFAULT 0,
    on_target_scoring_attempt INT DEFAULT 0,
    blocked_scoring_attempt INT DEFAULT 0,
    big_chance_missed INT DEFAULT 0,
    big_chance_created INT DEFAULT 0,
    total_offside INT DEFAULT 0,
    expected_goals DECIMAL(6,4) DEFAULT 0,
    expected_assists DECIMAL(8,6) DEFAULT 0,
    possession_lost_ctrl INT DEFAULT 0,
    fouls INT DEFAULT 0,
    was_fouled INT DEFAULT 0,
    saves INT DEFAULT 0,
    goals_prevented DECIMAL(6,4) DEFAULT 0,
    saved_shots_from_inside_the_box INT DEFAULT 0,
    dispossessed INT DEFAULT 0,
    won_contest INT DEFAULT 0,
    total_contest INT DEFAULT 0,
    challenge_lost INT DEFAULT 0,
    error_lead_to_a_shot INT DEFAULT 0,
    UNIQUE (match_id, player_id, team_id)
);

CREATE TABLE team_form (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id),
    tournament_id INT REFERENCES tournaments(id),
    season_id INT REFERENCES seasons(id),
    form_string VARCHAR(10), -- e.g., "WLWWW"
    form_value VARCHAR(5), -- e.g., "3-0"
    position_in_table INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE missing_players (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id),
    player_id INT NOT NULL REFERENCES players(id),
    team_id INT NOT NULL REFERENCES teams(id),
    reason_code INT NOT NULL -- 0=injury, 1=suspension, etc
);

-- DML Statements (Mock Data)

-- Sports
INSERT INTO sports (id, name, slug) VALUES (1, 'Football', 'football');

-- Countries
INSERT INTO countries (id, name, slug, alpha2, alpha3, flag) VALUES
(1, 'Brazil', 'brazil', 'BR', 'BRA', '🇧🇷'),
(2, 'Argentina', 'argentina', 'AR', 'ARG', '🇦🇷'),
(3, 'Spain', 'spain', 'ES', 'ESP', '🇪🇸'),
(4, 'England', 'england', 'GB', 'ENG', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
(5, 'Germany', 'germany', 'DE', 'DEU', '🇩🇪');

-- Cities
INSERT INTO cities (name, country_id) VALUES
('Rio de Janeiro', 1),
('São Paulo', 1),
('Buenos Aires', 2),
('Madrid', 3),
('Barcelona', 3),
('London', 4),
('Manchester', 4),
('Berlin', 5);

-- Categories (Leagues for Football)
INSERT INTO categories (id, name, slug, sport_id, country_id, flag) VALUES
(1, 'Brasileirão Série A', 'brasileirao-serie-a', 1, 1, '🇧🇷'),
(2, 'Superliga Argentina', 'superliga-argentina', 1, 2, '🇦🇷'),
(3, 'La Liga', 'la-liga', 1, 3, '🇪🇸'),
(4, 'Premier League', 'premier-league', 1, 4, '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
(5, 'Bundesliga', 'bundesliga', 1, 5, '🇩🇪');

-- Venues
INSERT INTO venues (id, name, slug, capacity, city_id, country_id) VALUES
(1, 'Maracanã', 'maracana', 78838, 1, 1),
(2, 'Estadio Monumental', 'estadio-monumental', 70074, 3, 2),
(3, 'Santiago Bernabéu', 'santiago-bernabeu', 81044, 4, 3),
(4, 'Wembley Stadium', 'wembley-stadium', 90000, 6, 4),
(5, 'Allianz Arena', 'allianz-arena', 75000, 8, 5);

-- Unique Tournaments (League Names)
INSERT INTO unique_tournaments (id, name, slug, category_id, user_count, primary_color_hex, secondary_color_hex) VALUES
(1, 'Brasileirão Série A', 'brasileirao-serie-a', 1, 150000, '#009B3A', '#FFCC29'),
(2, 'Superliga Argentina', 'superliga-argentina', 2, 120000, '#75AADB', '#FFFFFF'),
(3, 'La Liga Santander', 'la-liga-santander', 3, 200000, '#EE8700', '#FFFFFF'),
(4, 'Premier League', 'premier-league', 4, 300000, '#3D195B', '#FFFFFF'),
(5, 'Bundesliga', 'bundesliga', 5, 180000, '#D20515', '#FFFFFF');

-- Seasons
INSERT INTO seasons (id, name, year, editor) VALUES
(1, '2023', '2023', FALSE),
(2, '2022/2023', '2022/2023', FALSE),
(3, '2024', '2024', FALSE);

-- Tournaments (League Editions)
INSERT INTO tournaments (id, name, slug, unique_tournament_id, season_id, priority) VALUES
(1, 'Brasileirão Série A 2023', 'brasileirao-serie-a-2023', 1, 1, 10),
(2, 'Superliga Argentina 2022/2023', 'superliga-argentina-2022-2023', 2, 2, 9),
(3, 'La Liga Santander 2023/2024', 'la-liga-santander-2023-2024', 3, 3, 12),
(4, 'Premier League 2023/2024', 'premier-league-2023-2024', 4, 3, 15),
(5, 'Bundesliga 2023/2024', 'bundesliga-2023-2024', 5, 3, 11);

-- Teams
INSERT INTO teams (id, name, slug, short_name, country_id, venue_id, national) VALUES
(101, 'Flamengo', 'flamengo', 'FLA', 1, 1, FALSE),
(102, 'Palmeiras', 'palmeiras', 'PAL', 1, NULL, FALSE),
(201, 'Boca Juniors', 'boca-juniors', 'BOC', 2, 2, FALSE),
(301, 'Real Madrid', 'real-madrid', 'RMA', 3, 3, FALSE),
(401, 'Manchester City', 'manchester-city', 'MCI', 4, NULL, FALSE),
(501, 'Bayern München', 'bayern-munchen', 'BAY', 5, 5, FALSE);

-- Players
INSERT INTO players (id, name, slug, short_name, country_id, position, date_of_birth_timestamp, height, preferred_foot) VALUES
(1001, 'Gabriel Barbosa', 'gabriel-barbosa', 'Gabigol', 1, 'F', 809980800, 178, 'Left'), -- Approx 1995-08-30
(1002, 'Endrick Felipe', 'endrick-felipe', 'Endrick', 1, 'F', 1153785600, 173, 'Left'), -- Approx 2006-07-21
(2001, 'Edinson Cavani', 'edinson-cavani', 'Cavani', 2, 'F', 540432000, 184, 'Right'), -- Approx 1987-02-14
(3001, 'Jude Bellingham', 'jude-bellingham', 'Bellingham', 4, 'M', 1056931200, 186, 'Right'), -- Approx 2003-06-29
(4001, 'Erling Haaland', 'erling-haaland', 'Haaland', 4, 'F', 964089600, 194, 'Left'), -- Approx 2000-07-21
(5001, 'Harry Kane', 'harry-kane', 'Kane', 4, 'F', 743817600, 188, 'Right'); -- Approx 1993-07-28

-- Matches
INSERT INTO matches (id, slug, tournament_id, season_id, home_team_id, away_team_id, start_timestamp, status_code, status_type, home_score_normaltime, away_score_normaltime, winner_code) VALUES
(1, 'flamengo-vs-palmeiras-2023', 1, 1, 101, 102, 1672531200, 100, 'finished', 1, 1, 3), -- Approx 2023-01-01
(2, 'real-madrid-vs-manchester-city-2024', 3, 3, 301, 401, 1704067200, 100, 'finished', 3, 3, 3); -- Approx 2024-01-01

-- Team Tournaments
INSERT INTO team_tournaments (team_id, tournament_id, season_id, is_primary) VALUES
(101, 1, 1, TRUE), (102, 1, 1, TRUE),
(301, 3, 3, TRUE), (401, 4, 3, TRUE); -- Assuming Man City is in PL for this season

-- Player Teams (Contracts/Transfers)
INSERT INTO player_teams (player_id, team_id, start_date, is_current) VALUES
(1001, 101, '2020-01-01', TRUE),
(3001, 301, '2023-07-01', TRUE),
(4001, 401, '2022-07-01', TRUE);

-- Match Players (Lineups)
INSERT INTO match_players (match_id, player_id, team_id, position, shirt_number) VALUES
(1, 1001, 101, 'CF', 9), -- Gabigol for Flamengo
(2, 3001, 301, 'CM', 5), -- Bellingham for Real Madrid
(2, 4001, 401, 'CF', 9); -- Haaland for Man City

-- Player Statistics
INSERT INTO player_statistics (match_id, player_id, team_id, rating, minutes_played, goals, total_pass, accurate_pass, expected_goals) VALUES
(1, 1001, 101, 7.5, 90, 1, 30, 25, 0.8),
(2, 3001, 301, 8.2, 88, 1, 60, 55, 0.5),
(2, 4001, 401, 7.8, 90, 1, 20, 15, 1.2);

-- Team Form
INSERT INTO team_form (team_id, tournament_id, season_id, form_string) VALUES
(101, 1, 1, 'WDWLW'),
(301, 3, 3, 'WWWDW');

-- Missing Players
INSERT INTO missing_players (match_id, player_id, team_id, reason_code) VALUES
(1, 1002, 102, 0); -- Endrick missing for Palmeiras due to injury (reason_code 0)

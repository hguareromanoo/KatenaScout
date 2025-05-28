# backend/models/sql_models.py

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DECIMAL, BOOLEAN, BIGINT, DATE, TIMESTAMP, CHAR,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=False) # As per DDL: INT PRIMARY KEY
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    alpha2 = Column(CHAR(2))
    alpha3 = Column(CHAR(3))
    flag = Column(String(50))

    # Relationships
    cities = relationship("City", back_populates="country")
    categories = relationship("Category", back_populates="country")
    venues = relationship("Venue", back_populates="country")
    teams = relationship("Team", back_populates="country")
    players = relationship("Player", back_populates="country")

    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}')>"

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)

    # Relationships
    country = relationship("Country", back_populates="cities")
    venues = relationship("Venue", back_populates="city")

    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}')>"

class Sport(Base):
    __tablename__ = 'sports'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False, unique=True)

    # Relationships
    categories = relationship("Category", back_populates="sport")

    def __repr__(self):
        return f"<Sport(id={self.id}, name='{self.name}')>"

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    sport_id = Column(Integer, ForeignKey('sports.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    flag = Column(String(50))
    alpha2 = Column(CHAR(2))

    # Relationships
    sport = relationship("Sport", back_populates="categories")
    country = relationship("Country", back_populates="categories")
    unique_tournaments = relationship("UniqueTournament", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(200), nullable=False)
    slug = Column(String(200))
    capacity = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    hidden = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    city = relationship("City", back_populates="venues")
    country = relationship("Country", back_populates="venues")
    teams = relationship("Team", back_populates="venue")

    def __repr__(self):
        return f"<Venue(id={self.id}, name='{self.name}')>"

class UniqueTournament(Base):
    __tablename__ = 'unique_tournaments'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_count = Column(Integer, server_default='0')
    primary_color_hex = Column(String(7))
    secondary_color_hex = Column(String(7))
    has_event_player_statistics = Column(BOOLEAN, server_default='FALSE')
    has_performance_graph_feature = Column(BOOLEAN, server_default='FALSE')
    display_inverse_home_away_teams = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    category = relationship("Category", back_populates="unique_tournaments")
    tournaments = relationship("Tournament", back_populates="unique_tournament")

    def __repr__(self):
        return f"<UniqueTournament(id={self.id}, name='{self.name}')>"

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(100), nullable=False)
    year = Column(String(10), nullable=False)
    editor = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    tournaments = relationship("Tournament", back_populates="season")
    matches = relationship("Match", back_populates="season")
    team_tournaments = relationship("TeamTournament", back_populates="season")
    team_forms = relationship("TeamForm", back_populates="season")

    def __repr__(self):
        return f"<Season(id={self.id}, name='{self.name}', year='{self.year}')>"

class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    unique_tournament_id = Column(Integer, ForeignKey('unique_tournaments.id'), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    is_live = Column(BOOLEAN, server_default='FALSE')
    is_group = Column(BOOLEAN, server_default='FALSE')
    priority = Column(Integer)

    # Relationships
    unique_tournament = relationship("UniqueTournament", back_populates="tournaments")
    season = relationship("Season", back_populates="tournaments")
    matches = relationship("Match", back_populates="tournament")
    team_tournaments = relationship("TeamTournament", back_populates="tournament")
    team_forms = relationship("TeamForm", back_populates="tournament")


    def __repr__(self):
        return f"<Tournament(id={self.id}, name='{self.name}')>"

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    short_name = Column(String(100))
    full_name = Column(String(200))
    name_code = Column(String(10))
    type = Column(Integer, server_default='0')
    gender = Column(CHAR(1), server_default='M')
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    user_count = Column(Integer, server_default='0')
    national = Column(BOOLEAN, server_default='FALSE')
    disabled = Column(BOOLEAN, server_default='FALSE')
    primary_color = Column(String(7))
    secondary_color = Column(String(7))
    text_color = Column(String(7))

    # Relationships
    country = relationship("Country", back_populates="teams")
    venue = relationship("Venue", back_populates="teams")
    home_matches = relationship("Match", foreign_keys="[Match.home_team_id]", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="[Match.away_team_id]", back_populates="away_team")
    team_tournaments = relationship("TeamTournament", back_populates="team")
    player_teams = relationship("PlayerTeam", back_populates="team")
    match_players = relationship("MatchPlayer", back_populates="team") # A team has players in a match
    player_statistics = relationship("PlayerStatistic", back_populates="team") # Stats are recorded for a player of a team
    team_forms = relationship("TeamForm", back_populates="team")
    missing_players = relationship("MissingPlayer", back_populates="team")


    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    short_name = Column(String(200))
    first_name = Column(String(100))
    last_name = Column(String(100))
    height = Column(Integer)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    position = Column(CHAR(1)) # G, D, M, F
    shirt_number = Column(Integer)
    jersey_number = Column(String(5))
    preferred_foot = Column(String(10))
    date_of_birth_timestamp = Column(BIGINT)
    contract_until_timestamp = Column(BIGINT)
    retired = Column(BOOLEAN, server_default='FALSE')
    deceased = Column(BOOLEAN, server_default='FALSE')
    user_count = Column(Integer, server_default='0')
    market_value_currency = Column(String(3), server_default='EUR')
    proposed_market_value = Column(DECIMAL(15, 2))

    # Relationships
    country = relationship("Country", back_populates="players")
    player_teams = relationship("PlayerTeam", back_populates="player")
    match_players = relationship("MatchPlayer", back_populates="player")
    player_statistics = relationship("PlayerStatistic", back_populates="player")
    missing_players = relationship("MissingPlayer", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}')>"

class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=False) # INT PRIMARY KEY
    slug = Column(String(200), nullable=False, unique=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    start_timestamp = Column(BIGINT, nullable=False)
    home_score_current = Column(Integer, server_default='0')
    away_score_current = Column(Integer, server_default='0')
    home_score_period1 = Column(Integer, server_default='0')
    away_score_period1 = Column(Integer, server_default='0')
    home_score_period2 = Column(Integer, server_default='0')
    away_score_period2 = Column(Integer, server_default='0')
    home_score_normaltime = Column(Integer, server_default='0')
    away_score_normaltime = Column(Integer, server_default='0')
    status_code = Column(Integer, nullable=False)
    status_type = Column(String(20), nullable=False)
    status_description = Column(String(50))
    winner_code = Column(Integer) # 1=home, 2=away, 3=draw
    round_number = Column(Integer)
    injury_time1 = Column(Integer, server_default='0')
    injury_time2 = Column(Integer, server_default='0')
    home_red_cards = Column(Integer, server_default='0')
    away_red_cards = Column(Integer, server_default='0')
    final_result_only = Column(BOOLEAN, server_default='FALSE')
    has_global_highlights = Column(BOOLEAN, server_default='FALSE')
    has_event_player_heat_map = Column(BOOLEAN, server_default='FALSE')
    has_event_player_statistics = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    season = relationship("Season", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    match_players = relationship("MatchPlayer", back_populates="match")
    player_statistics = relationship("PlayerStatistic", back_populates="match")
    missing_players = relationship("MissingPlayer", back_populates="match")

    def __repr__(self):
        return f"<Match(id={self.id}, slug='{self.slug}')>"

class TeamTournament(Base):
    __tablename__ = 'team_tournaments'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    is_primary = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    team = relationship("Team", back_populates="team_tournaments")
    tournament = relationship("Tournament", back_populates="team_tournaments")
    season = relationship("Season", back_populates="team_tournaments")

    __table_args__ = (UniqueConstraint('team_id', 'tournament_id', 'season_id', name='unique_team_tournament_season'),)

    def __repr__(self):
        return f"<TeamTournament(id={self.id}, team_id={self.team_id}, tournament_id={self.tournament_id})>"

class PlayerTeam(Base):
    __tablename__ = 'player_teams'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    start_date = Column(DATE)
    end_date = Column(DATE)
    is_current = Column(BOOLEAN, server_default='FALSE')

    # Relationships
    player = relationship("Player", back_populates="player_teams")
    team = relationship("Team", back_populates="player_teams")

    def __repr__(self):
        return f"<PlayerTeam(id={self.id}, player_id={self.player_id}, team_id={self.team_id})>"

class MatchPlayer(Base):
    __tablename__ = 'match_players'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False) # Team player played for in this match
    position = Column(String(2)) # G, D, M, F (using String to be safe, DDL says VARCHAR(2))
    shirt_number = Column(Integer)
    jersey_number = Column(String(5))
    is_substitute = Column(BOOLEAN, server_default='FALSE')
    is_captain = Column(BOOLEAN, server_default='FALSE')
    formation_position = Column(String(20))

    # Relationships
    match = relationship("Match", back_populates="match_players")
    player = relationship("Player", back_populates="match_players")
    team = relationship("Team", back_populates="match_players")

    __table_args__ = (UniqueConstraint('match_id', 'player_id', name='unique_match_player'),)

    def __repr__(self):
        return f"<MatchPlayer(id={self.id}, match_id={self.match_id}, player_id={self.player_id})>"


class PlayerStatistic(Base):
    __tablename__ = 'player_statistics'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False) # Team for which player got stats in this match

    rating = Column(DECIMAL(3, 1))
    minutes_played = Column(Integer, server_default='0')
    goals = Column(Integer, server_default='0')
    goal_assist = Column(Integer, server_default='0')
    total_pass = Column(Integer, server_default='0')
    accurate_pass = Column(Integer, server_default='0')
    total_long_balls = Column(Integer, server_default='0')
    accurate_long_balls = Column(Integer, server_default='0')
    total_cross = Column(Integer, server_default='0')
    accurate_cross = Column(Integer, server_default='0')
    key_pass = Column(Integer, server_default='0')
    total_tackle = Column(Integer, server_default='0')
    total_clearance = Column(Integer, server_default='0')
    interception_won = Column(Integer, server_default='0')
    outfielder_block = Column(Integer, server_default='0')
    duel_won = Column(Integer, server_default='0')
    duel_lost = Column(Integer, server_default='0')
    aerial_won = Column(Integer, server_default='0')
    aerial_lost = Column(Integer, server_default='0')
    touches = Column(Integer, server_default='0')
    shot_off_target = Column(Integer, server_default='0')
    on_target_scoring_attempt = Column(Integer, server_default='0')
    blocked_scoring_attempt = Column(Integer, server_default='0')
    big_chance_missed = Column(Integer, server_default='0')
    big_chance_created = Column(Integer, server_default='0')
    total_offside = Column(Integer, server_default='0')
    expected_goals = Column(DECIMAL(6, 4), server_default='0')
    expected_assists = Column(DECIMAL(8, 6), server_default='0')
    possession_lost_ctrl = Column(Integer, server_default='0')
    fouls = Column(Integer, server_default='0')
    was_fouled = Column(Integer, server_default='0')
    saves = Column(Integer, server_default='0')
    goals_prevented = Column(DECIMAL(6, 4), server_default='0')
    saved_shots_from_inside_the_box = Column(Integer, server_default='0')
    dispossessed = Column(Integer, server_default='0')
    won_contest = Column(Integer, server_default='0')
    total_contest = Column(Integer, server_default='0')
    challenge_lost = Column(Integer, server_default='0')
    error_lead_to_a_shot = Column(Integer, server_default='0')

    # Relationships
    match = relationship("Match", back_populates="player_statistics")
    player = relationship("Player", back_populates="player_statistics")
    team = relationship("Team", back_populates="player_statistics")

    __table_args__ = (UniqueConstraint('match_id', 'player_id', 'team_id', name='unique_match_player_stats'),)

    def __repr__(self):
        return f"<PlayerStatistic(id={self.id}, match_id={self.match_id}, player_id={self.player_id})>"

class TeamForm(Base):
    __tablename__ = 'team_form'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    season_id = Column(Integer, ForeignKey('seasons.id'))
    form_string = Column(String(10)) # Ex: "WLWWW"
    form_value = Column(String(5))
    position_in_table = Column(Integer)
    updated_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    team = relationship("Team", back_populates="team_forms")
    tournament = relationship("Tournament", back_populates="team_forms")
    season = relationship("Season", back_populates="team_forms")

    def __repr__(self):
        return f"<TeamForm(id={self.id}, team_id={self.team_id}, form_string='{self.form_string}')>"

class MissingPlayer(Base):
    __tablename__ = 'missing_players'

    id = Column(Integer, primary_key=True, autoincrement=True) # SERIAL PRIMARY KEY
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    reason_code = Column(Integer, nullable=False) # 0=injury, 1=suspension, etc

    # Relationships
    match = relationship("Match", back_populates="missing_players")
    player = relationship("Player", back_populates="missing_players")
    team = relationship("Team", back_populates="missing_players")

    def __repr__(self):
        return f"<MissingPlayer(id={self.id}, match_id={self.match_id}, player_id={self.player_id}, reason_code={self.reason_code})>"

# Create Indexes (Optional but good for performance for foreign keys and frequently queried columns)
# Example: Index('ix_cities_country_id', City.country_id)
# Adding a few examples, more can be added as needed.

Index('ix_cities_country_id', City.country_id)
Index('ix_categories_sport_id', Category.sport_id)
Index('ix_categories_country_id', Category.country_id)
Index('ix_venues_city_id', Venue.city_id)
Index('ix_venues_country_id', Venue.country_id)
Index('ix_unique_tournaments_category_id', UniqueTournament.category_id)
Index('ix_tournaments_unique_tournament_id', Tournament.unique_tournament_id)
Index('ix_tournaments_season_id', Tournament.season_id)
Index('ix_teams_country_id', Team.country_id)
Index('ix_teams_venue_id', Team.venue_id)
Index('ix_players_country_id', Player.country_id)
Index('ix_matches_tournament_id', Match.tournament_id)
Index('ix_matches_season_id', Match.season_id)
Index('ix_matches_home_team_id', Match.home_team_id)
Index('ix_matches_away_team_id', Match.away_team_id)
Index('ix_team_tournaments_team_id', TeamTournament.team_id)
Index('ix_team_tournaments_tournament_id', TeamTournament.tournament_id)
Index('ix_team_tournaments_season_id', TeamTournament.season_id)
Index('ix_player_teams_player_id', PlayerTeam.player_id)
Index('ix_player_teams_team_id', PlayerTeam.team_id)
Index('ix_match_players_match_id', MatchPlayer.match_id)
Index('ix_match_players_player_id', MatchPlayer.player_id)
Index('ix_match_players_team_id', MatchPlayer.team_id)
Index('ix_player_statistics_match_id', PlayerStatistic.match_id)
Index('ix_player_statistics_player_id', PlayerStatistic.player_id)
Index('ix_player_statistics_team_id', PlayerStatistic.team_id)
Index('ix_team_form_team_id', TeamForm.team_id)
Index('ix_team_form_tournament_id', TeamForm.tournament_id)
Index('ix_team_form_season_id', TeamForm.season_id)
Index('ix_missing_players_match_id', MissingPlayer.match_id)
Index('ix_missing_players_player_id', MissingPlayer.player_id)
Index('ix_missing_players_team_id', MissingPlayer.team_id)

# End of models
# To create tables in DB (usually done in an app setup script):
# Base.metadata.create_all(engine)
# Example of engine setup (not part of models file):
# from sqlalchemy import create_engine
# DATABASE_URL = "postgresql://user:password@host:port/database"
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)

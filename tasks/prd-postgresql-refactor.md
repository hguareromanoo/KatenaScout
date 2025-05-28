# Product Requirements Document: KatenaScout - PostgreSQL Refactor

## 1. Introduction/Overview

*   **Project:** KatenaScout - Soccer Scouting AI Web App (Python Flask backend).
*   **Feature:** Refactor data persistence layer from local JSON files to a PostgreSQL database using SQLAlchemy ORM.
*   **Problem:** Current JSON-based storage is not scalable for the expected increase in player data.
*   **Goal:** To enhance scalability and maintainability by migrating to a robust relational database system.

## 2. Goals

*   Replace current JSON-based data storage (`database.json`, `db_by_id.json`, `team.json`) with a PostgreSQL database.
*   Implement SQLAlchemy as the ORM for all database interactions within the backend.
*   Define SQLAlchemy models that accurately represent the provided PostgreSQL schema.
*   Refactor the data service layer (`services/data_service.py`) to use SQLAlchemy for all CRUD operations.
*   Ensure all existing application functionalities (player search, comparison, data analysis, report generation, image serving) that depend on data storage continue to work seamlessly with the new database.
*   Configure the Flask application to connect to the PostgreSQL database.
*   Refactor the handling of auxiliary JSON files (`average_statistics_by_position.json`, `weights_dict.json`, `sigma_statistics_by_position.json`) to derive their data dynamically from PostgreSQL where possible.
*   Implement a clear strategy for player position handling, using a default mapping from the database's general position codes to more specific application-level codes, ensuring modularity for future enhancements.

## 3. User Stories

*   As a System Administrator, I want the application to use a PostgreSQL database so that it can efficiently manage and scale to a large number of players and their detailed statistics.
*   As a Developer, I want to use SQLAlchemy ORM to interact with the PostgreSQL database, leading to more maintainable, robust, and standardized data access code.
*   As an End-User (e.g., Club CEO/President), I want the application to perform all its existing data retrieval, player scouting, comparison, and analysis functions without any noticeable change in behavior or degradation in performance after the database migration.

## 4. Functional Requirements

*   **FR1:** The system must use a PostgreSQL database for persistence of all primary data entities (players, teams, matches, etc., as per the provided schema).
*   **FR2:** The system must use SQLAlchemy as the ORM for all database interactions (queries, inserts, updates, deletes).
*   **FR3:** SQLAlchemy models must be defined to map to each table in the provided PostgreSQL schema: `countries`, `cities`, `sports`, `categories`, `venues`, `unique_tournaments`, `seasons`, `tournaments`, `teams`, `players`, `matches`, `team_tournaments`, `player_teams`, `match_players`, `player_statistics`, `team_form`, `missing_players`.
*   **FR4:** The database connection parameters (host, port, user, password, database name) must be configurable (e.g., via environment variables or `config.py`).
*   **FR5:** The `services/data_service.py` module must be refactored:
    *   All functions currently reading from JSON files (`get_player_database`, `get_player_database_by_id`, `get_team_names`, `find_player_by_id`, `find_player_by_name`, `get_players_with_position`) must be updated to query the PostgreSQL database via SQLAlchemy.
    *   The caching mechanism (`_data_cache`) for JSON files should be removed or re-evaluated for database query results if necessary.
*   **FR6:** All parts of the application (especially in `app.py` routes and `core` modules) that currently consume data from `data_service.py` must continue to function correctly with the data retrieved from PostgreSQL. This includes adapting to the new player position mapping strategy (see FR11).
*   **FR7:** Existing Pydantic models in `models/player.py` (and others) should be reviewed. If they are used for API request/response validation, a clear conversion mechanism between SQLAlchemy models and Pydantic models must be implemented. Pydantic models should reflect the mapped granular positions where applicable.
*   **FR8:** The player image serving endpoint (`/player-image/<player_id>`) in `app.py` must be updated to fetch image information (e.g., URL or path if stored in the DB) from PostgreSQL if applicable, or continue its current logic if image data is not part of the `players` table. (The `players` table schema has `market_value_currency` and `proposed_market_value`, but no direct image URL. The old JSON had `imageDataURL`). This needs to be reconciled.
*   **FR9:** The handling of auxiliary data files must be refactored:
    *   `average_statistics_by_position.json`: Its data must be dynamically calculated from the `player_statistics` table in PostgreSQL using appropriate aggregate functions (e.g., AVG) grouped by player position.
    *   `sigma_statistics_by_position.json` (previously implicitly handled): Its data (standard deviations) must be dynamically calculated from the `player_statistics` table in PostgreSQL using appropriate aggregate functions (e.g., STDDEV) grouped by player position.
    *   `weights_dict.json`: The strategy for managing weights must be implemented. Options include:
        *   Dynamic calculation based on certain criteria (if applicable).
        *   Storing weights in a new dedicated configuration table in PostgreSQL.
        *   Defining weights within the application's configuration (e.g., `config.py`) if they are relatively static.
        The chosen method must be implemented, replacing the JSON file.
*   **FR10:** Data integrity must be maintained according to the foreign key constraints and relationships defined in the SQL schema.
*   **FR11:** Player position handling must be implemented using a fallback mapping from the `players.position` (CHAR(1)) field to specific application-level position codes.
    *   Initial mapping: 'G' -> 'gk', 'D' -> 'cb', 'M' -> 'rcmf', 'F' -> 'cf'.
    *   The implementation should be modular (e.g., a dedicated mapping function or service) to allow for future enhancements, such as incorporating more detailed position data from web scraping or other sources, without major refactoring of consuming logic.

## 5. Non-Goals (Out of Scope)

*   Migration of existing data from the current JSON files (`database.json`, `db_by_id.json`) to PostgreSQL, as this data is considered mock/useless. New mock data will be provided for the SQL database.
*   Changes to the frontend React application (API contracts should remain consistent).
*   Introduction of new application features beyond the database refactoring.
*   Fundamental changes to the existing business logic in the `core` modules, other than adapting to new data access methods.
*   Setting up the PostgreSQL server instance itself or managing its backups and maintenance. The focus is on application-level integration.
*   Significant performance optimization beyond ensuring the application remains responsive and functions as before.

## 6. Design Considerations (Optional)

*   The PostgreSQL schema is predefined by the user. SQLAlchemy models must strictly adhere to this schema.
*   Database session management should be handled carefully within the Flask application context (e.g., request-scoped sessions).
*   Consider creating a dedicated module (e.g., `backend/database.py`) for SQLAlchemy engine setup, session factory, and base model declaration.

## 7. Technical Considerations (Optional)

*   Backend Programming Language: Python (Flask framework).
*   ORM: SQLAlchemy.
*   Database: PostgreSQL.
*   Key modules to be refactored: `services/data_service.py`, `app.py`, potentially `models/*`.
*   Environment variables should be the preferred method for storing database credentials.
*   SQL aggregate functions (AVG, STDDEV, etc.) will be used for dynamic calculation of statistics previously stored in JSON files.

## 8. Success Metrics

*   All existing application endpoints that rely on data (e.g., `/players/search`, `/enhanced_search`, `/player_comparison`, `/scout_report`, `/player-image`) operate correctly using data from the PostgreSQL database.
*   The application successfully connects to and performs CRUD operations on the PostgreSQL database using SQLAlchemy.
*   No regressions in functionality related to player scouting, natural language processing, comparison, data analysis, and report generation.
*   Code in `services/data_service.py` and other affected modules is successfully refactored to use SQLAlchemy models and session.
*   The system can be run with a PostgreSQL backend by configuring the necessary connection parameters.

## 9. Open Questions

*   **[Resolved]** How should `average_statistics_by_position.json`, `weights_dict.json`, and `sigma_statistics_by_position.json` be handled?
    *   **Resolution:** These files will be replaced. `average_statistics_by_position.json` and `sigma_statistics_by_position.json` data will be dynamically calculated from the `player_statistics` table in PostgreSQL using aggregate functions. The strategy for `weights_dict.json` (dynamic, new table, or app config) will be implemented.
*   **[Partially Resolved]** The provided `players` SQL table schema does not have a direct field for `imageDataURL` which was present in the JSON. How should player images be handled?
    *   **Partial Resolution:** While the image URL storage remains an open question for direct DB integration, player position data from `players.position` (CHAR(1)) will be mapped to default granular codes ('G' -> 'gk', 'D' -> 'cb', 'M' -> 'rcmf', 'F' -> 'cf') as a fallback. This mapping should be modular for future enhancements. The direct image data handling (imageDataURL) is still TBD.
*   **[Resolved]** Are there specific environment variable names to be used for PostgreSQL connection details (e.g., `POSTGRES_HOST`, `POSTGRES_DB`)?
    *   **Resolution:** Yes, standard environment variables like `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB` are defined in `backend/config.py` and used to construct `DATABASE_URL`.
*   **[Resolved]** What is the expected mechanism for creating the database schema in the PostgreSQL instance? Should the application create it (e.g. using `metadata.create_all()`) or is it assumed to exist?
    *   **Resolution:** The SQL DDL for schema creation has been provided by the user. The application can use `Base.metadata.create_all(engine)` (e.g., via `init_db()` in `backend/database.py`) for initial setup if needed, but the DDL serves as the canonical schema definition.

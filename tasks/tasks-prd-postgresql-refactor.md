## Relevant Files

- `backend/models/sql_models.py` - Contains SQLAlchemy ORM models. (FR3)
- `backend/models/player.py` - Contains Pydantic models for player data; will need review and updates for API contracts, especially regarding player positions. (FR7)
- `backend/database.py` - Manages DB engine (`create_engine`) and session creation (`SessionLocal`, `get_db`). (FR4, Design Considerations)
- `backend/config.py` - Stores DB connection URLs (from environment variables) and potentially new configurations for weights. (FR4)
- `backend/services/data_service.py` - Core data access logic to be refactored for SQLAlchemy, dynamic stats, and position mapping. (FR5, FR9, FR11)
- `backend/services/tests/test_data_service.py` - Unit tests for `data_service.py`. (To be created or updated)
- `backend/app.py` - Flask application; route handlers will need updates to use new data service methods and session management. (FR6)
- `backend/tests/test_app.py` - Integration tests for Flask app routes. (To be created or updated)
- `backend/core/` - Various modules (e.g., `player_scouting.py`, `player_comparison.py`, `report_generation.py`) that consume data services will need updates. (FR6)
- `backend/core/tests/` - Unit tests for core logic modules. (To be created or updated)
- `tasks/mock_data.sql` - (New file) SQL script for populating the PostgreSQL database with mock data for testing and development. (Non-Goal: no production data migration, but mock data is needed).
- `backend/requirements.txt` - Add/verify `psycopg2-binary` and `SQLAlchemy`.
- `README.md` or `docs/database_setup.md` - Documentation to be updated with new setup instructions.

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., in a `tests` subdirectory within `backend/services/`) or in a dedicated top-level test directory, following project conventions.
- Use a testing framework like `pytest`. Commands might be `pytest` or `python -m pytest`.
- Ensure tests cover both successful cases and error handling.
- For testing database interactions, consider using a separate test database or transaction rollbacks to keep tests isolated. In-memory SQLite can be an option for faster unit tests if the SQL dialect is mostly compatible, but testing against PostgreSQL is better for integration tests.
- Sub-tasks related to "implementing" a function also imply writing corresponding unit tests.

## Tasks

- [ ] **1.0 PostgreSQL Integration Foundation: SQLAlchemy Models, Configuration, and Connectivity**
  - [ ] 1.1 Verify/finalize SQLAlchemy ORM models in `backend/models/sql_models.py` against the provided DDL. Ensure all relationships, constraints, and data types are correct. (FR3)
  - [ ] 1.2 Update `backend/config.py` to include PostgreSQL connection parameters (user, password, host, port, db name) loaded from environment variables, and construct `DATABASE_URL`. (FR4)
  - [ ] 1.3 Create `backend/database.py` with SQLAlchemy engine setup (`create_engine`), session factory (`SessionLocal`), and a dependency injectable `get_db` function for request-scoped sessions. (FR4, Design Considerations)
  - [ ] 1.4 Add `SQLAlchemy` and `psycopg2-binary` to `backend/requirements.txt` and ensure they are installed in the development environment.
  - [ ] 1.5 Develop an `init_db()` function (e.g., in `backend/database.py` or a separate script) that uses `Base.metadata.create_all(engine)` to create the schema in the PostgreSQL database. (Implied by DDL provision)
  - [ ] 1.6 Test database connectivity by attempting to connect to the PostgreSQL server using the configured settings.

- [ ] **2.0 Core Data Service Refactoring: Migrating Basic CRUD to SQLAlchemy**
  - [ ] 2.1 Remove old JSON file loading logic for `database.json`, `db_by_id.json`, `team.json` from `backend/services/data_service.py`. (FR5)
  - [ ] 2.2 Refactor `find_player_by_id(player_id: int, db: Session)` in `data_service.py` to query the `players` table using SQLAlchemy. (FR5)
  - [ ] 2.3 Refactor `find_player_by_name(player_name: str, db: Session)` in `data_service.py` to query the `players` table using SQLAlchemy (e.g., with case-insensitive search). (FR5)
  - [ ] 2.4 Refactor `get_team_names(db: Session)` in `data_service.py` to query the `teams` table (and `countries` for country name) using SQLAlchemy. (FR5)
  - [ ] 2.5 Refactor `find_club_by_id(club_id: int, db: Session)` in `data_service.py` (originally using `team.json`) to query the `teams` table using SQLAlchemy. (FR5)
  - [ ] 2.6 Write/update unit tests in `backend/services/tests/test_data_service.py` for the refactored CRUD functions, mocking the DB session and models.

- [ ] **3.0 Advanced Data Logic Implementation: Dynamic Statistics and Position Mapping**
  - [ ] 3.1 Design and implement the player position fallback mapping logic in `data_service.py` or a new dedicated module (e.g., `backend/utils/position_mapper.py`) as per FR11 ('G' -> 'gk', 'D' -> 'cb', 'M' -> 'rcmf', 'F' -> 'cf').
  - [ ] 3.2 Refactor `get_players_with_position(position_code: str, db: Session)` in `data_service.py` to use the new position mapping logic if the input `position_code` is one of the general DB codes, or query directly if it's a specific one. (FR5, FR11)
  - [ ] 3.3 Refactor `get_average_statistics()` in `data_service.py`:
    - [ ] 3.3.1 Remove loading from `average_statistics_by_position.json`.
    - [ ] 3.3.2 Implement dynamic calculation of average player statistics by position using SQLAlchemy aggregate functions (AVG) on the `player_statistics` table, grouped by mapped player position. (FR9)
  - [ ] 3.4 Refactor `get_sigma_by_position()` in `data_service.py`:
    - [ ] 3.4.1 Remove loading from `sigma_statistics_by_position.json`.
    - [ ] 3.4.2 Implement dynamic calculation of standard deviation for player statistics by position using SQLAlchemy aggregate functions (STDDEV_SAMP or STDDEV_POP) on the `player_statistics` table, grouped by mapped player position. (FR9)
  - [ ] 3.5 Address `get_weights_dictionary()` in `data_service.py`:
    - [ ] 3.5.1 Remove loading from `weights_dict.json`.
    - [ ] 3.5.2 Implement the chosen strategy for weights (e.g., store in `config.py`, a new DB table, or calculate dynamically if feasible). (FR9)
  - [ ] 3.6 Write/update unit tests for the dynamic statistics calculation and position mapping logic.

- [ ] **4.0 Application-Wide Integration: Updating API Endpoints and Core Logic**
  - [ ] 4.1 Review all API endpoints in `backend/app.py` that use affected `data_service.py` functions.
  - [ ] 4.2 Update these endpoints to correctly pass the SQLAlchemy `db: Session` (obtained via `get_db` dependency) to `data_service.py` functions.
  - [ ] 4.3 Adapt endpoint logic to handle SQLAlchemy model instances returned by `data_service.py` instead of dictionaries (e.g., attribute access `player.name` vs. dict access `player['name']`).
  - [ ] 4.4 Update core logic modules in `backend/core/*` (e.g., player comparison, report generation) to use the refactored `data_service.py` methods and adapt to new data formats (SQLAlchemy models, mapped positions). (FR6)
  - [ ] 4.5 Write/update integration tests in `backend/tests/test_app.py` for the modified API endpoints.

- [ ] **5.0 API Data Model Alignment: Pydantic Model Updates and SQLAlchemy-Pydantic Conversion**
  - [ ] 5.1 Review Pydantic models in `backend/models/player.py` (and others if relevant). (FR7)
  - [ ] 5.2 Update Pydantic models to reflect data structures returned by SQLAlchemy queries and any changes due to position mapping (e.g., if a specific position field is added/modified). (FR7)
  - [ ] 5.3 Implement or refine a clear conversion mechanism from SQLAlchemy model instances to Pydantic models for API responses. This might involve helper functions or Pydantic's `from_orm` mode. (FR7)
  - [ ] 5.4 Ensure API request validation using Pydantic models still functions correctly.

- [ ] **6.0 Player Image Data Handling Strategy and Implementation**
  - [ ] 6.1 Analyze the existing player image serving endpoint (`/player-image/<player_id>`) in `app.py` and its current logic for finding image URLs/paths. (FR8)
  - [ ] 6.2 Investigate if player image URLs or identifiers can/should be stored in the `players` table or a related table (this is an open question in PRD).
  - [ ] 6.3 Based on findings, update the endpoint:
    - [ ] 6.3.1 If image info is moved to DB: Modify to query this information via `data_service.py`.
    - [ ] 6.3.2 If image info remains file-based or external: Ensure current logic is compatible with other changes (e.g., player ID handling). (FR8)
  - [ ] 6.4 Test the player image serving endpoint thoroughly.

- [ ] **7.0 Comprehensive Testing, Mock Data Population, and Documentation Updates**
  - [ ] 7.1 Create a `tasks/mock_data.sql` script (or Python script using SQLAlchemy) to populate PostgreSQL with comprehensive mock data covering all relevant tables and scenarios for testing.
  - [ ] 7.2 Ensure all new and refactored functionalities are covered by unit tests (for individual functions/modules) and integration tests (for API endpoints and critical workflows).
  - [ ] 7.3 Perform end-to-end testing of all application features that rely on data (player search, comparison, report generation, etc.). (Success Metrics)
  - [ ] 7.4 Update `README.md` or other project documentation with:
    - [ ] 7.4.1 Instructions for setting up the PostgreSQL database.
    - [ ] 7.4.2 Information about environment variables for DB connection.
    - [ ] 7.4.3 Instructions for running the `init_db()` script and populating mock data.
    - [ ] 7.4.4 Any changes to API contracts if Pydantic models were significantly altered.
  - [ ] 7.5 Review and resolve any remaining "Open Questions" in the PRD if possible, or document why they remain open.

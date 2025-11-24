# Development Journal

This document tracks the "stream of consciousness" of the project's evolution. It captures the intent before changes are made and the conclusion after they are complete.

## 2025-11-24: Data Reset Feature

### Intent
**Objective**: Add a feature to clear all data for a fresh start.
**Scope**:
- Create a script to remove all persistence data (Postgres volumes).
- Ensure the system can restart cleanly after reset.
**Rationale**: We need a way to clear the system state for testing and "fresh start" scenarios without manually deleting docker volumes.

### Conclusion
**Changes**:
- Created `scripts/reset_data.py` which uses `docker compose down -v` to remove volumes and `docker compose up -d db` to restart the database.
- Updated `README.md` with instructions.
**Verification**:
- Verified that running the script removes the `embeddings` table and resets the database.
- Confirmed `check_db.py` shows no tables after reset.

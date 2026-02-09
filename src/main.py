"""Pipeline principal GameTracker : Extract, Transform, Load."""
from src.config import Config
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.database import database_connection


def main():
    """Exécute le pipeline ETL complet."""

    # 1. Extract
    print("  Extraction des données...")
    players_raw = extract(f"{Config.DATA_DIR}/Players.csv")
    scores_raw = extract(f"{Config.DATA_DIR}/Scores.csv")

    # 2. Transform
    print("  Transformation des données...")
    players_clean = transform_players(players_raw)
    valid_ids = players_clean['player_id'].tolist()
    scores_clean = transform_scores(scores_raw, valid_ids)

    # 3. Load
    print("  Chargement en base de données...")
    with database_connection() as conn:
        load_players(players_clean, conn)
        load_scores(scores_clean, conn)


if __name__ == "__main__":
    main()

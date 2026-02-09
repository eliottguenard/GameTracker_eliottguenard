"""Module ETL : Load."""
import pandas as pd
import numpy as np


def _clean_value(val):
    """Convertit les valeurs NaN/NaT de pandas en None pour MySQL."""
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, pd.Timestamp):
        if pd.isna(val):
            return None
        return val.strftime('%Y-%m-%d %H:%M:%S')
    if pd.isna(val):
        return None
    return val


def load_players(df: pd.DataFrame, conn) -> None:
    """Charge les joueurs en base avec ON DUPLICATE KEY UPDATE.

    Args:
        df: DataFrame des joueurs nettoyés.
        conn: Connexion MySQL active.
    """
    cursor = conn.cursor()

    query = """
        INSERT INTO players (player_id, username, email, registration_date, country, level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            username = VALUES(username),
            email = VALUES(email),
            registration_date = VALUES(registration_date),
            country = VALUES(country),
            level = VALUES(level)
    """

    count = 0
    for _, row in df.iterrows():
        values = (
            _clean_value(row['player_id']),
            _clean_value(row['username']),
            _clean_value(row['email']),
            _clean_value(row['registration_date']),
            _clean_value(row['country']),
            _clean_value(row['level']),
        )
        cursor.execute(query, values)
        count += 1

    conn.commit()
    print(f"Chargé {count} joueurs en base")
    cursor.close()


def load_scores(df: pd.DataFrame, conn) -> None:
    """Charge les scores en base avec ON DUPLICATE KEY UPDATE.

    Args:
        df: DataFrame des scores nettoyés.
        conn: Connexion MySQL active.
    """
    cursor = conn.cursor()

    query = """
        INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            player_id = VALUES(player_id),
            game = VALUES(game),
            score = VALUES(score),
            duration_minutes = VALUES(duration_minutes),
            played_at = VALUES(played_at),
            platform = VALUES(platform)
    """

    count = 0
    for _, row in df.iterrows():
        values = (
            _clean_value(row['score_id']),
            _clean_value(row['player_id']),
            _clean_value(row['game']),
            _clean_value(row['score']),
            _clean_value(row['duration_minutes']),
            _clean_value(row['played_at']),
            _clean_value(row['platform']),
        )
        cursor.execute(query, values)
        count += 1

    conn.commit()
    print(f"Chargé {count} scores en base")
    cursor.close()

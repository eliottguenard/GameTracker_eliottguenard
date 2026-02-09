"""Module ETL : Transform."""
import pandas as pd


def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme et nettoie les données des joeurs.

    Args:
        df: DataFrame brut des personnes.
    Returns:
        DataFrame nettoyé.
    """
    df = df.copy()

    # Supprimer les doublons sur player_id
    df = df.drop_duplicates(subset=['player_id'])

    # Nettoyer les espaces des username
    df['username'] = df['username'].str.strip()

    # il reste des doublons dedans, on peut nettoyer ça sur le username étant donné qu'il n'est jamais vide

    df = df.drop_duplicates(subset=['username'])

    # Convertir les dates
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')

    # Remplacer NaT par None pour MySQL
    df['registration_date'] = df['registration_date'].astype(object).where(df['registration_date'].notna(), None)

    # Nettoyer les emails invalides
    df['email'] = df['email'].where(df['email'].str.contains('@', na=False), None)

    print(f"Transformé {len(df)} joueurs")
    return df

def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """Transforme et nettoie les données des scores.

    Args:
        df: DataFrame brut des scores.
        valid_player_ids: Liste des player_id valides issus des joueurs nettoyés.
    Returns:
        DataFrame nettoyé.
    """
    df = df.copy()

    # Supprimer les doublons sur score_id
    df = df.drop_duplicates(subset=['score_id'])

    # Convertir les dates
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')

    # Convertir les scores en numérique
    df['score'] = pd.to_numeric(df['score'], errors='coerce')

    # Supprimer les lignes avec un score négatif ou nul
    df = df[df['score'] > 0]

    # Supprimer les scores dont le player_id n'est pas dans valid_player_ids
    df = df[df['player_id'].isin(valid_player_ids)]

    print(f"Transformé {len(df)} scores")
    return df
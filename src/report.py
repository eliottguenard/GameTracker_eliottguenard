"""Module de génération de rapport."""
from datetime import datetime
from src.database import database_connection


def generate_report(output_path: str = "/app/output/rapport.txt") -> None:
    """Génère un rapport de synthèse à partir des données en base.

    Args:
        output_path: Chemin du fichier de rapport en sortie.
    """
    with database_connection() as conn:
        cursor = conn.cursor()

        # 1. Statistiques générales
        cursor.execute("SELECT COUNT(*) FROM players")
        nb_joueurs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scores")
        nb_scores = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT game) FROM scores")
        nb_jeux = cursor.fetchone()[0]

        # 2. Top 5 des meilleurs scores
        cursor.execute("""
            SELECT p.username, s.game, s.score
            FROM scores s
            JOIN players p ON s.player_id = p.player_id
            ORDER BY s.score DESC
            LIMIT 5
        """)
        top5 = cursor.fetchall()

        # 3. Score moyen par jeu
        cursor.execute("""
            SELECT game, ROUND(AVG(score), 1) as avg_score
            FROM scores
            GROUP BY game
            ORDER BY avg_score DESC
        """)
        score_moyen = cursor.fetchall()

        # 4. Répartition des joueurs par pays
        cursor.execute("""
            SELECT country, COUNT(*) as nb
            FROM players
            GROUP BY country
            ORDER BY nb DESC
        """)
        joueurs_pays = cursor.fetchall()

        # 5. Répartition des sessions par plateforme
        cursor.execute("""
            SELECT platform, COUNT(*) as nb
            FROM scores
            GROUP BY platform
            ORDER BY nb DESC
        """)
        sessions_plateforme = cursor.fetchall()

        cursor.close()

    # Écriture du rapport
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 52 + "\n")
        f.write("GAMETRACKER - Rapport de synthese\n")
        f.write(f"Genere le : {now}\n")
        f.write("=" * 52 + "\n\n")

        # Statistiques générales
        f.write("--- Statistiques generales ---\n")
        f.write(f"Nombre de joueurs : {nb_joueurs}\n")
        f.write(f"Nombre de scores  : {nb_scores}\n")
        f.write(f"Nombre de jeux    : {nb_jeux}\n\n")

        # Top 5
        f.write("--- Top 5 des meilleurs scores ---\n")
        for i, (username, game, score) in enumerate(top5, 1):
            f.write(f"{i}. {username} | {game} | {score}\n")
        f.write("\n")

        # Score moyen par jeu
        f.write("--- Score moyen par jeu ---\n")
        for game, avg_score in score_moyen:
            f.write(f"{game} : {avg_score}\n")
        f.write("\n")

        # Joueurs par pays
        f.write("--- Joueurs par pays ---\n")
        for country, nb in joueurs_pays:
            f.write(f"{country} : {nb}\n")
        f.write("\n")

        # Sessions par plateforme
        f.write("--- Sessions par plateforme ---\n")
        for platform, nb in sessions_plateforme:
            f.write(f"{platform} : {nb}\n")
        f.write("\n")

        f.write("=" * 52 + "\n")

    print(f"Rapport généré dans {output_path}")

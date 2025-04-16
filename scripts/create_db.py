import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def create_database():
    """Crée la base de données si elle n'existe pas"""
    # Utiliser les variables d'environnement ou des valeurs par défaut
    db_name = "medical_assistant"
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    
    # Créer une connexion à PostgreSQL sans spécifier de base de données
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la base de données existe
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"Base de données {db_name} créée avec succès!")
        else:
            print(f"La base de données {db_name} existe déjà.")
            
    except Exception as e:
        print(f"Erreur lors de la création de la base de données: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_database() 
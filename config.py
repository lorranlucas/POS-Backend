from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

print("Arquivo .env carregado de:", os.path.abspath(dotenv_path))  # Diagnóstico

class Config:
    # Pasta para uploads
    UPLOAD_FOLDER = 'uploads/'  # Diretório para salvar imagens

    # Variáveis do MySQL
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

    # URI do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

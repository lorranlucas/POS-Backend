from dotenv import load_dotenv
import os

# Carregar as variáveis do .env
dotenv_path = os.path.join(os.getcwd(), '.env')

# Carregar o arquivo .env novamente
load_dotenv(dotenv_path=dotenv_path, override=True)

# Verificar onde o arquivo .env está sendo carregado
print("Arquivo .env carregado de:", os.path.abspath(dotenv_path))

# Variáveis de ambiente
class Config:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

    # Verificar se as variáveis estão sendo carregadas corretamente
    print("MYSQL_USER:", MYSQL_USER)
    print("MYSQL_PASSWORD:", MYSQL_PASSWORD)
    print("MYSQL_HOST:", MYSQL_HOST)
    print("MYSQL_DATABASE:", MYSQL_DATABASE)

    if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE]):
        raise ValueError("Faltam variáveis de ambiente para conexão com o banco de dados.")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

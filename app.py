from flask import Flask
from config import Config
from extensions import db, migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Carregar configurações
    app.config.from_object(Config)

    # Inicializar as extensões
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar Blueprints
    from routes.categoria_routes import categoria_bp
    from routes.setor_routes import setor_bp
    from routes.fornecedor_routes import fornecedor_bp
    from routes.produto_routes import produto_bp

    app.register_blueprint(categoria_bp, url_prefix='/api')
    app.register_blueprint(setor_bp, url_prefix='/api')
    app.register_blueprint(fornecedor_bp, url_prefix='/api')
    app.register_blueprint(produto_bp, url_prefix='/api')

    return app



# Executar a aplicação
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'notes.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-this')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # import models and create DB
        from models import User, Note
        db.create_all()

    # register blueprints
    from auth import auth_bp
    from routes import notes_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

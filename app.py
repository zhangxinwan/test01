from flask import Flask, request, jsonify, render_template
from models import db, User
from sqlalchemy.exc import IntegrityError


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    # default config
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    if config:
        app.config.update(config)

    db.init_app(app)


    @app.route('/users', methods=['GET'])
    def list_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])


    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        u = User.query.get_or_404(user_id)
        return jsonify(u.to_dict())


    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        if not name or not email:
            return jsonify({'error': 'name and email are required'}), 400
        u = User(name=name, email=email)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'email already exists'}), 409
        return jsonify(u.to_dict()), 201


    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        u = User.query.get_or_404(user_id)
        data = request.get_json() or {}
        u.name = data.get('name', u.name)
        u.email = data.get('email', u.email)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'email already exists'}), 409
        return jsonify(u.to_dict())


    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        u = User.query.get_or_404(user_id)
        db.session.delete(u)
        db.session.commit()
        return ('', 204)


    @app.route('/')
    def index():
        return jsonify({'message': '用户管理系统: 使用 /users 进行操作'})

    @app.route('/ui')
    def ui():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

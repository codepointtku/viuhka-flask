from app.utils import create, register_extensions
from app.utils.extensions.database import module as connector
from sys import argv, exit

if __name__ == '__main__':
    app = create()
    if '--create' in argv:
        with app.app_context():
            connector.create_all()
            connector.session.commit()
        print('Created database')
        exit(2)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', False),
        load_dotenv=False
    )

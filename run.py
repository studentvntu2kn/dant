from app import db, create_app
from app.models import User

app = create_app()

if __name__ == '__main__':
    app.run()

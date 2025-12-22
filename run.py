from app.config import create_app
import os

read_env = os.environ.get('FLASK_ENV', 'development')
app = create_app(read_env)

if __name__ == "__main__":
    app.run(debug=True)

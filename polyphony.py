from polyphony_app.app import create_app, db
from polyphony_app import users

app = application = create_app()

if __name__ == '__main__':
    app.run(host='192.168.1.33', port=9000, debug=True, load_dotenv=False)

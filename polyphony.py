from polifonia_app.app import create_app

app = application = create_app()

if __name__ == '__main__':
    host = 'localhost'
    host = '192.168.1.34'
    app.run(host=host, port=9000, debug=True, load_dotenv=False)

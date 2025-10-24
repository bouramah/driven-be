from app import Application

# Créer l'application Flask
application = Application()
app = application.get_app()

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

from puppies import app


if __name__ == "__main__":
    app.debug = False
    
    #default configs are located in config.py
    app.config.from_object('config')
    app.run(app.config.get('SERVER_NAME'),
            app.config.get('SERVER_PORT')
           )

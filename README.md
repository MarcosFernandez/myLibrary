# myLibrary REST API

Flask application just for learning basics about REST API web services.

Implements a dummy database to handle authors, languages, editorials and books. 

Database model is conceived just for learning proposes, it can not be considered as a reference for production purposes.

myLibrary shows how to develop a complete REST API service, test it and document it through [swagger](https://swagger.io).

myLibrary REST API has been inspired by Miguel Grinberg [Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). His excellent code can be found [here](https://github.com/miguelgrinberg/microblog/tree/master).

## Installation

### 0. Download code from github

```sh
git clone -b master https://github.com/MarcosFernandez/myLibrary.git
```

### 1. Install virtualenv
 
```sh
pip3 install virtualenv
```

### 2. Activate Virtual environment 

```sh
virtualenv venv
source venv/bin/activate
```

### 3. Install Flask

```sh
(venv) pip3 install Flask
```

### 4. Install SQL Alchemy and SQLLite 

```sh
(venv) pip3 install flask-sqlalchemy
```

### 4.1 Install Database Migrations

```sh
(venv) pip3 install flask-migrate
```

### 5. Install Flask Login

```sh
(venv) pip3 install flask-login
```

### 6. JWT

```sh
(venv) pip3 install PyJWT==1.5.3
```

### 7. HTTP Autho

```sh
(venv) pip3 install Flask-HTTPAuth==4.0.0
```

### 8. SET FLASK ENVIRONMENT APP

```sh
(venv) pip3 install python-dotenv
echo "FLASK_APP=myLibrary.py" > .flaskenv
```

### 9. RUN DEBUG SERVER

```sh
(venv) flask run
```

### 10. Setup Database

### 10.1 Create migration repository

```sh
(venv) flask db init
```

### 10.2 First Database Migration

```sh
(venv) flask db migrate -m "First Migration"
```

### 10.3 Apply the changes to the database

```sh
(venv) flask db upgrade
```

### 11. Create First User From Shell

```sh
userflask@flaskserver:~/myLibrary$ flask shell
Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
[GCC 8.4.0] on linux
App: app [production]
Instance: /home/userflask/myLibrary/instance
>>> from app.models import User
>>> from app import db
>>> user = User()
>>> user.username = 'userflask'
>>> user.set_password('USERPASSWORD')
>>> db.session.add(user)
>>> db.session.commit()
>>> 
now exiting InteractiveConsole...
```

## Usage

### 1. GET REST API TOKEN

```sh
curl -X POST -u userflask:userflask "http://127.0.0.1:5000/api/tokens""
{"token" : "TOKENUSERFLASK"}
```

### 2. GET AUTHORS

```sh
curl -X GET "http://127.0.0.1:5000/api/authors" -H "Authorization":"Bearer TOKENUSERFLASK"
```

### 3. CREATE AUTHOR

```sh
curl -X POST "http://127.0.0.1:5000/api/author" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"name":"Bertrand Russell", "country":"England"}'
```

### 4. GET GIVEN AUTHOR

```sh
curl -X GET "http://127.0.0.1:5000/api/author/Bertrand%20Russell" -H "Authorization":"Bearer TOKENUSERFLASK"
{"_links":{"self":"/api/author/Bertrand%20Russell"},"country":"England","id":1,"name":"Bertrand Russell"}
```

### 5. UPDATE AUTHOR

```sh
curl -X PUT "http://127.0.0.1:5000/api/author/Manuel%20Garrido" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"name":"Manolo Garrido"}'
```

### 6. DELETE AUTHOR

```sh
curl -X DELETE "http://127.0.0.1:5000/api/author/J.R.R%20Tolkien" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' 
{"success":true}
```
 
### 7. CREATE LANGUAGE

```sh
curl -X POST "http://127.0.0.1:5000/api/language" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"name":"English"}'
```

### 8. GET ALL LANGUAGES

```sh
curl -X GET "http://127.0.0.1:5000/api/languages" -H "Authorization":"Bearer TOKENUSERFLASK" 
```

### 9. POST LANGUAGES

```sh
curl -X PUT "http://127.0.0.1:5000/api/language/English" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"name":"England"}'
```

### 10. DELETE LANGUAGE

```sh
curl -X DELETE "http://127.0.0.1:5000/api/language/Italian" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' 
{"success":true}
```

### 11. ADD EDITORIAL

```sh
curl -X POST "http://127.0.0.1:5000/api/editorial" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"name":"Simon&Schuster", "country":"USA"}'
```

### 12. GET ALL EDITORIALS

```sh
curl -X GET "http://127.0.0.1:5000/api/editorials" -H "Authorization":"Bearer TOKENUSERFLASK" 
```

### 13. POST EDITORIAL

```sh
curl -X PUT "http://127.0.0.1:5000/api/editorial/Simon%26Schuster" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"country":"England"}'
```

### 14. DELETE EDITORIAL

```sh
curl -X DELETE "http://127.0.0.1:5000/api/editorial/Plaza%26Janes" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json'
```

### 15. ADD BOOK

```sh
curl -X POST "http://127.0.0.1:5000/api/book" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json' -d '{"title":"The problems of Philosophy", "author":"Bertrand Russell","language":"English","editorial":"Simon&Schuster","location":"London","status":"NOT PRESENT"}'
```

### 16. GET A GIVEN BOOK

```sh
 curl -X GET "http://127.0.0.1:5000/api/book/German%20Social%20Democracy" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json'
{"_links":{"author":"/api/author/Bertrand%20Russell","editorial":"/api/editorial/Simon%26Schuster","language":"/api/language/English","self":"/api/book/German%20Social%20Democracy"},"author":"Bertrand Russell","editorial":"Simon&Schuster","id":2,"language":"English","location":"London","status":"NOT PRESENT","title":"German Social Democracy"}
```

### 17. GET ALL BOOKS

```sh
curl -X GET "http://127.0.0.1:5000/api/books" -H "Authorization":"Bearer TOKENUSERFLASK" -H 'Content-Type: application/json'
```

## Run REST APIs Tests

Runs unit test on all REST APIs endpoints.

```sh
python -m unittest tests/test_api_endpoint.py
```

## Check Swagger Documentation

### 1. Install swagger package

```sh
(venv) pip3 install flask_swagger_ui
```

### 2. Show Swagger Documentation

```sh
(venv) flask run
```

Open in browser **http://127.0.0.1:5000/swagger/**
Check swagger JSON: **http://127.0.0.1:5000/static/swagger.json**

## License

GNU General Public License **gpl-3.0**

## Developers

* Marcos Fernandez-Callejo - marcos.callejo@hotmail.com

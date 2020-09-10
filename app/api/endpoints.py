from flask import jsonify, request, url_for
from app import db
from app.models import Author, Language, Editorial, Book 
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/author/<string:name>', methods=['GET'])
@token_auth.login_required
def get_author(name):
    author = Author.query.filter_by(name=name)
    if author.count() > 0:
        return jsonify(Author.query.filter_by(name=name).first().to_dict())
    else:
        return bad_request(f'Author {name} does not exists at database')

@bp.route('/authors', methods=['GET'])
@token_auth.login_required
def get_authors():
    page = request.args.get('page', 1,type=int)
    per_page = min(request.args.get('per_page',10,type=int),100)
    data = Author.to_collection_dict(Author.query,page,per_page,'api.get_authors')
    return jsonify(data)

@bp.route('/language/<string:name>', methods=['GET'])
@token_auth.login_required
def get_language(name):
    language = Language.query.filter_by(name=name)
    if language.count() > 0:
        return jsonify(language.first().to_dict())
    else:
        return bad_request(f'Language {language} does not exists at database')

@bp.route('/languages', methods=['GET'])
@token_auth.login_required
def get_languages():
    page = request.args.get('page',1,type=int)
    per_page = min(request.args.get('per_page',10,type=int),100)
    data = Language.to_collection_dict(Language.query,page,per_page,'api.get_languages')
    return jsonify(data)

@bp.route('/editorial/<string:name>', methods=['GET'])
@token_auth.login_required
def get_editorial(name):
    editorial = Editorial.query.filter_by(name=name)
    if editorial.count() > 0:
        return jsonify(editorial.first().to_dict())
    else:
        return bad_request(f'Editorial {name} does not exists at database')

@bp.route('/editorials', methods=['GET'])
@token_auth.login_required
def get_editorials():
    page = request.args.get('page',1,type=int)
    per_page = min(request.args.get('per_page',10,type=int),100)
    data = Editorial.to_collection_dict(Editorial.query,page,per_page,'api.get_editorials')
    return jsonify(data)

@bp.route('/book/<string:title>', methods=['GET'])
@token_auth.login_required
def get_book(title):
    book = Book.query.filter_by(title=title)
    if book.count() > 0:
        return jsonify(book.first().to_dict())
    else:
        return bad_request(f'Book title {title} does not exists at database')

@bp.route('/books', methods=['GET'])
@token_auth.login_required
def get_books():
    page = request.args.get('page',1,type=int)
    per_page = min (request.args.get('per_page',10,type=int),100)
    data = Book.to_collection_dict(Book.query, page,per_page,'api.get_books')
    return jsonify(data)

@bp.route('/author', methods=['POST'])
@token_auth.login_required
def create_author():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if Author.query.filter_by(name=data["name"]).first():
        return bad_request(f'Author {data["name"]} already present at database')
    author = Author()
    author.from_dict(data=data)
    db.session.add(author)
    db.session.commit()
    response = jsonify(author.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_author', name=author.name)
    return response

@bp.route('/author/<string:name>', methods=['PUT'])
@token_auth.login_required
def update_author(name):
    authors = Author.query.filter_by(name=name)
    if authors.count() > 0:
        author = authors.first()
        data = request.get_json() or {}
        author.from_dict(data)
        db.session.commit()
        return jsonify(author.to_dict())
    else:
        return bad_request(f'Author {name} does not exists at database')

@bp.route('/author/<string:name>', methods=['DELETE'])
@token_auth.login_required
def delete_author(name):
    authors = Author.query.filter_by(name=name)
    if authors.count() > 0:
        author = authors.first()
        db.session.delete(author)
        db.session.commit()
        return jsonify(success=True)
    else:
        return bad_request(f'Author {name} does not exists at database')

@bp.route('/language', methods=['POST'])
@token_auth.login_required
def create_language():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if Language.query.filter_by(name=data["name"]).first():
        return bad_request(f'Language {data["name"]} already present at database')
    language = Language()
    language.from_dict(data=data)
    db.session.add(language)
    db.session.commit()
    response = jsonify(language.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_language', name=language.name)
    return response

@bp.route('/language/<string:name>', methods=['PUT'])
@token_auth.login_required
def update_language(name):
    languages = Language.query.filter_by(name=name)
    if languages.count() > 0:
        language = languages.first()
        data = request.get_json() or {}
        language.from_dict(data)
        db.session.commit()
        return jsonify(language.to_dict())
    else:
        return bad_request(f'Language {name} does not exists at database')

@bp.route('/language/<string:name>', methods=['DELETE'])
@token_auth.login_required
def delete_language(name):
    languages = Language.query.filter_by(name=name)
    if languages.count() > 0:
        language = languages.first()
        db.session.delete(language)
        db.session.commit()
        return jsonify(success=True)
    else:
        return bad_request(f'Language {name} does not exists at database')

@bp.route('/editorial', methods=['POST'])
@token_auth.login_required
def create_editorial():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if Editorial.query.filter_by(name=data["name"]).first():
        return bad_request(f'Editorial {data["name"]} already present at database')
    editorial = Editorial()
    editorial.from_dict(data=data)
    db.session.add(editorial)
    db.session.commit()
    response = jsonify(editorial.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_editorial', name=editorial.name)
    return response

@bp.route('/editorial/<string:name>', methods=['PUT'])
@token_auth.login_required
def update_editorial(name):
    editorials = Editorial.query.filter_by(name=name)
    if editorials.count() > 0:
        editorial = editorials.first()
        data = request.get_json() or {}
        editorial.from_dict(data)
        db.session.commit()
        return jsonify(editorial.to_dict())
    else:
        return bad_request(f'Editorial {name} does not exists at database')

@bp.route('/editorial/<string:name>', methods=['DELETE'])
@token_auth.login_required
def delete_editorial(name):
    editorials = Editorial.query.filter_by(name=name)
    if editorials.count() > 0:
        editorial = editorials.first()
        db.session.delete(editorial)
        db.session.commit()
        return jsonify(success=True)
    else:
        return bad_request(f'Editorial {name} does not exists at database')

@bp.route('/book', methods=['POST'])
@token_auth.login_required
def create_book():
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title field')
    if Book.query.filter_by(title=data["title"]).first():
        return bad_request(f'Title {data["title"]} already present at database')
    book = Book()
    book.from_dict(data)
    db.session.add(book)
    db.session.commit()
    response = jsonify(book.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_book', title=book.title)
    return response

@bp.route('/book/<string:title>', methods=['PUT'])
@token_auth.login_required
def update_book(title):
    books = Book.query.filter_by(title=title)
    if books.count() > 0:
        book = books.first()
        data = request.get_json() or {}
        book.from_dict(data)
        db.session.commit()
        return jsonify(book.to_dict())
    else:
        return bad_request(f'Book {title} does not exists at database')

@bp.route('/book/<string:title>', methods=['DELETE'])
@token_auth.login_required
def delete_book(title):
    books = Book.query.filter_by(title=title)
    if books.count() > 0:
        book = books.first()
        db.session.delete(book)
        db.session.commit()
        return jsonify(success=True)
    else:
        return bad_request(f'Book {title} does not exists at database')

#2.1 GET All Authors
#2.2 POST New Author/s
#2.3 GET All Languages
#2.4 POST New Language/s
#2.5 GET All Editorial
#2.6 POST New Editorial/s
#2.7 GET All Books
#2.13 POST New Book/s
#2.8 GET Book By Author
#2.9 GET Books By Language
#2.10 GET Books By Editorial
#2.11 GET Book By Status
#2.12 GET Books by Location


#https://github.com/miguelgrinberg/microblog/blob/v0.23/app/api/users.py








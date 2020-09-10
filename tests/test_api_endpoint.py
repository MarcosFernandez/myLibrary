import unittest
import json
import os
import io

from app import create_app, db
from app.models import User, Author, Language, Editorial, Book

basedir = os.path.abspath(os.path.dirname(__file__))

class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'test.db')

class ApiTest(unittest.TestCase):
    """Class API Test, check All API endspoint"""
 
    def set_up_user_test(self):
        """Create user for testing and set its Authentcation Token"""
        user_test = User(username='test')
        user_test.set_password('test')
        db.session.add(user_test)
        db.session.commit()
        self.token = user_test.get_token()
    
    def setUp(self):
        """Set up test fixtures"""
        print ('### Setting up flask server ###')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.api = self.app.test_client()
        self.set_up_user_test()
        self.content = 'application/json'
        self.headers = {"Authorization":f'Bearer {self.token}'}

    def tearDown(self):
        # Delete Database collections after the test is complete
        print ('### Tearing Down the flask server ###')
        db.session.remove()
        db.drop_all()

    def test_author_endpoints(self):
        #0.Set url
        url = '/api/author'

        #1. Author Creation
        payload = json.dumps({"name":"Bertrand Russell", "country":"USA"})
        #1.2 Response
        response = self.api.post(url,headers=self.headers,content_type=self.content, data=payload)
        #1.3. Check Response
        self.assertEqual(201, response.status_code)

        #2. Author Update
        payload = json.dumps({"country":"England"})
        #2.2 Response
        response = self.api.put(f'{url}/Bertrand%20Russell',headers=self.headers,content_type=self.content,data=payload)
        #2.3 Check Response
        self.assertEqual(200,response.status_code)

        #3. Get Author
        #3.1 Response
        response = self.api.get(f'{url}/Bertrand%20Russell',headers=self.headers)
        #3.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("Bertrand Russell",response.json["name"])
        self.assertEqual("England", response.json["country"])

        #4. Get All Authors
        author = Author()
        author.name = "Miguel de Unamuno"
        author.country = "Spain"
        db.session.add(author)
        db.session.commit()
        #4.1 Response
        response = self.api.get(f'{url}s',headers=self.headers)
        #4.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("Miguel de Unamuno",response.json["items"][1]["name"])
        self.assertEqual("Spain", response.json["items"][1]["country"])

    def test_language_endpoints(self):
        #0.Set url
        url = '/api/language'

        #1. Language Creation
        payload = json.dumps({"name":"British"})
        #1.2 Response
        response = self.api.post(url,headers=self.headers,content_type=self.content, data=payload)
        #1.3. Check Response
        self.assertEqual(201, response.status_code)

        #2. Language Update
        payload = json.dumps({"name":"English"})
        #2.2 Response
        response = self.api.put(f'{url}/British',headers=self.headers,content_type=self.content,data=payload)
        #2.3 Check Response
        self.assertEqual(200,response.status_code)

        #3. Get Language
        #3.1 Response
        response = self.api.get(f'{url}/English',headers=self.headers)
        #3.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("English",response.json["name"])

        #4. Get All Languages
        language = Language()
        language.name = "Spanish"
        db.session.add(language)
        db.session.commit()
        #4.1 Response
        response = self.api.get(f'{url}s',headers=self.headers)
        #4.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("Spanish",response.json["items"][1]["name"])

    def test_editorial_endpoint(self):
        #0.Set url
        url = '/api/editorial'

        #1. Editorial Creation
        payload = json.dumps({"name":"RoutledgeClassics", "country":"England"})

        #1.2 Response
        response = self.api.post(url,headers=self.headers,content_type=self.content, data=payload)
        #1.3. Check Response
        self.assertEqual(201, response.status_code)

        #2. Editorial Update
        payload = json.dumps({"country":"USA"})
        #2.2 Response
        response = self.api.put(f'{url}/RoutledgeClassics',headers=self.headers,content_type=self.content,data=payload)
        #2.3 Check Response
        self.assertEqual(200,response.status_code)

        #3. Get Editorial
        #3.1 Response
        response = self.api.get(f'{url}/RoutledgeClassics',headers=self.headers)
        #3.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("RoutledgeClassics",response.json["name"])

        #4. Get All Editorials
        editorial = Editorial()
        editorial.name = "LaCampana"
        editorial.country = "Spain"
        db.session.add(editorial)
        db.session.commit()
        #4.1 Response
        response = self.api.get(f'{url}s',headers=self.headers)
        #4.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("LaCampana",response.json["items"][1]["name"])

    def test_book_endpoint(self):
        #0.Set url
        url = '/api/book'
        #0.1 Create Author, Language, Editorial
        #0.1.1 Author
        author = Author()
        author.name = "Bertrand Russell"
        author.country = "England"
        db.session.add(author)
        #0.1.2 Language
        language = Language()
        language.name = "English"
        db.session.add(language)
        #0.1.3 Editorial
        editorial = Editorial()
        editorial.name = "Cambridge"
        editorial.country = "England"
        db.session.add(editorial)
        #0.1.4 Commit to database
        db.session.commit()

        #1. Book Creation
        payload = json.dumps({
                              "title":"Principia Mathematica", 
                              "author":"Bertrand Russell",
                              "language":"English",
                              "editorial":"Cambridge",
                              "location":"Santa Coloma de Cervello",
                              "status":"Available"
        })
        #1.2 Response
        response = self.api.post(url,headers=self.headers,content_type=self.content, data=payload)
        #1.3. Check Response
        self.assertEqual(201, response.status_code)

        #2. Book Update
        payload = json.dumps({"title":"The Principles of Mathematics"})
        #2.2 Response
        response = self.api.put(f'{url}/Principia%20Mathematica',headers=self.headers,content_type=self.content,data=payload)
        #2.3 Check Response
        self.assertEqual(200,response.status_code)

        #3. Get Book
        #3.1 Response
        response = self.api.get(f'{url}/The%20Principles%20of%20Mathematics',headers=self.headers)
        #3.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("The Principles of Mathematics",response.json["title"])

        #4. Get All Books
        book = Book()
        book.title = "Principia Mathematica"
        book.location = "Santa Coloma de Cervello"
        book.status = "Booked"
        book.author = Author.query.filter_by(name="Bertrand Russell").first()
        book.language = Language.query.filter_by(name="English").first()
        book.editorial = Editorial.query.filter_by(name="Cambridge").first()
        db.session.add(book)
        db.session.commit()
        #4.1 Response
        response = self.api.get(f'{url}s',headers=self.headers)
        #4.2 Check Response
        self.assertEqual(200,response.status_code)
        self.assertEqual("Principia Mathematica",response.json["items"][1]["title"])


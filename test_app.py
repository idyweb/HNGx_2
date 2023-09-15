import unittest
import json
from app import app, db, Person

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client and create a test database
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up the test database after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_person(self):
        # Test adding a person
        data = {'name': 'John Doe'}
        response = self.app.post('/api', json=data)
        self.assertEqual(response.status_code, 201)

    def test_add_person_duplicate_name(self):
        # Test adding a person with a duplicate name
        data = {'name': 'John Doe'}
        self.app.post('/api', json=data)  # Add the first person
        response = self.app.post('/api', json=data)  # Try to add the same person again
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['error'], 'Name already exists')

    def test_get_all_persons(self):
        # Test retrieving all persons
        response = self.app.get('/api')
        self.assertEqual(response.status_code, 200)

    def test_get_person(self):
        # Test retrieving a specific person by ID
        person = Person(name='John Doe')
        with app.app_context():
            db.session.add(person)
            db.session.commit()
            response = self.app.get(f'/api/{person.id}')
            self.assertEqual(response.status_code, 200)

    def test_get_person_not_found(self):
        # Test retrieving a person that does not exist
        response = self.app.get('/api/999')  # Assuming ID 999 does not exist
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['error'], 'Person not found')

    def test_update_person(self):
        # Test updating a specific person by ID
        person = Person(name='John Doe')
        db.session.add(person)
        db.session.commit()
        updated_data = {'name': 'Jane Doe'}
        response = self.app.put(f'/api/{person.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        updated_person = Person.query.get(person.id)
        self.assertEqual(updated_person.name, 'Jane Doe')

    def test_update_person_not_found(self):
        # Test updating a person that does not exist
        updated_data = {'name': 'Jane Doe'}
        response = self.app.put('/api/999', json=updated_data)  # Assuming ID 999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_update_person_missing_name(self):
        # Test updating a person with missing name
        person = Person(name='John Doe')
        db.session.add(person)
        db.session.commit()
        updated_data = {}  # Missing 'name' key
        response = self.app.put(f'/api/{person.id}', json=updated_data)
        self.assertEqual(response.status_code, 400)

    def test_delete_person(self):
        # Test deleting a specific person by ID
        person = Person(name='John Doe')
        db.session.add(person)
        db.session.commit()
        response = self.app.delete(f'/api/{person.id}')
        self.assertEqual(response.status_code, 200)
        deleted_person = Person.query.get(person.id)
        self.assertIsNone(deleted_person)

    def test_delete_person_not_found(self):
        # Test deleting a person that does not exist
        response = self.app.delete('/api/999')  # Assuming ID 999 does not exist
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()

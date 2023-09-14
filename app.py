from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
db.init_app(app)
migrate = Migrate(app, db)

#define person model

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    

    def to_json(self):
        return{
            'id': self.id,
            'name': self.name
        }
    __table_args__ = {'extend_existing':True}
    
with app.app_context():
    db.create_all()


#api routes
@app.route('/api', methods=['POST'])
def add_person():
    data = request.get_json()
    if 'name' in data:
        name = data['name']
        new_person = Person(name=data['name'])
        # Check if a person with the same name already exists
        existing_person = Person.query.filter_by(name=name).first()

        if existing_person:
            return jsonify({'error': 'Name already exists'}), 400
        db.session.add(new_person)
        db.session.commit()
        return jsonify({'message': 'Person added successfully'}), 201
    else:
        return jsonify({'error': 'Please add name'}), 400
    

# Retrieve all persons
@app.route('/api', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    return jsonify([person.to_json() for person in persons])

# Retrieve a specific person by ID
@app.route('/api/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person:
        return jsonify(person.to_json())
    else:
        return jsonify({'error': 'Person not found'}), 404

# Update a person by ID
@app.route('/api/<int:id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get(id)
    if person:
        data = request.get_json()
        if 'name' in data:
            person.name = data['name']
            db.session.commit()
            return jsonify({'message': 'Person updated successfully'})
        else:
            return jsonify({'error': 'Name is required'}), 400
    else:
        return jsonify({'error': 'Person not found'}), 404

# Delete a person by ID
@app.route('/api/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted successfully'})
    else:
        return jsonify({'error': 'Person not found'}), 404

        

if __name__ == '__main__':
    
    app.run(debug=True)
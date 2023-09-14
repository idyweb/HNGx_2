## API Endpoints
### Add a Person

Endpoint: /api
Method: POST
Description: Add a new person to the database.
Request Body: JSON object with a name field.
Response: Success (201 Created) or Error (400 Bad Request).


### Get All Persons

Endpoint: /api
Method: GET
Description: Retrieve a list of all persons in the database.
Response: JSON array of person objects.


### Get a Specific Person

Endpoint: /api/<int:id>
Method: GET
Description: Retrieve a specific person by their ID.
Response: JSON object of the person or an error message.


### Update a Person

Endpoint: /api/<int:id>
Method: PUT
Description: Update a person's information by their ID.
Request Body: JSON object with a name field.
Response: Success (200 OK) or Error (400 Bad Request).


### Delete a Person

Endpoint: /api/<int:id>
Method: DELETE
Description: Delete a person by their ID.
Response: Success (200 OK) or Error (404 Not Found).

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory example data structure to simulate a database
users = {
    1: {'name': 'John Doe', 'email': 'john@example.com'},
    2: {'name': 'Jane Smith', 'email': 'jane@example.com'}
}

# GET method: Retrieve a list of users or a specific user by ID
@app.route('/users', methods=['GET'])
def get_users():
    """
    Handle GET requests to retrieve all users.
    If a user ID is provided in the query string, return that specific user.
    Example: /users?user_id=1
    """
    user_id = request.args.get('user_id')
    if user_id:
        user = users.get(int(user_id))
        if user:
            return jsonify(user), 200  # 200 OK if user is found
        return "User not found", 404  # 404 Not Found if user does not exist
    return jsonify(users), 200  # Return all users if no specific ID is requested

# POST method: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    """
    Handle POST requests to create a new user.
    Expecting JSON data with 'name' and 'email' fields.
    """
    new_user = request.json
    if 'name' in new_user and 'email' in new_user:
        new_id = max(users.keys()) + 1  # Generate a new ID
        users[new_id] = new_user  # Add the new user to the data structure
        return jsonify(new_user), 201  # 201 Created if the user is successfully added
    return "Invalid data", 400  # 400 Bad Request if required fields are missing

# PUT method: Update an entire user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Handle PUT requests to update an existing user by ID.
    The PUT method replaces the entire user resource with new data.
    """
    updated_user = request.json
    if user_id in users:
        if 'name' in updated_user and 'email' in updated_user:
            users[user_id] = updated_user  # Replace the existing user data
            return jsonify(updated_user), 200  # 200 OK if update is successful
        return "Invalid data", 400  # 400 Bad Request if required fields are missing
    return "User not found", 404  # 404 Not Found if the user does not exist

# PATCH method: Partially update a user by ID
@app.route('/users/<int:user_id>', methods=['PATCH'])
def partial_update_user(user_id):
    """
    Handle PATCH requests to partially update an existing user by ID.
    Only the fields provided in the request are updated.
    """
    if user_id in users:
        updated_data = request.json
        users[user_id].update(updated_data)  # Partially update the user data
        return jsonify(users[user_id]), 200  # 200 OK if partial update is successful
    return "User not found", 404  # 404 Not Found if the user does not exist

# DELETE method: Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Handle DELETE requests to remove a user by ID.
    """
    if user_id in users:
        del users[user_id]  # Remove the user from the data structure
        return "User deleted", 204  # 204 No Content if deletion is successful
    return "User not found", 404  # 404 Not Found if the user does not exist

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)




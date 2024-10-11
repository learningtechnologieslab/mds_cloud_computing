from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulating a database with a dictionary
accounts = {}
next_account_id = 1

# Helper function to find an account by ID
def find_account(account_id):
    return accounts.get(account_id)


# Route to create a new account
@app.route('/account', methods=['POST'])
def create_account():
    global next_account_id
    data = request.get_json()

    name = data.get('name')
    initial_balance = data.get('initial_balance', 0)

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    account_id = next_account_id
    next_account_id += 1

    # Create the account and store it in the dictionary
    accounts[account_id] = {
        'id': account_id,
        'name': name,
        'balance': initial_balance
    }

    return jsonify({'message': 'Account created', 'account_id': account_id}), 201


# Route to get account balance
@app.route('/account/<int:account_id>/balance', methods=['GET'])
def get_balance(account_id):
    account = find_account(account_id)
    if account:
        return jsonify({'account_id': account_id, 'balance': account['balance']}), 200
    return jsonify({'message': 'Account not found'}), 404


# Route to deposit money into an account
@app.route('/account/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    account = find_account(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({'message': 'Amount must be greater than 0'}), 400

    account['balance'] += amount
    return jsonify({'message': 'Deposit successful', 'balance': account['balance']}), 200


# Route to withdraw money from an account
@app.route('/account/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    account = find_account(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({'message': 'Amount must be greater than 0'}), 400

    if amount > account['balance']:
        return jsonify({'message': 'Insufficient funds'}), 400

    account['balance'] -= amount
    return jsonify({'message': 'Withdrawal successful', 'balance': account['balance']}), 200


# Route to list all accounts
@app.route('/account', methods=['GET'])
def list_accounts():
    result = [{'id': acc['id'], 'name': acc['name'], 'balance': acc['balance']} for acc in accounts.values()]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)

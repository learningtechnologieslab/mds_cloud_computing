from flask import request
from flask_restful import Resource
from models import Account

class AccountResource(Resource):
    def post(self):
        """Create a new account"""
        data = request.get_json()
        name = data.get('name')
        initial_balance = data.get('initial_balance', 0)
        
        if not name:
            return {'message': 'Name is required'}, 400
        
        new_account = Account(name=name, initial_balance=initial_balance)
        return {'message': 'Account created', 'account_id': new_account.id}, 201

    def get(self):
        """List all accounts"""
        accounts = Account.all_accounts()
        result = [{'id': acc.id, 'name': acc.name, 'balance': acc.balance} for acc in accounts.values()]
        return result, 200


class AccountBalance(Resource):
    def get(self, account_id):
        """Get account balance"""
        account = Account.find_by_id(account_id)
        if account:
            return {'account_id': account_id, 'balance': account.balance}, 200
        return {'message': 'Account not found'}, 404


class DepositResource(Resource):
    def post(self, account_id):
        """Deposit money to the account"""
        account = Account.find_by_id(account_id)
        if not account:
            return {'message': 'Account not found'}, 404

        data = request.get_json()
        amount = data.get('amount')

        if not amount or amount <= 0:
            return {'message': 'Amount must be greater than 0'}, 400

        account.balance += amount
        return {'message': 'Deposit successful', 'balance': account.balance}, 200


class WithdrawResource(Resource):
    def post(self, account_id):
        """Withdraw money from the account"""
        account = Account.find_by_id(account_id)
        if not account:
            return {'message': 'Account not found'}, 404

        data = request.get_json()
        amount = data.get('amount')

        if not amount or amount <= 0:
            return {'message': 'Amount must be greater than 0'}, 400

        if amount > account.balance:
            return {'message': 'Insufficient funds'}, 400

        account.balance -= amount
        return {'message': 'Withdrawal successful', 'balance': account.balance}, 200

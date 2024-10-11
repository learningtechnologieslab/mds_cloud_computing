# A simple class is used to simulate a database with in-memory storage for accounts.

class Account:
    accounts = {}
    next_id = 1

    def __init__(self, name, initial_balance):
        self.id = Account.next_id
        self.name = name
        self.balance = initial_balance
        Account.accounts[self.id] = self
        Account.next_id += 1

    @classmethod
    def find_by_id(cls, account_id):
        return cls.accounts.get(account_id)
    
    @classmethod
    def delete_account(cls, account_id):
        if account_id in cls.accounts:
            del cls.accounts[account_id]

    @classmethod
    def all_accounts(cls):
        return cls.accounts

from flask import Flask
from flask_restful import Api
from resources.account import AccountResource, AccountBalance, DepositResource, WithdrawResource

app = Flask(__name__)
api = Api(app)

# Add resources to the API
api.add_resource(AccountResource, '/account')
api.add_resource(AccountBalance, '/account/<int:account_id>/balance')
api.add_resource(DepositResource, '/account/<int:account_id>/deposit')
api.add_resource(WithdrawResource, '/account/<int:account_id>/withdraw')

if __name__ == '__main__':
    app.run(debug=True)

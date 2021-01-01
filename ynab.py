import os
from requests import Response
from ynab_sdk import YNAB as YNAB_API
from ynab_sdk.api.models.responses.accounts import Account
from ynab_sdk.api.models.requests.transaction import TransactionRequest


class YNAB:
    def __init__(self):
        key = os.environ.get('YNAB_KEY')
        if key is None:
            raise EnvironmentError('error: the YNAB_KEY environment variable is not set')
        self.ynab = YNAB_API(key)

    def get_budget_id(self) -> str:
        budget_name = os.environ.get('YNAB_BUDGET_NAME')
        if budget_name is None:
            raise EnvironmentError('error: the YNAB_BUDGET_NAME environment variable is not set')

        budgets = self.ynab.budgets.get_budgets()
        for b in budgets.data.budgets:
            if b.name == budget_name:
                return b.id
        raise RuntimeError(f'error: no budget named {budget_name} was found')

    def get_account(self, budget_id: str, account_id: str) -> Account:
        accounts = self.ynab.accounts.get_accounts(budget_id)
        for a in accounts.data.accounts:
            if a.note == account_id:
                return a
        raise RuntimeError(f'error: no account with id {account_id} was found')

    def create_transactions(self, budget_id: str, transactions: list[TransactionRequest]) -> Response:
        return self.ynab.transactions.create_transactions(budget_id, transactions)

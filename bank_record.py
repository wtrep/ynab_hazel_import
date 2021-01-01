import codecs
from ofxparse import OfxParser
from ynab_sdk.api.models.requests.transaction import TransactionRequest


class BankRecord:
    def __init__(self, file):
        self.file = file

    @classmethod
    def parse(cls, path: str):
        with codecs.open(path) as fileobj:
            return cls(OfxParser.parse(fileobj))

    def get_account_id(self) -> str:
        return self.file.account.account_id

    def generate_transaction_requests(self, ynab_account_id: str) -> list[TransactionRequest]:
        requests = []
        for t in self.file.account.statement.transactions:
            r = TransactionRequest(ynab_account_id, t.date.isoformat(), int(t.amount * 1000))
            r.import_id = t.id[:36]
            r.memo = t.payee
            r.cleared = 'cleared'
            requests.append(r)
        return requests

import argparse
import logging
import pathlib
from bank_record import BankRecord
from ynab import YNAB


def parse_file_path() -> str:
    parser = argparse.ArgumentParser(description='Sync QFX files with YNAB API')
    parser.add_argument('-f', '--file', type=pathlib.Path, required=True, help='QFX file to import')
    args = parser.parse_args()
    return args.file


def update_transactions():
    logging.getLogger().setLevel(logging.INFO)
    path = parse_file_path()
    logging.info(f'Importing transactions from file {path}')

    record = BankRecord.parse(path)
    ynab = YNAB()
    budget_id = ynab.get_budget_id()
    account = ynab.get_account(budget_id, record.get_account_id())
    transactions = record.generate_transaction_requests(account.id)
    logging.info(f'Importing {len(transactions)} transaction(s)')

    res = ynab.create_transactions(budget_id, transactions)
    logging.info(res)


if __name__ == "__main__":
    update_transactions()

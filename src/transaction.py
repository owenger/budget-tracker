import os
import mt940
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List


class Currency(str, Enum):
    CHF = 'CHF'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'


@dataclass
class Transaction:
    amount: float
    currency: Currency
    transaction_date: date
    detail: str

    @staticmethod
    def list_from_swift_file(path: str) -> List["Transaction"]:
        if not os.path.isfile(path):
            print("Path does not exist, can't load swift file.")
            return False
        try:
            with open(path, 'r', encoding='latin1') as file:
                transactions: List[Transaction] = []
                data = mt940.parse(file.read())
                for transaction in data.transactions:
                    amount: int = int(transaction.data['amount'].amount)
                    currency: Currency = Currency(transaction.data['amount'].currency)
                    transaction_date: date = transaction.data['date']
                    detail = transaction.data['transaction_details']
                    start = detail.find('?')
                    end = detail.find('\n', start)
                    detail: str = detail[start+1:end]
                    transactions.append(Transaction(amount=amount, currency=currency, 
                                            transaction_date=transaction_date, detail=detail))
                return transactions
        except Exception as e:
            print(f'File not readable. Failed with exception: {e}.')
            return False


def main():
    abs_path = os.path.abspath(__file__)
    path = f'{os.path.dirname(abs_path)}/../resources/transactions.mt940'
    check = Transaction.list_from_swift_file(path)
    print(check)

if __name__ == '__main__':
    main()
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
class SwiftTransaction:
    amount: float
    currency: Currency
    transaction_date: date
    detail: str

class SwiftHandler:
    def __init__(self):
        self._transactions: List[SwiftTransaction] = []
    
    def load_from_file(self, path: str) -> bool:
        if not os.path.isfile(path):
            print("Path does not exist, can't load swift file.")
            return False
        try:
            with open(path, 'r', encoding='latin1') as file:
                data = mt940.parse(file.read())
                for transaction in data.transactions:
                    amount: int = int(transaction.data['amount'].amount)
                    currency: Currency = Currency(transaction.data['amount'].currency)
                    transaction_date: date = transaction.data['date']
                    detail = transaction.data['transaction_details']
                    start = detail.find('?')
                    end = detail.find('\n', start)
                    detail: str = detail[start+1:end]
                    self._transactions.append(SwiftTransaction(amount=amount, currency=currency, 
                                            transaction_date=transaction_date, detail=detail))
        except Exception as e:
            print(f'File not readable. Failed with exception: {e}.')
            return False
        



def main():
    abs_path = os.path.abspath(__file__)
    path = f'{os.path.dirname(abs_path)}/../resources/transactions.mt940'

    swift_handler = SwiftHandler()
    swift_handler.load_from_file(path)

if __name__ == '__main__':
    main()
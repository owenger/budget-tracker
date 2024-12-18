import os
import mt940
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional


class Currency(str, Enum):
    CHF = 'CHF'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'

class TransactionType(str, Enum):
    RENT = 'Rent'
    TRANSPORT = 'Transport'
    TRAVEL = 'Travel'
    EDUCATION = 'Education'
    FOOD = 'Food'
    HOUSEHOLD = 'Household'
    SAVINGS = 'Savings'
    LEISURE = 'Leisure'
    CLOTHES = 'Clothes'
    HEALTH_AND_FITNESS = 'Health and Fitness'
    INSURANCE = 'Insurance'
    INFRASTRUCTURE = 'Infrastructure'
    SUBSCIPTIONS = 'Subscriptions'


@dataclass
class Transaction:
    amount: float
    currency: Currency
    transaction_date: date
    detail: str
    transaction_type: Optional[TransactionType] = None

    @staticmethod
    def list_from_swift_file(path: str) -> List["Transaction"]:
        if not os.path.isfile(path):
            print(f"Path {path} does not exist, can't load swift file.")
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
    path = f'{os.path.dirname(abs_path)}/../resources/transaction_lists/transactions.mt940'
    check = Transaction.list_from_swift_file(path)
    print(check)

if __name__ == '__main__':
    main()
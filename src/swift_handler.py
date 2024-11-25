import os
import mt940


def main():
    abs_path = os.path.abspath(__file__)
    path = f'{os.path.dirname(abs_path)}/../resources/transactions.mt940'
    with open(path, encoding='latin1') as file:
        data = mt940.parse(file.read())

        for transaction in data.transactions:
            detail = transaction.data['transaction_details']
            start = detail.find('?')
            end = detail.find('\n', start)
            print('\n')
            print(detail[start+1:end])
            print('\n')

if __name__ == '__main__':
    main()
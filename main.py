import requests
import sys
import json
from rich.console import Console
from rich.table import Table

console = Console()

class NotSupportedCurrencyError(Exception):
    ...

def main():
    get_response(arguments())

def arguments():
    try:
        # Check if the amount of arguments is the right one
        if len(sys.argv) > 4 or len(sys.argv) < 4:
            raise IndexError
        
        float(sys.argv[1]) # Convert amount to float if it fails raises ValueError

        # Check if the base and target are supported
        with open("supported_currencies.json") as currencies:
            currencies_dict = json.load(currencies)
            if (sys.argv[2] not in currencies_dict or sys.argv[3] not in currencies_dict):
                raise NotSupportedCurrencyError
            
        # Assign data
        amount = f"&amount={sys.argv[1]}"
        from_ = sys.argv[2]
        to_ = f"&symbols={sys.argv[3]}"

    except IndexError:
        print("Usage: Amount Base Target")
        sys.exit(1)
    except ValueError:
        print("You must use an int or float!")
        sys.exit(1)
    except NotSupportedCurrencyError:
        print("Your base or target is not supported. Check 'supported_currencies.json' for more details.")
        sys.exit(1)


    return f"https://api.frankfurter.dev/v1/latest?base={from_}{to_}{amount}"

def get_response(url):
    r = requests.get(url)
    r = r.json()

    rates = r.get("rates")

    key, value = list(rates.items())[0]

    amount = r.get("amount")
    output1 = f"""[bold red]{amount} [bold green]{r.get("base")} = [bold red]{value} [bold green]{key}"""
    output2 = f"""[bold red]Base: [bold green]{r.get("base")} | [bold red]Target: [bold green]{key}"""
    rate = f"""[bold red]Rate: {value / amount}"""

    # Table using rich
    table = Table(show_header=True, header_style="bold green")
    table.add_column(":currency_exchange: Currency Converter", justify="center")
    table.add_row(output1)
    table.add_section()
    table.add_row(output2)
    table.add_row(rate)

    console.print(table) # Print table


if __name__ == "__main__":
    main()
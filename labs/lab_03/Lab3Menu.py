
from CreateTransactions import transaction_session
from GetCash import show_cash_balance
from GetTransactionsTicker import show_ticker_history
from PortfolioValue import show_portfolio_value


def main_menu():
    actions = {
        "1": transaction_session,
        "2": show_cash_balance,
        "3": show_ticker_history,
        "4": show_portfolio_value
    }

    while True:
        print("\n--- MENU ---")
        print("1. Add Transactions")
        print("2. Show Cash Balance")
        print("3. Show Transactions by Ticker")
        print("4. Show Portfolio Value")
        print("q. Quit Current Menu")

        choice = input("Choose option: ").strip().lower()

        if choice == "q":
            print("Exiting program.")
            break

        if choice not in actions:
            print("❌ Invalid option. Try again.")
            continue

        actions[choice]()
if __name__ == "__main__":
    main_menu()
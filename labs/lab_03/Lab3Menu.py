
from CreateTransactions import transaction_session
from GetCash import show_cash_balance
from GetTransactionsTicker import show_ticker_history
from PortfolioValue import show_portfolio_value



def main_menu():
    while True:
        print("\n--- MENU ---")
        print("1. Add Transactions")
        print("2. Show Cash Balance")
        print("3. Show Transactions by Ticker")
        print("4. Show Portfolio Value")
        print("q. Quit Current Menu")

        choice = input("Choose option: ").strip().lower()

        if choice not in ["1", "2", "3", "4", "q"]:
            print("❌ Invalid option. Try again.")
            continue

        if choice == "1":
            transaction_session()

        elif choice == "2":
            show_cash_balance()

        elif choice == "3":
            show_ticker_history()

        elif choice == "4":
            show_portfolio_value()

        elif choice == "q":
            print("Exiting program.")
            break


if __name__ == "__main__":
    main_menu()
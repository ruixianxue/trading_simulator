from order_book import OrderBook


def print_menu():
    """Print the menu options."""
    print("\n" + "="*60)
    print("                  TRADING SIMULATOR MENU")
    print("="*60)
    print("1. Place BUY order")
    print("2. Place SELL order")
    print("3. View order book")
    print("4. View trade history")
    print("5. View statistics")
    print("6. Clear database")
    print("7. Exit")
    print("="*60)


def get_order_details():
    """Get order details from user."""
    try:
        price = float(input("Enter price: $"))
        quantity = int(input("Enter quantity: "))
        return price, quantity
    except ValueError:
        print("❌ Invalid input! Please enter valid numbers.")
        return None, None


def main():
    """Interactive trading simulator."""
    
    print("="*60)
    print("     TRADING SIMULATOR - INTERACTIVE MODE")
    print("="*60)
    print("\nWelcome! You can place orders and see them match in real-time.")
    
    ob = OrderBook()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\n📝 PLACE BUY ORDER")
            price, quantity = get_order_details()
            if price and quantity:
                ob.place_order('BUY', price, quantity)
        
        elif choice == '2':
            print("\n📝 PLACE SELL ORDER")
            price, quantity = get_order_details()
            if price and quantity:
                ob.place_order('SELL', price, quantity)
        
        elif choice == '3':
            ob.get_order_book()
        
        elif choice == '4':
            ob.get_trade_history()
        
        elif choice == '5':
            ob.get_statistics()
        
        elif choice == '6':
            confirm = input("\n⚠️  Clear all data? (yes/no): ").strip().lower()
            if confirm == 'yes':
                ob.db.clear_database()
                print("✓ Database cleared!")
            else:
                print("Cancelled.")
        
        elif choice == '7':
            print("\n👋 Goodbye! Thanks for using the trading simulator.")
            ob.close()
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-7.")


if __name__ == "__main__":
    main()
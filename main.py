from order_book import OrderBook


def main():
    """Demo of the trading simulator."""
    
    print("="*60)
    print("         TRADING SIMULATOR - ORDER BOOK DEMO")
    print("="*60)
    
    # Create order book
    ob = OrderBook()
    
    print("\n📝 SCENARIO: Simulating a day of trading\n")
    
    # Morning: Initial orders arrive
    print("🌅 MORNING: Market opens, orders arrive...")
    print("-" * 60)
    
    ob.place_order('BUY', 100.50, 10)   # Someone wants to buy 10 @ $100.50
    ob.place_order('BUY', 100.00, 5)    # Someone wants to buy 5 @ $100.00
    ob.place_order('SELL', 101.00, 8)   # Someone wants to sell 8 @ $101.00
    ob.place_order('SELL', 101.50, 12)  # Someone wants to sell 12 @ $101.50
    
    # Show order book (no matches yet - prices don't cross)
    ob.get_order_book()
    
    # Midday: A seller willing to accept lower price
    print("\n☀️  MIDDAY: Aggressive seller arrives...")
    print("-" * 60)
    
    ob.place_order('SELL', 100.50, 7)   # Matches with buy order at 100.50!
    ob.get_order_book()
    
    # Afternoon: More trading activity
    print("\n🌤️  AFTERNOON: More orders...")
    print("-" * 60)
    
    ob.place_order('BUY', 101.00, 15)   # Aggressive buyer - matches sells!
    ob.get_order_book()
    
    ob.place_order('SELL', 99.50, 5)    # Very low sell price - matches everything!
    ob.get_order_book()
    
    # Evening: Final orders
    print("\n🌆 EVENING: Final trades...")
    print("-" * 60)
    
    ob.place_order('BUY', 100.75, 3)
    ob.place_order('SELL', 100.75, 3)   # Perfect match!
    ob.get_order_book()
    
    # Show results
    print("\n" + "="*60)
    print("                    END OF DAY SUMMARY")
    print("="*60)
    
    ob.get_trade_history()
    ob.get_statistics()
    
    print("\n✅ Demo completed!")
    print("\nThe database 'trading.db' contains all orders and trades.")
    print("You can inspect it with any SQLite browser.\n")
    
    # Close database
    ob.close()


if __name__ == "__main__":
    main()
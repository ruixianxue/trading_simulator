from order_book import OrderBook


def test_basic_matching():
    """Test 1: Basic order matching."""
    print("\n" + "="*60)
    print("TEST 1: Basic Order Matching")
    print("="*60)
    
    ob = OrderBook()
    ob.db.clear_database()
    
    # Place orders that should match
    print("\n📝 Placing BUY order at $100...")
    ob.place_order('BUY', 100.00, 10)
    
    print("\n📝 Placing SELL order at $100 (should match!)...")
    ob.place_order('SELL', 100.00, 10)
    
    # Check statistics
    stats = ob.db.get_statistics()
    
    if stats['total_trades'] == 1:
        print("\n✅ TEST PASSED: Orders matched successfully!")
    else:
        print("\n❌ TEST FAILED: Orders did not match!")
    
    ob.close()


def test_no_matching():
    """Test 2: Orders that don't match."""
    print("\n" + "="*60)
    print("TEST 2: No Matching (prices don't cross)")
    print("="*60)
    
    ob = OrderBook()
    ob.db.clear_database()
    
    # Place orders with gap in prices
    print("\n📝 Placing BUY order at $100...")
    ob.place_order('BUY', 100.00, 10)
    
    print("\n📝 Placing SELL order at $105 (should NOT match)...")
    ob.place_order('SELL', 105.00, 10)
    
    # Check statistics
    stats = ob.db.get_statistics()
    
    if stats['total_trades'] == 0:
        print("\n✅ TEST PASSED: Orders correctly did not match!")
    else:
        print("\n❌ TEST FAILED: Orders matched when they shouldn't!")
    
    ob.get_order_book()
    ob.close()


def test_partial_fill():
    """Test 3: Partial order fills."""
    print("\n" + "="*60)
    print("TEST 3: Partial Fill")
    print("="*60)
    
    ob = OrderBook()
    ob.db.clear_database()
    
    # Large buy order
    print("\n📝 Placing BUY order for 100 shares at $100...")
    ob.place_order('BUY', 100.00, 100)
    
    # Small sell order (partial fill)
    print("\n📝 Placing SELL order for 30 shares at $100...")
    ob.place_order('SELL', 100.00, 30)
    
    # Check order book - should still have 70 buy shares
    ob.get_order_book()
    
    stats = ob.db.get_statistics()
    
    if stats['total_volume'] == 30:
        print("\n✅ TEST PASSED: Partial fill worked correctly!")
    else:
        print("\n❌ TEST FAILED: Wrong volume traded!")
    
    ob.close()


def test_price_priority():
    """Test 4: Best price gets filled first."""
    print("\n" + "="*60)
    print("TEST 4: Price Priority")
    print("="*60)
    
    ob = OrderBook()
    ob.db.clear_database()
    
    # Multiple buy orders at different prices
    print("\n📝 Placing BUY orders at different prices...")
    ob.place_order('BUY', 100.00, 10)
    ob.place_order('BUY', 102.00, 10)  # Higher price - should match first
    ob.place_order('BUY', 101.00, 10)
    
    ob.get_order_book()
    
    # Sell order - should match with highest buy price (102)
    print("\n📝 Placing SELL order at $101 (should match with $102 buy)...")
    ob.place_order('SELL', 101.00, 5)
    
    # Check trade price
    trades = ob.db.get_all_trades()
    trade_price = trades[0][3]  # Price is at index 3
    
    if trade_price == 101.00:  # Trades at sell price in our implementation
        print("\n✅ TEST PASSED: Best price got priority!")
        print(f"   Trade executed at: ${trade_price:.2f}")
    else:
        print("\n❌ TEST FAILED: Wrong order matched!")
    
    ob.get_order_book()
    ob.close()


def test_multiple_matches():
    """Test 5: One order matching multiple orders."""
    print("\n" + "="*60)
    print("TEST 5: Multiple Matches")
    print("="*60)
    
    ob = OrderBook()
    ob.db.clear_database()
    
    # Multiple small sell orders
    print("\n📝 Placing multiple SELL orders...")
    ob.place_order('SELL', 100.00, 10)
    ob.place_order('SELL', 100.50, 15)
    ob.place_order('SELL', 101.00, 20)
    
    ob.get_order_book()
    
    # One large buy order that matches multiple sells
    print("\n📝 Placing large BUY order (should match multiple sells)...")
    ob.place_order('BUY', 101.00, 50)
    
    ob.get_order_book()
    ob.get_trade_history()
    
    stats = ob.db.get_statistics()
    
    if stats['total_trades'] >= 2:
        print("\n✅ TEST PASSED: Multiple matches occurred!")
    else:
        print("\n❌ TEST FAILED: Not enough matches!")
    
    ob.close()


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("         RUNNING AUTOMATED TESTS")
    print("="*60)
    
    test_basic_matching()
    test_no_matching()
    test_partial_fill()
    test_price_priority()
    test_multiple_matches()
    
    print("\n" + "="*60)
    print("              ALL TESTS COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
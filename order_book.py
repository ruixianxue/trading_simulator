from database import Database


class Order:
    """Represents a single buy or sell order."""
    
    def __init__(self, order_id, order_type, price, quantity, status, timestamp):
        self.id = order_id
        self.type = order_type  # 'BUY' or 'SELL'
        self.price = price
        self.quantity = quantity
        self.status = status
        self.timestamp = timestamp
    
    def __str__(self):
        return f"{self.type} {self.quantity} @ ${self.price:.2f} [{self.status}]"


class OrderBook:
    """
    Order book that matches buy and sell orders.
    Uses price-time priority: best price first, then earliest timestamp.
    """
    
    def __init__(self):
        self.db = Database()
    
    def place_order(self, order_type, price, quantity):
        """
        Place a new order (BUY or SELL).
        Automatically tries to match with existing orders.
        """
        if order_type not in ['BUY', 'SELL']:
            print("Error: order_type must be 'BUY' or 'SELL'")
            return None
        
        if price <= 0 or quantity <= 0:
            print("Error: price and quantity must be positive")
            return None
        
        # Insert order into database
        order_id = self.db.insert_order(order_type, price, quantity)
        print(f"✓ Order placed: {order_type} {quantity} @ ${price:.2f} (ID: {order_id})")
        
        # Try to match orders
        self.match_orders()
        
        return order_id
    
    def match_orders(self):
        """
        Match buy and sell orders.
        A trade happens when: buy_price >= sell_price
        """
        open_orders = self.db.get_open_orders()
        
        # Separate into buy and sell orders
        buy_orders = [Order(*o) for o in open_orders if o[1] == 'BUY']
        sell_orders = [Order(*o) for o in open_orders if o[1] == 'SELL']
        
        # Sort: buy orders by price DESC (highest first)
        buy_orders.sort(key=lambda x: (-x.price, x.timestamp))
        
        # Sort: sell orders by price ASC (lowest first)
        sell_orders.sort(key=lambda x: (x.price, x.timestamp))
        
        # Try to match orders
        for buy_order in buy_orders:
            for sell_order in sell_orders:
                # Can we match? Buy price must be >= sell price
                if buy_order.price >= sell_order.price:
                    # Execute trade at the sell price (market convention)
                    trade_price = sell_order.price
                    trade_quantity = min(buy_order.quantity, sell_order.quantity)
                    
                    # Record the trade
                    trade_id = self.db.insert_trade(
                        buy_order.id,
                        sell_order.id,
                        trade_price,
                        trade_quantity
                    )
                    
                    print(f"★ TRADE EXECUTED: {trade_quantity} @ ${trade_price:.2f} (Trade ID: {trade_id})")
                    
                    # Update quantities
                    buy_order.quantity -= trade_quantity
                    sell_order.quantity -= trade_quantity
                    
                    # Update order statuses
                    if buy_order.quantity == 0:
                        self.db.update_order_status(buy_order.id, 'FILLED')
                    if sell_order.quantity == 0:
                        self.db.update_order_status(sell_order.id, 'FILLED')
                    
                    # If sell order is filled, move to next sell order
                    if sell_order.quantity == 0:
                        break
                
                # If we can't match with this sell order, we won't match with more expensive ones
                else:
                    break
            
            # If buy order still has quantity but no more matches, stop
            if buy_order.quantity > 0:
                break
    
    def get_order_book(self):
        """Display current order book (all open orders)."""
        open_orders = self.db.get_open_orders()
        
        if not open_orders:
            print("\n📊 ORDER BOOK: Empty")
            return
        
        buy_orders = [Order(*o) for o in open_orders if o[1] == 'BUY']
        sell_orders = [Order(*o) for o in open_orders if o[1] == 'SELL']
        
        print("\n📊 ORDER BOOK:")
        print("="*50)
        
        print("\n🔴 SELL ORDERS (lowest price first):")
        if sell_orders:
            sell_orders.sort(key=lambda x: x.price)
            for order in sell_orders:
                print(f"  {order}")
        else:
            print("  (none)")
        
        print("\n🟢 BUY ORDERS (highest price first):")
        if buy_orders:
            buy_orders.sort(key=lambda x: -x.price)
            for order in buy_orders:
                print(f"  {order}")
        else:
            print("  (none)")
        
        print("="*50)
    
    def get_trade_history(self):
        """Display all executed trades."""
        trades = self.db.get_all_trades()
        
        if not trades:
            print("\n📈 TRADE HISTORY: No trades yet")
            return
        
        print("\n📈 TRADE HISTORY:")
        print("="*50)
        for trade in trades:
            trade_id, buy_id, sell_id, price, quantity, timestamp = trade
            print(f"Trade #{trade_id}: {quantity} @ ${price:.2f} | {timestamp[:19]}")
        print("="*50)
    
    def get_statistics(self):
        """Display trading statistics."""
        stats = self.db.get_statistics()
        
        print("\n📊 STATISTICS:")
        print("="*50)
        print(f"Total Orders: {stats['total_orders']}")
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Total Volume: {stats['total_volume']}")
        print(f"Average Price: ${stats['avg_price']:.2f}")
        print("="*50)
    
    def close(self):
        """Close database connection."""
        self.db.close()
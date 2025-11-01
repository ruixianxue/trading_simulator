import sqlite3
from datetime import datetime


class Database:
    """Handles all database operations for the trading simulator."""
    
    def __init__(self, db_name='trading.db'):
        """Initialize database connection and create tables."""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create orders and trades tables if they don't exist."""
        # Orders table - stores all buy/sell orders
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_type TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Trades table - stores executed trades
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buy_order_id INTEGER,
                sell_order_id INTEGER,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
    
    def insert_order(self, order_type, price, quantity):
        """Insert a new order into database."""
        timestamp = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO orders (order_type, price, quantity, status, timestamp)
            VALUES (?, ?, ?, 'OPEN', ?)
        ''', (order_type, price, quantity, timestamp))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def insert_trade(self, buy_order_id, sell_order_id, price, quantity):
        """Insert a new trade into database."""
        timestamp = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO trades (buy_order_id, sell_order_id, price, quantity, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (buy_order_id, sell_order_id, price, quantity, timestamp))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_order_status(self, order_id, status):
        """Update order status (OPEN, FILLED, PARTIAL)."""
        self.cursor.execute('''
            UPDATE orders SET status = ? WHERE id = ?
        ''', (status, order_id))
        self.conn.commit()
    
    def get_all_orders(self):
        """Get all orders from database."""
        self.cursor.execute('SELECT * FROM orders ORDER BY timestamp DESC')
        return self.cursor.fetchall()
    
    def get_open_orders(self):
        """Get all open orders."""
        self.cursor.execute('''
            SELECT * FROM orders WHERE status = 'OPEN' ORDER BY price DESC, timestamp ASC
        ''')
        return self.cursor.fetchall()
    
    def get_all_trades(self):
        """Get all trades from database."""
        self.cursor.execute('SELECT * FROM trades ORDER BY timestamp DESC')
        return self.cursor.fetchall()
    
    def get_statistics(self):
        """Get trading statistics."""
        # Total number of trades
        self.cursor.execute('SELECT COUNT(*) FROM trades')
        total_trades = self.cursor.fetchone()[0]
        
        # Total volume traded
        self.cursor.execute('SELECT SUM(quantity) FROM trades')
        result = self.cursor.fetchone()[0]
        total_volume = result if result else 0
        
        # Average trade price
        self.cursor.execute('SELECT AVG(price) FROM trades')
        result = self.cursor.fetchone()[0]
        avg_price = result if result else 0
        
        # Total orders
        self.cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = self.cursor.fetchone()[0]
        
        return {
            'total_trades': total_trades,
            'total_volume': total_volume,
            'avg_price': round(avg_price, 2) if avg_price else 0,
            'total_orders': total_orders
        }
    
    def clear_database(self):
        """Clear all data from database (for testing)."""
        self.cursor.execute('DELETE FROM orders')
        self.cursor.execute('DELETE FROM trades')
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
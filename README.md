# Trading Simulator - Order Book

A simple trading simulation system built with Python and SQLite that demonstrates order matching, trade execution, and database operations.

## 📋 What This Project Does

This project simulates a basic **order book** used in financial markets:

- **Place BUY and SELL orders** with price and quantity
- **Automatically match orders** when prices cross (buy price ≥ sell price)
- **Store all data in SQL database** (SQLite)
- **Track trade history** and statistics
- **Real-time order book visualization**

## 🎯 Learning Goals

Built to understand:
- How trading systems work (order matching, price priority)
- Python programming with classes and databases
- SQL operations (CREATE, INSERT, SELECT, UPDATE)
- Market microstructure basics

## 📁 Project Structure

```
trading-simulator/
├── database.py       # SQL database operations
├── order_book.py     # Main trading logic (order matching)
├── main.py           # Demo script
├── interactive.py    # Interactive mode
├── test.py           # Automated tests
├── trading.db        # SQLite database (created when you run)
└── README.md         # This file
```

## 🚀 How to Run

### Prerequisites
- Python 3.x (no external libraries needed!)
- SQLite is built into Python

### Option 1: Run Demo (Recommended First)
```bash
python3 main.py
```
This runs a full simulation showing various trading scenarios.

### Option 2: Interactive Mode
```bash
python3 interactive.py
```
Place your own orders and see them match in real-time!

### Option 3: Run Tests
```bash
python3 test.py
```
Runs automated tests to verify everything works correctly.

## 📊 How It Works

### 1. Order Matching Logic

**When can orders match?**
- A BUY order matches a SELL order when: `buy_price >= sell_price`
- Trade executes at the **sell price** (market convention)

**Example:**
```
BUY  10 shares @ $100.50
SELL 10 shares @ $100.00
→ TRADE: 10 shares @ $100.00 ✓
```

### 2. Price-Time Priority

Orders are matched by:
1. **Best price first**
   - Highest buy price gets priority
   - Lowest sell price gets priority
2. **Then by time** (first-come, first-served)

### 3. Database Schema

**Orders Table:**
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_type TEXT,        -- 'BUY' or 'SELL'
    price REAL,             -- Order price
    quantity INTEGER,       -- Number of shares
    status TEXT,            -- 'OPEN' or 'FILLED'
    timestamp TEXT          -- When order was placed
);
```

**Trades Table:**
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    buy_order_id INTEGER,   -- Which buy order
    sell_order_id INTEGER,  -- Which sell order
    price REAL,             -- Trade price
    quantity INTEGER,       -- Number traded
    timestamp TEXT          -- When trade executed
);
```

## 💡 Example Session

```python
from order_book import OrderBook

# Create order book
ob = OrderBook()

# Place orders
ob.place_order('BUY', 100.50, 10)   # Want to buy 10 @ $100.50
ob.place_order('SELL', 100.00, 5)   # Want to sell 5 @ $100.00
# → Automatically matches! Trade: 5 @ $100.00

# View order book
ob.get_order_book()

# View trade history
ob.get_trade_history()

# Get statistics
ob.get_statistics()
```

## 🧪 Testing

Run `test.py` to verify:
1. ✅ Basic order matching works
2. ✅ Orders don't match when prices don't cross
3. ✅ Partial fills work correctly
4. ✅ Best price gets priority
5. ✅ One order can match multiple orders

## 📈 Features

- ✅ **Automatic order matching** - Real-time execution
- ✅ **SQL database** - All data persisted
- ✅ **Price-time priority** - Fair order matching
- ✅ **Partial fills** - Orders can be partially filled
- ✅ **Trade history** - Complete audit trail
- ✅ **Statistics** - Volume, average price, etc.
- ✅ **Interactive mode** - Manual testing
- ✅ **Automated tests** - Verify correctness

## 🔧 Technologies Used

- **Python 3** - Main programming language
- **SQLite** - Database (built into Python, no installation needed)
- **Object-Oriented Programming** - Classes for clean code
- **SQL** - Database queries and operations

## 📚 What I Learned

Building this project taught me:
- How order books work in real trading systems
- Order matching algorithms (price-time priority)
- SQL database design and operations
- Python class design and methods
- Market microstructure basics
- Trade execution and settlement

## 🎓 Concepts Demonstrated

### Trading Concepts:
- Order book structure
- Bid-ask spread
- Order matching
- Trade execution
- Price discovery

### Programming Concepts:
- Object-Oriented Programming (classes)
- Database operations (SQL)
- File I/O
- Error handling
- Testing

## 🚧 Future Improvements

Potential enhancements:
- Add different order types (LIMIT, MARKET, STOP)
- Implement order cancellation
- Add historical price charts
- Support multiple instruments (stocks)
- Add API for external access
- Real-time data feeds

## 📝 Notes

- This is a **simplified simulation** for learning purposes
- Real trading systems are much more complex
- Does not include: latency, fees, regulations, etc.
- Uses SQLite (simple) - production systems use PostgreSQL, MySQL, etc.

## 👤 Author

Built by Ruixian Xue as part of learning Python, SQL, and trading systems.

## 📄 License

Free to use for learning and education.
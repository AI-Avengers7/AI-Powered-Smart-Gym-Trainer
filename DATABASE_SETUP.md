# Database Connection Guide

## 🗄️ Where Database Connection Happens

### 1. **Environment Variables** (`.env`)
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### 2. **Configuration** (`config.py`)
```python
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

### 3. **Database Initialization** (`app/models/__init__.py`)
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

### 4. **Application Setup** (`app.py`)
```python
db.init_app(app)  # Initialize database with Flask app

with app.app_context():
    db.create_all()  # Create all tables
```

---

## 🚀 Quick Setup Options

### **Option A: SQLite (Quick Start - Already Configured)**

✅ **No installation needed!** Already set up in your `.env`:
```bash
DATABASE_URL=sqlite:///test_gym_trainer.db
```

**Just run:**
```bash
python3 app.py
```

The database file `test_gym_trainer.db` will be created automatically.

---

### **Option B: PostgreSQL (Production Ready)**

#### Step 1: Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Step 2: Run the setup script
```bash
./setup_postgres.sh
```

#### Step 3: Update `.env` file
```bash
DATABASE_URL=postgresql://gym_user:GymTrainer2024!@localhost:5432/gym_trainer_db
```

#### Step 4: Run the application
```bash
python3 app.py
```

---

### **Option C: Manual PostgreSQL Setup**

```bash
# 1. Access PostgreSQL
sudo -u postgres psql

# 2. Create database and user
CREATE DATABASE gym_trainer_db;
CREATE USER gym_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gym_trainer_db TO gym_user;

# 3. Connect to database
\c gym_trainer_db

# 4. Grant schema privileges
GRANT ALL ON SCHEMA public TO gym_user;

# 5. Exit
\q
```

Then update `.env`:
```bash
DATABASE_URL=postgresql://gym_user:your_password@localhost:5432/gym_trainer_db
```

---

## 🔍 Connection String Format

### PostgreSQL:
```
postgresql://username:password@host:port/database_name
```

Examples:
```bash
# Local PostgreSQL
DATABASE_URL=postgresql://gym_user:password123@localhost:5432/gym_trainer_db

# Remote PostgreSQL
DATABASE_URL=postgresql://user:pass@192.168.1.100:5432/gym_db

# Heroku PostgreSQL
DATABASE_URL=postgresql://user:pass@ec2-host.compute-1.amazonaws.com:5432/dbname
```

### SQLite:
```
sqlite:///filename.db
```

Examples:
```bash
# Relative path
DATABASE_URL=sqlite:///gym_trainer.db

# Absolute path
DATABASE_URL=sqlite:////home/user/databases/gym_trainer.db

# In-memory (for testing)
DATABASE_URL=sqlite:///:memory:
```

---

## 📊 Database Tables

When you run `python3 app.py`, these tables are automatically created:

### **users** table:
- `id` (Primary Key)
- `name`
- `email` (Unique)
- `password` (Hashed)

### **workouts** table:
- `id` (Primary Key)
- `exercise`
- `reps`
- `sets`
- `user_id` (Foreign Key → users.id)

---

## ✅ Verify Database Connection

### Check if PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

### Start PostgreSQL (if not running):
```bash
sudo systemctl start postgresql
```

### Test connection:
```bash
psql -U gym_user -d gym_trainer_db -h localhost -W
```

### View tables in your database:
```sql
\dt
```

### View data:
```sql
SELECT * FROM users;
SELECT * FROM workouts;
```

---

## 🐛 Troubleshooting

### Error: "connection refused"
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start it
sudo systemctl start postgresql
```

### Error: "authentication failed"
```bash
# Check your password in .env matches the database user password
# Reset password if needed:
sudo -u postgres psql
ALTER USER gym_user WITH PASSWORD 'new_password';
```

### Error: "database does not exist"
```bash
# Create the database
sudo -u postgres createdb gym_trainer_db
```

### Error: "permission denied"
```bash
# Grant proper permissions
sudo -u postgres psql -d gym_trainer_db
GRANT ALL ON SCHEMA public TO gym_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO gym_user;
```

---

## 🔄 Database Migrations (Optional)

If you need to modify the database schema later:

```bash
# Initialize migrations
flask db init

# Create a migration
flask db migrate -m "Add new column"

# Apply migrations
flask db upgrade
```

---

## 📝 Summary

**Current Setup:**
- ✅ Using SQLite for testing
- ✅ Database file: `test_gym_trainer.db`
- ✅ Tables created automatically on app start

**To Switch to PostgreSQL:**
1. Run `./setup_postgres.sh`
2. Update `.env` with PostgreSQL connection string
3. Restart app with `python3 app.py`

**Database Connection Files:**
- `.env` → Database URL
- `config.py` → Configuration loader
- `app/models/__init__.py` → Database object
- `app.py` → Database initialization

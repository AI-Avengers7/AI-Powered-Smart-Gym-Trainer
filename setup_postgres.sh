#!/bin/bash
# PostgreSQL Database Setup Script

echo "🗄️ Setting up PostgreSQL Database for AI Gym Trainer"
echo "=================================================="

# Database credentials
DB_NAME="gym_trainer_db"
DB_USER="gym_user"
DB_PASSWORD="GymTrainer2024!"

echo "Creating PostgreSQL database and user..."

# Create database and user
sudo -u postgres psql <<EOF
-- Create database
CREATE DATABASE $DB_NAME;

-- Create user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Grant schema privileges
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database created successfully!"
    echo ""
    echo "📝 Update your .env file with:"
    echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
    echo ""
    echo "Then run: python3 app.py"
else
    echo "❌ Failed to create database. Make sure PostgreSQL is installed."
fi

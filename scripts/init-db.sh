#!/bin/bash

# INSTALL RS_FULLSTACK DB

# DB Configuration Variables
db_user='rs_fullstack'
db_pass='O,AenBn]9Flbw`wg6MUY8Hp{0F{us62*r!I]7vJY#f3!l4SAzw'
db_name='rs_fullstack_db'

# Function to check if PostgreSQL is installed
is_postgres_installed() {
    command -v psql >/dev/null
}

# Function to install PostgreSQL
install_postgres() {
    echo "Installing PostgreSQL..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install postgresql postgresql-contrib -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install postgresql
    fi
    echo "PostgreSQL installed successfully."
}

# OS-specific installations
case "$OSTYPE" in
    "linux-gnu"*)
        is_postgres_installed || install_postgres
        ;;
    "darwin"*)
        ! command -v brew >/dev/null && /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        is_postgres_installed || install_postgres
        ;;
    "win32"|"cygwin")
        echo "Please install PostgreSQL manually from https://www.postgresql.org/download/windows/"
        echo "Or use WSL on Windows 10/11 for a Linux environment."
        exit 1
        ;;
    *)
        echo "Unknown Operating System!"
        exit 1
        ;;
esac

# Ensure the PostgreSQL service is running
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo systemctl start postgresql
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew services start postgresql
fi

# Determine the current user
current_user=$(whoami)

# Drop and recreate the database and role
sudo_p_user='postgres'
[[ "$OSTYPE" == "darwin"* ]] || sudo_p_user=$current_user

echo "Dropping existing database and user if they exist..."
sudo -u $sudo_p_user psql -d postgres -c "REVOKE ALL PRIVILEGES ON SCHEMA public FROM $db_user;"
sudo -u $sudo_p_user psql -d postgres -c "DROP DATABASE IF EXISTS $db_name;"
sudo -u $sudo_p_user psql -d postgres -c "DROP ROLE IF EXISTS $db_user;"

# Fix for collation version mismatch
sudo -u $sudo_p_user psql -d postgres -c "ALTER DATABASE template1 REFRESH COLLATION VERSION;"

echo "Creating new database: $db_name"
sudo -u $sudo_p_user psql -d postgres -c "CREATE DATABASE $db_name;"

echo "Creating new user: $db_user"
sudo -u $sudo_p_user psql -d postgres -c "CREATE USER $db_user WITH PASSWORD '$db_pass';"

echo "Granting permissions to the new user on the new database"
sudo -u $sudo_p_user psql -d postgres -c "ALTER DATABASE $db_name OWNER TO $db_user;"

echo "Installation and configuration completed successfully."

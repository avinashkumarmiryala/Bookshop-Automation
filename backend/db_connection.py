import mysql.connector as connector

def create_database():
    mydb = connector.connect(
    host="127.0.0.1",
    user="root",
    password="Avinash@6174")

    
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]

    if "bookshop" not in [db.lower() for db in databases]:
        mycursor.execute("CREATE DATABASE BookShop")
        print("✅ Database 'BookShop' created.")
    else:
        print("ℹ️ Database 'BookShop' already exists.")

    mycursor.close()
    mydb.close()

def create_connection():
    connection_temp = None
    try:
        connection_temp = connector.connect(
            host="127.0.0.1",
            user="root",
            password="Avinash@6174",
            database="BookShop"
        )        
        if connection_temp.is_connected():
            print("✅ Connection succeeded!")
    except connector.Error as err:
        print(f"❌ Error: {err}")
        connection_temp = None  # Ensure it returns None if connection fails
    
    return connection_temp

create_database()
import mysql.connector as connector

def create_database():
    mydb = connector.connect(
    host="127.0.0.1",
    user="root",
    password="Avinash@6174")

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE BookShop")
    mycursor.close()

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

#create_database()
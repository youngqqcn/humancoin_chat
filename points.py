import pymysql

def main():

    # Create a connection to the database
    cnx = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='ae633jmFLiAGqigSO41',
        db='fansland_sol'
    )

    # Create a cursor object
    cursor = cnx.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM chat_history")

    # Fetch the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the cursor and connection
    cursor.close()
    cnx.close()


    pass

if __name__ == '__main__':
    main()
import sqlite3

# Connect to database (creates if not exists)
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Create Students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students(
        name VARCHAR(30), 
        class VARCHAR(10), 
        marks INT, 
        company VARCHAR(30)
    )
''')

# Insert 5 student records
cursor.execute("INSERT INTO Students VALUES('Sijo', 'BTech', 75, 'JSW')")
cursor.execute("INSERT INTO Students VALUES('Lijo', 'MTech', 69, 'TCS')")
cursor.execute("INSERT INTO Students VALUES('Rijo', 'BSc', 79, 'WIPRO')")
cursor.execute("INSERT INTO Students VALUES('Sibin', 'MSc', 89, 'INFOSYS')")
cursor.execute("INSERT INTO Students VALUES('Dilsha', 'MCom', 99, 'Cyient')")

# Show inserted records
print("Inserted Records:")
for row in cursor.execute("SELECT * FROM Students"):
    print(row)

# Save and close
connection.commit()
connection.close()
print("\nDatabase 'data.db' created successfully!")
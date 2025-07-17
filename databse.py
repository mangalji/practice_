import mysql.connector
from faker import Faker
import random

f = Faker('en_IN')

mydb = mysql.connector.connect(
    host = "localhost",
    user = "RajMangal",
    passwd = "raj12345",
    database ="pet_adoption_system_database"
    )
mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE pet_adoption_system_database")
# print("Database created successfully")

# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#     print(x)	

mycursor.execute("SELECT DATABASE()")
for database in mycursor:
    print(database)
print("------------------------------")

mycursor.execute("SHOW TABLES")
                                           # show_result = mycursor.fetchall()
for row in mycursor:
    print(row)
print("------------------------------")

# mycursor.execute("CREATE TABLE user_table(user_id INT PRIMARY KEY, name varchar(255), phone VARCHAR(255), email varchar(255), password varchar(255))")    
# mycursor.execute("CREATE TABLE pet_table(pet_id INT PRIMARY KEY, name varchar(255), category varchar(255), breed varchar(255), age varchar(3), weight varchar(5), medical_history varchar(255))")
# mycursor.execute("CREATE TABLE transaction_table(tr_id INT PRIMARY KEY,request_id int, foreign key(request_id)references call_request_table(request_id), pet_id int, FOREIGN KEY(pet_id)references pet_table(pet_id),user_id int,foreign key(user_id) references user_table(user_id),status varchar(255))")
# mycursor.execute("CREATE TABLE call_request_table(request_id INT PRIMARY KEY, pet_id int,user_id int,status varchar(255), FOREIGN KEY(pet_id)references pet_table(pet_id), foreign key(user_id) references user_table(user_id))")
# mycursor.execute("ALTER TABLE user_table ADD COLUMN (address VARCHAR(255),created_at DATETIME(6),last_login DATETIME(6))")
# mycursor.execute("ALTER TABLE pet_table ADD COLUMN (added_at DATETIME(6))")


# categories = ['Dog', 'Cat', 'Rabbit', 'Cow','Buffalo']
breeds = {
    'Dog': ['Labrador', 'Pug', 'German Shepherd', 'Beagle'],
    'Cat': ['Persian', 'Siamese', 'Maine Coon'],
    'Rabbit': ['Dutch', 'Mini Rex', 'Lionhead'],
    'Cow': ['Sahiwal', 'Red Sindhi', 'Gir', 'Tharparkar', 'Kankrej'],
    'Buffalo': ['Anatolian buffalo','Australian buffalo','Azi Kheli','Azari','Badavan','Murrah']
}
pet_names = ['Max', 'Bella', 'Charlie', 'Luna', 'Rocky', 'Milo', 'Daisy', 'Coco', 'Simba', 'Chiku', 'Oreo', 'Golu']


def get_existing_ids(table_name, column_name):
    query = f"SELECT {column_name} FROM {table_name}"
    mycursor.execute(query)
    results = mycursor.fetchall()
    return [row[0] for row in results]

def User():
    insert_data = "INSERT INTO user_table(user_id,name,phone,email,password,address,created_at,last_login) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    records = []
    entries = int(input("how many entries you want.: "))
    
    for _ in range(1,entries+1):
        user_id = f.unique.random_int(1,10000)       #int(input("enter the user id: "))
        name = f.name()                             #input("enter the name of user: ")
        phone = f.phone_number()                    #int(input("enter the mobile no. of user: ")) #f.phone_number() 
        email = f.email()                           #input("enter the email of user: ")
        password = f.password()                     #input("enter the password: ")
        address = f.address()
        created_at = f.date_between(start_date='-1y',end_date='now')            # date random generated lene ke liye humein f.date_time_between(start_date='',end_date='') ka use hoga 
        last_login = f.date_between(start_date=created_at,end_date='now')
        ID = user_id

        record = (user_id,name,phone,email,password,address,created_at,last_login)
        records.append(record)

    mycursor.executemany(insert_data,records)
    print(records)
    return ID 


def Pets():
    insert_data = "INSERT IGNORE INTO pet_table(pet_id,name,category,breed,age,weight,medical_history,added_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    records = []
    entries = int(input("how many entries you want.: "))
    
    for i in range(1,entries+1):
        pet_id = f.unique.random_int(1,10000)        #int(input("enter the unique id of pet: "))
        name = random.choice(pet_names)         #input("enter the name of pet: ")
        category = f.random_element(['Dog', 'Cat', 'Rabbit', 'Cow','Buffalo'])  #input("enter the category of pet like dog, cat: ")
        breed = random.choice(breeds[category]) #input("enter the breed of pet:")
        age = f.random_int(min=0,max=20)        #input("enter the age of pet.if age in year enter y, 'if in month enter m with your number': ")
        weight = f.random_int(min=20,max=2000)  #input("enter the weight of pet: ")
        medical_history = f.text()              #input("enter any type of medical history 'if occurred, if not enter no': ")
        added_at = f.date_between(start_date='-1y',end_date='now')
        record = (pet_id,name,category,breed,age,weight,medical_history,added_at)
        records.append(record)
        id_ = pet_id
    mycursor.executemany(insert_data,records)
    print(records)
    return id_


def Transactions():
    insert_data = "INSERT INTO transaction_table(tr_id,pet_id,user_id,status) VALUES(%s,%s,%s,%s)"
    records = []
    entries = int(input("how many entries you want.: "))
    user_ids = get_existing_ids("user_table", "user_id")
    pet_ids = get_existing_ids("pet_table", "pet_id")
    request_ids = get_existing_ids("call_request_table","request_id")

    for i in range(1,entries+1):
        tr_id = f.unique.random_int(1,10000)             #int(input("enter the tr. id: "))
        pet_id = f.random.choice(pet_ids)                 #int(input("enter the pet_id: "))
        user_id = f.random.choice(user_ids)
        request_id = f.random.choice(request_ids)                        #int(input("enter the user_id: "))
        status = f.random_element(['listed','got'])     #input("enter the status of pet: ")
    
        record = (tr_id,pet_id,user_id,status)
        records.append(record)

    mycursor.executemany(insert_data,records)   
    print(records)
    return tr_id


def callrequests():
    insert_data = "INSERT IGNORE INTO call_request_table(request_id,pet_id,user_id,status) VALUES(%s,%s,%s,%s)"
    records = []
    entries = int(input("how many entries you want.: "))
    user_ids = get_existing_ids("user_table", "user_id")
    pet_ids = get_existing_ids("pet_table", "pet_id")

    for i in range(1,entries+1):        
        request_id = f.unique.random_int(1,10000) #int(input("enter the request id: "))
        pet_id = f.random.choice(pet_ids)            #int(input("enter the pet_id: "))
        user_id = f.random.choice(user_ids)           #int(input("enter the user_id: "))
        status = f.random_element(['Accepted','Pending','Rejected']) #input("enter the status of pet: ")
    
        record = (request_id,pet_id,user_id,status)
        records.append(record)

    mycursor.executemany(insert_data,records)
    print(records)
    return request_id

def update(table_name,column_name,conditon,entry_for_update):
    query = f"UPDATE {table_name} SET {column_name} = %s WHERE {conditon}"
    mycursor.execute(query,(entry_for_update))
    print(f"your {table_name}'s entry is updated.")
    

def select(column_name,table_name):
    query = F"SELECT {column_name} FROM {table_name}"
    mycursor.execute(query)
    for x in mycursor:
        print(x)

choice = input("what you want to do (delete or insert or update or select): ")

if choice == 'insert' or choice == 'Insert' or choice == 'INSERT':   

    choice_1 = input("Enter table name which you want to insert (user/pet/transaction/call request): ")
    if choice_1 == 'user' or choice_1 == 'User':
        User()
    elif choice_1 == 'pet' or choice_1 == 'Pet':
        Pets()
    elif choice_1 == 'transaction' or choice_1 == 'Transaction':
        Transactions()
    elif choice_1 == 'call request' or choice_1 == 'Call Request':
        callrequests()
    else:
        print("incorrect entry!")

elif choice == 'DELETE' or choice == 'delete' or choice == 'Delete':

    choice_2 = input("what you want to delete: table or table's entire data\nPress 1 for table\nPress 2 for entire data\nTell me your choice: ")
    if choice_2 == '1':
        choice_3 = input("Which table you want to delete completely:\nPress 1 for User's table:\nPress 2 for Pets's table:\nPress 3 for Transaction's table:\nPress 4 for Call request table:\nEnter your choice: ")
        if choice_3 == '1':
            mycursor.execute("DROP TABLE user_table")
            print("User table entire data deleted successfully")
        elif choice_3 == '2':
            mycursor.execute("DROP TABLE pet_table")
            print("Pet table entire data deleted successfully")
        elif choice_3 == '3':
            mycursor.execute("DROP TABLE transaction_table")
            print("Transaction table entire data deleted successfully")
        elif choice_3 == '4':
            mycursor.execute("DROP TABLE call_request_table")
            print("Call request table entire data deleted successfully")
        else:
            print("wrong entry!")
    elif choice_2 == '2':
        choice_4 = input("Which table's data you want to delete completely:\nPress 1 for User's table:\nPress 2 for Pets's table:\nPress 3 for Transaction's table:\nPress 4 for Call request table:\nPress 5 for all\nEnter your choice: ")
        if choice_4 == '1':
            mycursor.execute("DELETE FROM user_table")
            print("User table entire data deleted successfully")
        elif choice_4 == '2':
            mycursor.execute("DELETE FROM pet_table")
            print("Pet table entire data deleted successfully")
        elif choice_4 == '3':
            mycursor.execute("DELETE FROM transaction_table")
            print("Transaction table entire data deleted successfully")
        elif choice_4 == '4':
            mycursor.execute("DELETE FROM call_request_table")
            print("Call request table entire data deleted successfully")
        elif choice_4 == '5':
            mycursor.execute("DELETE FROM transaction_table")
            mycursor.execute("DELETE FROM call_request_table")
            mycursor.execute("DELETE FROM user_table")
            mycursor.execute("DELETE FROM pet_table")
        else:
            print("wrong entry!")
    else:
        print('wrong input!')
elif choice == 'update' or choice == 'Update' or choice == 'UPDATE':
    table_name = input("enter your table name: ")
    column_name = input("enter your column name: ")
    conditon = input("enter your condition: ")
    entry_for_update = input("enter your updated entry: ")
    update(table_name,column_name,conditon,entry_for_update)

elif choice == 'select' or choice == 'Select' or choice == 'SELECT':
    choice_5 = input("Do you want to select 'all data' or any 'specific column'\nenter 'all' for all data, and column for specific column: ")
    if choice_5 == 'all' or choice_5 == 'All' or choice_5 == 'ALL':
        mycursor.execute("show tables")
        for table in mycursor:
            print(table)
        select_table_name = input("enter table name: ")
        select('*',select_table_name)
    elif choice_5 == 'column' or choice_5 == 'Column' or choice_5 == 'COLUMN':
        select_table_name = input("enter table name: ")
        select_column = input("enter column name: ")
        select(select_column,select_table_name)
    else:
        print("wrong entry!")

else:
    print('wrong entry!')
mydb.commit()

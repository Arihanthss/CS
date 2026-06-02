import csv
import os
import hashlib

def register(username, passwd):
   
    db_file = "users.csv"
    file_exists = os.path.isfile(db_file)
    
    # Checks pre existance to avoid duplication
    if file_exists:
        with open(db_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    return False, "Username already exists. Please choose another."
                    
    # Common Security practice to not store passwds in text files
    hashed_input = hashlib.sha256(passwd.encode()).hexdigest()
    
    # Adding the user to the master database IN HASHED PASSWORDS!!!
    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_input])
        
    return True, "Account created successfully!"

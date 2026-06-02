import csv
import os
import hashlib

def auth(username, passwd): #function that validates user
    db_file = "users.csv"
    if not os.path.isfile(db_file):
        return False, "Database empty."
        
    hashed_input = hashlib.sha256(passwd.encode()).hexdigest()
    
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                if row[1] == hashed_input:
                    return True, "Login successful!"
                else:
                    return False, "Incorrect password."
    return False, "Username not found."

def get_user_hash(username): #Self Explanatory
    db_file = "users.csv"
    if os.path.isfile(db_file):
        with open(db_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    return row[1]
    return "ERROR"

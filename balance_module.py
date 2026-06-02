import csv
import os

def get_balance(username):
    """Fetches the user's balance. If they aren't in the file yet, it returns 0."""
    db_file = "balance.csv"
    
    if not os.path.isfile(db_file):
        return 0  # File doesnt exist yet balance is 0
        
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                return int(row[1])
                
    return 0  # User not found in the file balance is 0

def add_funds(username, amount):
    """Adds money to the user's balance and saves it to the CSV."""
    db_file = "balance.csv"
    temp_file = "temp_balance.csv"
    user_found = False
    
    #Read existing data and update the balance if the user exists
    if os.path.isfile(db_file):
        with open(db_file, mode='r') as file, open(temp_file, mode='w', newline='') as out_file:
            reader = csv.reader(file)
            writer = csv.writer(out_file)
            
            for row in reader:
                if row:
                    if row[0] == username:
                        #Add the new amount to their existing balance
                        new_balance = int(row[1]) + amount
                        writer.writerow([username, new_balance])
                        user_found = True
                    else:
                        #Write other users exactly as they are
                        writer.writerow(row)
    
    #  If the user wasn't in the file append them with their first deposit
    if not user_found:
        with open(temp_file if os.path.isfile(temp_file) else db_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, amount])
            
    #  Replace the old database with the updated one
    if os.path.isfile(temp_file):
        os.replace(temp_file, db_file)
        
    return True

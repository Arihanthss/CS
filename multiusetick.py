import csv
import os
import fare_calc

USERS_DB = "users.csv"
BALANCE_DB = "balance.csv"
ACTIVE_DB = "active_users.csv"

def check_card(username, passwdhash, current_station, stntype):
    # Auth
    if not os.path.isfile(USERS_DB):
        return (False, "SYSTEM ERROR.")

    authenticated = False
    with open(USERS_DB, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 2 and row[0] == username and row[1] == passwdhash:
                authenticated = True
                break
                
    if not authenticated:
        return (False, "INVALID CARD.")

    # tapin/depart
    if stntype == 0:
        if os.path.isfile(ACTIVE_DB):
            with open(ACTIVE_DB, mode='r') as file:
                for row in csv.reader(file):
                    if row and row[0] == username:
                        return (False, "ALREADY TAPPED IN.")
        
        with open(ACTIVE_DB, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, current_station])
            
        return (True, "GATE OPENED.")

    # tapout/arrival
    elif stntype == 1:
        if not os.path.isfile(ACTIVE_DB):
            return (False, "NO TAP-IN FOUND.")
            
        start_stn = None
        updated_active_users = []
        
        with open(ACTIVE_DB, mode='r') as file:
            for row in csv.reader(file):
                if row and row[0] == username:
                    start_stn = int(row[1])
                else:
                    updated_active_users.append(row)
                    
        if start_stn is None:
            return (False, "NO TAP-IN FOUND.")
            
        # using 0 as a incentive for smart cards or whats it called
        fare = fare_calc.calculate_fare(start_stn, current_station, 0)
        
        if os.path.isfile(BALANCE_DB):
            updated_balances = []
            user_found = False
            current_balance = 0
            
            with open(BALANCE_DB, mode='r') as file:
                for row in csv.reader(file):
                    if row and row[0] == username:
                        user_found = True
                        current_balance = int(float(row[1]))
                        # detucting balanxe omly if there is enough
                        if current_balance >= fare:
                            row[1] = str(current_balance - fare)
                    updated_balances.append(row)
            
            if not user_found:
                return (False, "WALLET NOT FOUND.")
                
            # insufficient money
            if current_balance < fare:
                shortfall = fare - current_balance
                # shortfall variable dictates the amount needed
                return (False, f"NEED ₹{shortfall} TO EXIT.")
                
            # exitting code following the core logic 
            with open(BALANCE_DB, mode='w', newline='') as file:
                csv.writer(file).writerows(updated_balances)
            with open(ACTIVE_DB, mode='w', newline='') as file:
                csv.writer(file).writerows(updated_active_users)
                
            return (True, f"GATE OPENED. ₹{fare} DEDUCTED.")

    return (False, "INVALID GATE TYPE.")

import csv
import os

TICKETS_DB = "tickets.csv"

def check_ticket(ticket_uuid, current_station, stntype):
    if not os.path.isfile(TICKETS_DB):
        return (False, "SYSTEM ERROR.")

    updated_rows = []
    gate_opened = False
    message = "INVALID TICKET."
    ticket_found = False

    with open(TICKETS_DB, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 4 and row[2] == ticket_uuid:
                ticket_found = True
                try:
                    start_stn = int(row[0])
                    end_stn = int(row[1])
                    status = int(row[3])
                except ValueError:
                    updated_rows.append(row)
                    continue
                
                
                if stntype == 0:
                    if current_station != start_stn:
                        message = "WRONG START STATION."
                    elif status != 0:
                        message = "TICKET ALREADY USED."
                    else:
                        row[3] = "1" 
                        gate_opened = True
                        message = "GATE OPENED."
                        
                
                elif stntype == 1:
                    if current_station != end_stn:
                        message = "WRONG DESTINATION."
                    elif status == 0:
                        message = "NEVER TAPPED IN."
                    elif status == 2:
                        message = "TICKET EXPIRED."
                    elif status == 1:
                        row[3] = "2" 
                        gate_opened = True
                        message = "GATE OPENED."
                        
            updated_rows.append(row)
            
    if not ticket_found:
        return (False, "TICKET NOT FOUND.")

    if gate_opened:
        with open(TICKETS_DB, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        return (True, message)

    return (False, message)

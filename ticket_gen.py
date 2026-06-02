import uuid
import csv
import os

def ticketgen(start, end):
    # UUID for unique ticks
    raw_uuid = str(uuid.uuid4())
    
    # 0:uuid is the format for identification
    qr_string = f"0:{raw_uuid}"
    
    # status =0 means unused 1 is in use 2 is used up
    status = 0
    
    # Assignment of file
    db_file = "tickets.csv"
    file_exists = os.path.isfile(db_file)
    
    # appending each new tickets
    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # In case of absence creates a file
        if not file_exists:
            writer.writerow(["Start", "End", "UUID", "Status"])
            
        #Writing in the format
        writer.writerow([start, end, raw_uuid, status])
        
    # this func returns only the string required for QR ticket gen
    return qr_string

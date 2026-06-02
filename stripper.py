import oneusetick
import multiusetick

def data_stripper(qr_string, current_station, stntype):
    parts = qr_string.split(":")
    
    if len(parts) < 2:
        return (False, "INVALID QR.")
        
    ticket_type = parts[0]
    
    #Relay to temp
    if ticket_type == "0":
        ticket_uuid = parts[1]
        return oneusetick.check_ticket(ticket_uuid, current_station, stntype)
            
    # Relay to multi
    elif ticket_type == "1":
        if len(parts) < 3:
            return (False, "INVALID CARD DATA.")
        username = parts[1]
        passwdhash = parts[2]
        return multiusetick.check_card(username, passwdhash, current_station, stntype)
        
    return (False, "INVALID QR.")

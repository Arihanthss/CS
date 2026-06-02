from flask import Flask, render_template, request, jsonify
import stripper

app = Flask(__name__)

@app.route('/')
def scanner_ui():
   
    return render_template('scanner.html')

@app.route('/process_scan', methods=['POST'])
def process_scan():
  
    try:
        # Using JSON data from qr to relay to respective modules
        data = request.json
        qr_string = data.get('qr_string', '')
        
        
        current_station = int(data.get('station_id'))
        stntype = int(data.get('gate_type')) # 0 for Departure, 1 for Arrival

        
        gate_success, display_message = stripper.data_stripper(qr_string, current_station, stntype)
        
        # Simple boolean used along with a message to be relayed
        return jsonify({"success": gate_success, "message": display_message})
            
    except Exception as e:
        # Failsafe in case bad data is sent or hardware disconnects
        print(f"Server Error during scan: {e}")
        return jsonify({"success": False, "message": "SYSTEM ERROR."})

if __name__ == '__main__':
    # the name=main checks if this is run as a standalone program
    print("Starting Station Scanner Terminal on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=True)

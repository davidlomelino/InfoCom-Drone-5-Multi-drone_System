from flask import Flask, request
from flask_cors import CORS
import redis
import json


app = Flask(__name__)
CORS(app)

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis(host="localhost", port=6379, decode_responses=True, charset="unicode_escape")
# ===============================================

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json()
    droneIP = request.remote_addr
    droneID = drone['id']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    # Get the infomation of the drone in the request, and update the information in Redis database
    # Data that need to be stored in the database: 
    # Drone ID, logitude of the drone, latitude of the drone, drone's IP address, the status of the drone
    # Note that you need to store the metioned infomation for all drones in Redis, think carefully how to store them
    # =========================================================================================
    drones = redis_server.smembers('drones')
    if droneID and droneID not in drones:
        redis_server.sadd('drones', droneID)
        
    droneData = {
        'id': droneIP,
        'longitude': drone_longitude,
        'latitude': drone_latitude,
        'status': drone_status
        }
    
    redis_server.hmset(droneID, droneData)
    #redis_server.hmset('drones', droneData)
    #redis_server.sadd('drones', droneData)
    
    return 'Get data'
    #return f"Drönare {droneID} uppdaterad i databasen"

    #long1 lat1
    #lat1 lat2
    #stat1 stat2
    #id1 id2
    
    #if id == id1
    #if stat1 == free
     #   hämta long1 och lat1
      #  och id1
        
    
        
     # =======================================================================================
    

if __name__ == "__main__":


    app.run(debug=True, host='0.0.0.0', port='5001')

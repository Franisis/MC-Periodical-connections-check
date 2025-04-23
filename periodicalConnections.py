import os
import time
from dotenv import load_dotenv
from mcstatus import MinecraftServer
import subprocess

load_dotenv()

SERVER_ADDRESS= os.getenv('SERVER_ADDRESS')
SERVER_PORT= os.getenv('SERVER_PORT')
VM_NAME=os.getenv('VM_NAME')
ZONE= os.getenv('ZONE')
PROJECT_ID=os.getenv('PROJECT_ID')
TIME_WO_PLAYERS = 0
THRESHOLD = 30

while True:
    try:
        server = MinecraftServer.lookup(f"{SERVER_ADDRESS}:{SERVER_PORT}")
        status = server.status()
        if status.players.online == 0:
            TIME_WO_PLAYERS += 1
            print(f"NO PLAYERS. TIME W/O PLAYERS: {TIME_WO_PLAYERS} minutes")
        else:
            TIME_WO_PLAYERS = 0
            print(f"Connected users: {status.players.online}")
        
        if TIME_WO_PLAYERS >= THRESHOLD:
            print("TURNING OFF VM")
            subprocess.run([
                "gcloud", "compute", "instances", "stop",
                f"{VM_NAME}", "--zone", f"{ZONE}", "--project", f"{PROJECT_ID}"
            ])
            break
        
        time.sleep(60*10) #Time before the script checks the server again.
    except Exception as e:
        print(f"Could not continue with the process because of: {e}")

from valclient.client import Client
import psutil
import os
import time 

# Customizable Settings

LOOP_DELAY = 0.4; 
LOCK_DELAY = 0.1;
HOVER_DELAY = 0.0;
REGIONCODE = None; 
AGENTCODE = None; 

# Globals 

SETTINGS = None; 
SEEN_MATCHES = [];
RUNNING = False;


# Agent & Region dictionaries 

AGENT_CODES = {
    "1": "add6443a-41bd-e414-f6ad-e58d267f4e95", # Jett
    "2": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc", # Reyna
    "3": "f94c3b30-42be-e959-889c-5aa313dba261", # Raze
    "4": "7f94d92c-4234-0a36-9646-3a87eb8b5c89", # Yoru
    "5": "eb93336a-449b-9c1b-0a54-a891f7921d69", # Phoenix
    "6": "bb2a4828-46eb-8cd1-e765-15848195d751", # Neon
    "7": "5f8d3a7f-467b-97f3-062c-13acf203c006", # Breach 
    "8": "6f2a04ca-43e0-be17-7f36-b3908627744d", # Skye  
    "9": "320b2a48-4d9b-a075-30f1-1f93a9b638fa", # Sova
    "10": "601dbbe7-43ce-be57-2a40-4abd24953621", # Kayo
    "11": "1e58de9c-4950-5125-93e9-a0aee9f98746", # Killjoy 
    "12": "117ed9e3-49f3-6512-3ccf-0cada7e3823b", # Cypher 
    "13": "569fdd95-4d10-43ab-ca70-79becc718b46", # Sage 
    "14": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7", # Chamber 
    "15": "8e253930-4c05-31dd-1b6c-968525494517", # Omen
    "16": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417", # Brimstone 
    "17": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf", # Astra 
    "18": "707eab51-4836-f488-046a-cda6bf494859", # Viper 
    "19": "dade69b4-4f5a-8528-247b-219e5a1facd6", # Fade
    "20": "95b78ed7-4637-86d9-7e41-71ba8c293152", # Harbor 
    "21": "e370fa57-4757-3604-3648-499e1f642d3f", # Gekko 
    "22": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235" # Deadlock 
};

REGIONS = {
    "1" : "na",
    "2" : "latam",
    "3" : "br", 
    "4" : "eu", 
    "5" : "ap", 
    "6" : "kr",
    "7" : "pbe"
};

def get_Settings(): # stores the Agent Code and the player Region
    global REGIONCODE 
    global AGENTCODE

    if (input("Would you like to change settings? y/n\n").lower() == 'y'): 
        REGIONCODE = input("Enter Region:\n[1] North America\n[2] Latin America\n[3] Brazil\n[4] Europe\n[5] Asia Pacific\n[6] Korea\n[7] Pbe\nEnter Number: ");
        AGENTCODE = AGENT_CODES[input("Enter Agent:\n[1] Jett\n[2] Reyna\n[3] Raze\n[4] Yoru\n[5] Phoenix\n[6] Neon\n[7] Breach\n[8] Skye\n[9] Sova\n[10] Kayo\n[11] Killjoy\n[12] Cypher\n[13] Sage\n[14] Chamber\n[15] Omen\n[16] Brimstone\n[17] Astra\n[18] Viper\n[19] Fade\n[20] Harbor\n[21] Gekko\n[22] Deadlock\nEnter Number: ")]; 
        with open(os.getcwd() + "\\Settings.txt", "w") as f: # Updates the file with the settings
            f.write(REGIONCODE + "\n" + AGENTCODE);     
    else: 
        try: 
            with open(os.getcwd() + "\\Settings.txt", "r") as f:     
                REGIONCODE = f.readline()[0:-1];
                AGENTCODE = f.readline();     
        except FileNotFoundError as e: 
            print("Settings file doesn't exist, Please try again. (If it's first time you must edit settings)");
            get_Settings();
    print(REGIONS[REGIONCODE]) # type: ignore
    print(AGENTCODE)
   
def try_Lock(): 
    global RUNNING
    global SETTINGS
    global SEEN_MATCHES

    if not "VALORANT.exe" in (p.name() for p in psutil.process_iter()): # Checks windows process to see if valorant is running
        if RUNNING: # Stops Checking for pre-game
            RUNNING = False; 
        print("Valorant Client not detected, please open client.");
        return None; 

    try: 
        client = Client(region = REGIONS[REGIONCODE]);  # type: ignore
    except ValueError:
        print("Connection to client failed.")
        RUNNING = False; 
        return;

    client.activate();

    RUNNING = True; # Initiating Loop

    print("STARTED SEARCHING FOR MATCH")

    while RUNNING: 

        time.sleep(LOOP_DELAY); # Loop delay

        if not RUNNING: 
            return; 
    
        try: 

            sessionState = client.fetch_presence(client.puuid)['sessionLoopState']; # Checks to see if your online in Valorant
            matchID = client.pregame_fetch_match()['ID']; # Grabs the pre-game ID   

            print(sessionState)

            if (sessionState == "PREGAME" and matchID not in SEEN_MATCHES):  # Making sure not a game thats been seen before 
                SEEN_MATCHES.append(matchID); 

                print("FOUND MATCH")

                time.sleep(HOVER_DELAY); # Creates a delay if you want

                client.pregame_select_character(AGENTCODE); # type: ignore

                print("SELCECTED CHARACTER")

                time.sleep(LOCK_DELAY); # Lock Delay
                client.pregame_lock_character(AGENTCODE); # type: ignore

                RUNNING = False; # Finished, stops the loop 

                print("LOCKED IN CHARACTER")

                return True;
    
        except Exception as e: 
            if "pre-game" not in str(e): 
                RUNNING = False; 
                print("Trouble finding game. ERROR")
                return; 

def main():
    global SETTINGS 
    SETTINGS = get_Settings(); 

    print("Starting Program.")
    
    while not try_Lock(): 
        break;  

    print("Program Finished")

if __name__ == "__main__": 
    main() 
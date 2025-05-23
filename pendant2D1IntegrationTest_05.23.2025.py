#*********************************** GERMAN ******************************************************
#Steuerung einer Einzelachse

#Laden Sie nach dem Neustart der D1 die Konfigurationsdatei. Stellen Sie dann sicher, dass Modbus TCP-Gateway im Fahrprofil und die Modbus TCP-Kommunikation aktiviert ist, bevor Sie eine Bewegung mit der D1 ausführen. 
#Es muss die mitgelieferte dryve D1 Konfigurationen geladen sein: 20201204 D1-1-RaspberryPI-ModbusTCP(GW).txt
#Die IP Adresse der dryve D1 muss mit der unter "s.connect" eingetragenen IP Adresse übereinstimmen. 
#Im Programm können alle Bewegungsparameter angepasst werden. Z.B. Geschwindigkeit, Beschleunigung oder die Strecke.

#Es müssen zum ablaufen des Programms Start und Stoptaster an die digitalen Eingänge 1 und 2 angeschlossen werden.

#Bitte immer die neueste Firmware von der Webseite www.igus.de/dryve verwenden!!!

#Für das Musterprogram wird kein Support bereitgestellt.
#Ebenfalls wird keine Verantwortung/Haftung für das Programm übernommen.

#*********************************** English *****************************************************
#Single axis control

#After restarting the D1, load the configuration file. Then make sure that the Modbus TCP gateway in the drive profile and that Modbus TCP communication is activated before you perform a movement with the D1.
#The supplied dryve D1 configuration must be loaded: 20201204 D1-1-RaspberryPI-ModbusTCP(GW).txt
#The IP address of the dryve D1 must match with the IP address stated at "s.connect".
#All movement parameter can be adopted. E.g. speed, acceleration or position.

#Start and stop buttons must be connected to digital inputs 1 and 2 to run the program.

#Please use the latest firmware available at www.igus.eu/dryve!!!

#No support is provided for this sample program.
#No responsibility/liability will be assumed for the test program.




#Bibliotheken importieren
#Import libraries 
import socket
import time
import sys


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

pin0 = 11
pin1 = 5
pin2 = 6
pin3 = 13
pin4 = 19
pin5 = 26

GPIO.setup(pin0,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin5,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


#Bus-Verbindung herstellen
#Establish bus connection
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print ('failed to create sockt')
    
s.connect(("169.254.0.1", 502))
print ('Socket created')
#Wird beim Ausfuehren des Programms nur der Speicherort und der Programmname in der Shell angezeigt, so sind die IP Adressen des Programms und der dryve D1 nicht uebereinstimmend
#When executing the program and the shell displays the storing folder and the program name, the set IP address in the program and the dryve D1 doesn't match




#Durchlauf State Machine (Handbuch: Visualisieung State Machine) 
#State Machine pass through (Manual: Visualisation State Machine)

# Digitale Eingänge 60FDh
# digital inputs
DInputs = [0, 0, 0, 0, 0, 13, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4]  
DInputs_array = bytearray(DInputs)
print(DInputs_array)


# Statusword 6041h
# Status request
status = [0, 0, 0, 0, 0, 13, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2]
status_array = bytearray(status)
print(status_array)

# Controlword 6040h
# Command: Shutdown
shutdown = [0, 0, 0, 0, 0, 15, 0, 43, 13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 6, 0]
shutdown_array = bytearray(shutdown)
print(shutdown_array)

# Controlword 6040h
# Command: Switch on
switchOn = [0, 0, 0, 0, 0, 15, 0, 43, 13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 7, 0]
switchOn_array = bytearray(switchOn)
print(switchOn_array)

# Controlword 6040h
# Command: enable Operation
enableOperation = [0, 0, 0, 0, 0, 15, 0, 43,13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 15, 0]
enableOperation_array = bytearray(enableOperation)
print(enableOperation_array)

# Controlword 6040h
# Command: stop motion
stop = [0, 0, 0, 0, 0, 15, 0, 43,13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 15, 1]
stop_array = bytearray(stop)
print(stop_array)

# Controlword 6040h
# Command: reset dryve
reset = [0, 0, 0, 0, 0, 15, 0, 43,13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 0, 1]
reset_array = bytearray(reset)
print(reset_array)

# Variablen einen Startwert geben
# Variables start value
start = 0
ref_done = 0
error = 0

#Definition der Funktion zum Senden und Empfangen von Daten
#Definition of the function to send and receive data 
def sendCommand(data):
    #Socket erzeugen und Telegram senden
    #Create socket and send request
    s.send(data)
    res = s.recv(24)
    #Ausgabe Antworttelegram 
    #Print response telegram
    # ~ print(list(res))
    return list(res)

#Shutdown Controlword senden und auf das folgende Statuswort pruefen. Pruefung auf mehrer Statuswords da mehrere Szenarien siehe Bit assignment Statusword, data package im Handbuch 
#sending Shutdown Controlword and check the following Statusword. Checking several Statuswords because of various options. look at Bit assignment Statusword, data package in user manual 
def set_shdn():
    sendCommand(reset_array)
    sendCommand(shutdown_array)
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 33, 6]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 33, 22]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 33, 2]):
        print("wait for shdn")

        #1 Sekunde Verzoegerung
        #1 second delay
        time.sleep(1)

#Switch on Disabled Controlword senden und auf das folgende Statuswort pruefen. Pruefung auf mehrer Statuswords da mehrere Szenarien siehe Bit assignment Statusword, data package im Handbuch 
#sending Switch on Disabled Controlword and check the following Statusword. Checking several Statuswords because of various options. look at Bit assignment Statusword, data package in user manual 
def set_swon():
    sendCommand(switchOn_array)
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 35, 6]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 35, 22]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 35, 2]):
        print("wait for sw on")

        time.sleep(1)

#Operation Enable Controlword senden und auf das folgende Statuswort pruefen. Pruefung auf mehrer Statuswords da mehrere Szenarien siehe Bit assignment Statusword, data package im Handbuch 
#Operation Enable Controlword and check the following Statusword. Checking several Statuswords because of various options. look at Bit assignment Statusword, data package in user manual 
def set_op_en():
    sendCommand(enableOperation_array)
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 6]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 22]
           and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 2]):
        print("wait for op en")

        time.sleep(1)

def init():

    #Aufruf der Funktion sendCommand zum hochfahren der State Machine mit vorher definierten Telegrammen (Handbuch: Visualisieung State Machine)
    #Call of the function sendCommand to start the State Machine with the previously defined telegrams (Manual: Visualisation State Machine)
    set_mode(1)
    sendCommand(reset_array)
    set_shdn()
    set_swon()
    set_op_en()



def set_mode(mode):

    #Setzen der Operationsmodi im Objekt 6060h Modes of Operation
    #Set operation modes in object 6060h Modes of Operation
    sendCommand(bytearray([0, 0, 0, 0, 0, 14, 0, 43, 13, 1, 0, 0, 96, 96, 0, 0, 0, 0, 1, mode]))
    while (sendCommand(bytearray([0, 0, 0, 0, 0, 13, 0, 43, 13, 0, 0, 0, 96, 97, 0, 0, 0, 0, 1])) != [0, 0, 0, 0, 0, 14, 0, 43, 13, 0, 0, 0, 96, 97, 0, 0, 0, 0, 1, mode]):

        print("wait for mode")

        time.sleep(0.1)

def homing ():
    #Zurücksetzen des Startbits im Controlword
    #Reset the start bit in Controlword
    sendCommand(enableOperation_array)
    #Parametrierung der Objekte gemäß Handbuch
    #Parameterization of the objects according to the manual
    #6060h Modes of Operation
    #Setzen auf Homing Modus (see "def set_mode(mode):"; Byte 19 = 6)
    #Set Homing mode (see "def set_mode(mode):"; Byte 19 = 6)
    set_mode(6)
    # 6092h_01h Feed constant Subindex 1 (Feed)
    #Setzen des Vorschubs auf den Wert 5400 (nach Achse im Video); vgl. Handbuch  (Byte 19 = 24; Byte 20 = 21; Byte 21 = 0; Byte 22 = 0)
    #Set feed constant to 5400 (axis in Video); refer to manual (Byte 19 = 24; Byte 20 = 21; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 146, 1, 0, 0, 0, 4, 24, 21, 0, 0]))
    # 6092h_02h Feed constant Subindex 2 (Shaft revolutions)
    #Setzen der Wellenumdrehung auf 1; vgl. Handbuch (Byte 19 = 1; Byte 20 = 0; Byte 21 = 0; Byte 22 = 0)
    #Set shaft revolutions to 1; refer to manual (Byte 19 = 1; Byte 20 = 0; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 146, 2, 0, 0, 0, 4, 1, 0, 0, 0]))
    # 6099h_01h Homing speeds Switch
    #Vorgabe der Verfahrgeschwindigkeit beim Suchen auf den Schalter wird auf 60 U/min gesetzt (Byte 19 = 112; Byte 20 = 23; Byte 21 = 0; Byte 22 = 0)
    #Speed during search for switch is set to 60 rpm (Byte 19 = 112; Byte 20 = 23; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 153, 1, 0, 0, 0, 4, 112, 23, 0, 0]))
    # 6099h_02h Homing speeds Zero
    #Setzen Verfahrgeschwindigkeit beim Suchen von Null auf 60 U/min (Byte 19 = 112; Byte 20 = 23; Byte 21 = 0; Byte 22 = 0)
    #Set speed during Search for zero to 60 rpm (Byte 19 = 112; Byte 20 = 23; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 153, 2, 0, 0, 0, 4, 112, 23, 0, 0]))
    # 609Ah Homing acceleration
    #Setzen der Refernzfahrt-Beschleunigung wird auf 1000 U/min² (Byte 19 = 160; Byte 20 = 134; Byte 21 = 1; Byte 22 = 0)
    #Set Homing acceleration to 1000 rpm/min² (Byte 19 = 160; Byte 20 = 134; Byte 21 = 1; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 154, 0, 0, 0, 0, 4, 160, 134, 1, 0]))
    # 6040h Controlword
    #Start Homing
    sendCommand(bytearray([0, 0, 0, 0, 0, 15, 0, 43, 13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 31, 0]))
    #Check Statusword nach Referenziert Signal und ob ein Fehler in der D1 passiert
    #Check Statusword for signal referenced and if an error in the D1 comes up
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 22]
        and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]
        and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 34]
        and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 2]):
            #Wenn der Stoptaster gedrückt wird soll die Kette unterbrechen
            #If the StopButton is pushed the loop breaks
            if sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]:
                break
            time.sleep(0.1)
            print ("Homing")

  
  
def movement_A ():  
    
    sendCommand(enableOperation_array)

    # 6081h Profile Velocity
    #Setzen der Geschwindigkeit auf 150 U/min (Byte 19 = 152; Byte 20 = 58; Byte 21 = 0; Byte 22 = 0)
    #Set velocity to 150 rpm (Byte 19 = 152; Byte 20 = 58; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 129, 0, 0, 0, 0, 4, 152, 58, 0, 0]))

    # 6083h Profile Acceleration
    #Setzen der Beschleunigung auf 500 U/min² (Byte 19 = 80; Byte 20 = 195; Byte 21 = 0; Byte 22 = 0)
    #Set acceleration to 500 rpm/min² (Byte 19 = 80; Byte 20 = 195; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 131, 0, 0, 0, 0, 4, 80, 195, 0, 0]))
    

    # 607A Target Position
    #Setzen sie einer Zielposition auf den Wert 0mm (Byte 19 = 0; Byte 20 = 0; Byte 21 = 0; Byte 22 = 0)
    #Set target position to 0mm (Byte 19 = 0; Byte 20 = 0; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 122, 0, 0, 0, 0, 4, 0, 0, 0, 0]))
    
    #Startbefehl zur Bewegung des Motors über Bit 4 
    #Set Bit 4 true to excecute the movoment of the motor 
    sendCommand(bytearray([0, 0, 0, 0, 0, 15, 0, 43, 13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 31, 0]))
    
    print("go")
    
    time.sleep(0.1)
    #Check Statusword nach Referenziert Signal und ob ein Fehler in der D1 passiert
    #Check Statusword for signal referenced and if an error in the D1 comes up
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 22]
        and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]):
            #Wenn der Stoptaster gedrückt wird soll die Kette unterbrechen
            #If the StopButton is pushed the loop breaks
            if sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]:
                break
            time.sleep(0.1)
            print ("Motion A")
        

  
 
def abs(position, velocity):  
    
    sendCommand(enableOperation_array)

    # 6081h Profile Velocity
    print("VELOCITY")
    mmPRev = 54
    mmps = velocity
    print("mm/s: ", mmps)
    rpm = int((mmps/mmPRev)*60*100)
    print("rpm: ", rpm)
    rpmHexa = hex(rpm)
    print("hex: ", rpmHexa)
    rpmHexaStr = str(rpmHexa[2:])
    print("hexaStr: ", rpmHexaStr)
    rpmHexaStrZ = rpmHexaStr.zfill(8)
    print("hexaStrZ: ", rpmHexaStrZ)
    vByte19 = int(rpmHexaStrZ[6:8],16)
    vByte20 = int(rpmHexaStrZ[4:6],16)
    vByte21 = int(rpmHexaStrZ[2:4],16)
    vByte22 = int(rpmHexaStrZ[0:2],16)
    print("velocity byte 19: ", rpmHexaStrZ[6:8],vByte19)
    print("velocity byte 20: ", rpmHexaStrZ[4:6],vByte20)
    print("velocity byte 21: ", rpmHexaStrZ[2:4],vByte21)
    print("velocity byte 22: ", rpmHexaStrZ[0:2],vByte22)
    print("--------------------------------")
    
    #Setzen der Geschwindigkeit auf 150 U/min (Byte 19 = 152; Byte 20 = 58; Byte 21 = 0; Byte 22 = 0)
    #Set velocity to 150 rpm (Byte 19 = 152; Byte 20 = 58; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 129, 0, 0, 0, 0, 4, vByte19, vByte20, vByte21, vByte22]))
    # ~ sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 129, 0, 0, 0, 0, 4, 152, 58, 0, 0]))

    # 6083h Profile Acceleration
    #Setzen der Beschleunigung auf 500 U/min² (Byte 19 = 80; Byte 20 = 195; Byte 21 = 0; Byte 22 = 0)
    #Set acceleration to 500 rpm/min² (Byte 19 = 80; Byte 20 = 195; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 131, 0, 0, 0, 0, 4, 80, 195, 0, 0]))
    

    # 607A Target Position
    print("POSITION")
    mm = int(position)
    print("mm: ", mm)
    mmx100 = mm*100
    print("mm * 100: ", mmx100)
    hexa = hex(mmx100)
    print("hex: ", hexa)
    hexaStr = str(hexa[2:])
    print("hexaStr: ", hexaStr)
    hexaStrZ = hexaStr.zfill(8)
    print("hexaStrZ: ", hexaStrZ)
    pByte19 = int(hexaStrZ[6:8],16)
    pByte20 = int(hexaStrZ[4:6],16)
    pByte21 = int(hexaStrZ[2:4],16)
    pByte22 = int(hexaStrZ[0:2],16)
    print("position byte 19: ", hexaStrZ[6:8],pByte19)
    print("position byte 20: ", hexaStrZ[4:6],pByte20)
    print("position byte 21: ", hexaStrZ[2:4],pByte21)
    print("position byte 22: ", hexaStrZ[0:2],pByte22)
    print("--------------------------------")
    
    #Setzen sie einer Zielposition auf den Wert 250mm (Byte 19 = 168; Byte 20 = 97; Byte 21 = 0; Byte 22 = 0)
    #Set target position to 250mm (Byte 19 = 168; Byte 20 = 97; Byte 21 = 0; Byte 22 = 0)
    sendCommand(bytearray([0, 0, 0, 0, 0, 17, 0, 43, 13, 1, 0, 0, 96, 122, 0, 0, 0, 0, 4, pByte19, pByte20, pByte21, pByte22]))
    
    #Startbefehl zur Bewegung des Motors über Bit 4 
    #Set Bit 4 true to excecute the movoment of the motor 
    sendCommand(bytearray([0, 0, 0, 0, 0, 15, 0, 43, 13, 1, 0, 0, 96, 64, 0, 0, 0, 0, 2, 31, 0]))
        
    time.sleep(0.1)

    #Check Statusword nach Referenziert Signal und ob ein Fehler in der D1 passiert
    #Check Statusword for signal referenced and if an error in the D1 comes up
    while (sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 39, 22]
        and sendCommand(status_array) != [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]):
            #Wenn der Stoptaster gedrückt wird soll die Kette unterbrechen
            #If the StopButton is pushed the loop breaks
            if sendCommand(DInputs_array) == ([0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0] 
            or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]):
                break
            if isError(): break
            time.sleep(0.1)
        
            
#Beginn Hauptprogramm
#Start main programm
#Abfrage ob Fehler in D1 vorliegt
#Ask if there is an Error on D1            
# ~ if (sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]
    # ~ or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]
    # ~ or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 34]
    # ~ or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 2] ):
        # ~ error = 1
# ~ else: 
    # ~ error = 0

def isError():
    if (sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]
    or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]
    or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 34]
    or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 2] ):
        error = 1
        return True
    else: 
        error = 0
        return False

#Wenn kein Fehler start der Initialisierung
#If no Error is up start the initialisierung    
if error == 0:
    init()
    time.sleep(0.5)
    #Sollange kein Fehler vorliegt wird auf einen Startbefehl gewartet
    #If there is no error, the system waits for a start command
    while error == 0:        
        #start = 1 ###TEST
        if sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 65, 0]:
            start = 1
            
        time.sleep(0.1)
        #Wenn Start gedrückt beginn des Homings
        #When Start is pressed start of the homing
        while start == 1:
            homing()
            #Abfrage ob jemand während des Homings stopt hat oder ein Fehler aufgetreten ist
            #Query whether someone has stopped during the homings or an error has occurred
            if (sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 34]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 2] ):
                    break
                    
            ref_done = 1
            #6060h Modes of Operation
            #Setzen auf Profile Position Mode (see "def set_mode(mode):"; Byte 19 = 1)
            #Set Profile Position Mode (see "def set_mode(mode):"; Byte 19 = 1)
            set_mode(1)
            #Solange Referenziert wird die Normale Bewegung gestartet.
            #For as long as referenced, the normal movement is started.
            while ref_done == 1:
                if isError(): break
                #Wenn während der Fahrt A gestopt wird oder ein Fehler aufgetreten ist wird die Schleife unterbrochen
                #If Movement is stopped while driving or an error has occurred, the loop is interrupted
                if (sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]
                    or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]):
                        break
                
                #Aufruf der Bewegung A
                #Call Movement A
                movement_A()
                time.sleep(0.5)
                
                b0 = GPIO.input(pin0)
                b1 = GPIO.input(pin1)
                b2 = GPIO.input(pin2)
                b3 = GPIO.input(pin3)
                b4 = GPIO.input(pin4)
                b5 = GPIO.input(pin5)
                bits = [b3,b2,b1,b0]
                bits = [str(b) for b in bits]
                binary = "".join(bits)
                index = int(binary,2)
                print(index)                
                
                #Aufruf der Bewegung B
                #Call Movement B
                abs(index*10, 50)
  
            #Wenn während der normalen Bewegungen die Fahrt gestopt wird oder ein Fehler aufgetreten ist wird die Schleife unterbrochen
            #If Motionbstopped while driving or an error has occurred, the loop is interrupted
            if (sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]):
                    break
              
        #Wenn gestopt wurde wird die Bewegung angehalten
        #If stopped, the movement is stopped         
        if sendCommand(DInputs_array) == [0, 0, 0, 0, 0, 17, 0, 43, 13, 0, 0, 0, 96, 253, 0, 0, 0, 0, 4, 8, 0, 66, 0]:
            start = 0
            sendCommand(stop_array)
        #Wenn ein Fehler aufgetreten ist wird die Schleife unterbrochen
        #If an error has occurred, the loop is interrupted    
        if (sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 22]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 6]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 34]
                or sendCommand(status_array) == [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 2]):
                error = 1
                break
        print ("Wait for Start")
   
print("Error on D1")







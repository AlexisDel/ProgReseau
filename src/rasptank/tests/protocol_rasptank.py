import paho.mqtt.client as mqtt

def processFlagMessage(querry, verbose=False):
	
	if querry == "START_CATCHING":
		if verbose:
			print("Start catching")

	elif querry == "NOT_ONBASE":
		if verbose:
			print("Flag not on base")

	elif querry == "ABORT_CATCHING_EXIT":
		if verbose:
			print("Abort catching, you leaved the flag area")
			
	elif querry == "ABORT_CATCHING_SHOT":
		if verbose:
			print("Abort catching, you got shot")

    elif querry == "FLAG_CATCHED":
        if verbose:
            print("Flag catched")

	elif querry == "FLAG_LOST":
		if verbose:
			print("Flag lost, you got shot")

	elif querry == "ALREADY_GOT":
		if verbose:
			print("You've alreay catched the flag")

	elif querry == "FLAG_DEPOSITED":
		if verbose:
			print("Flag deposited")

	elif querry == "NO_FLAG":
		if verbose:
			print("There is no flag to deposit")

def processCommand(client, userdata, message):
	"""	
    Manage and process all messages received via the MQTT protocol
    """

	global team, qr_code, init, direction_command, turn_command

    # Message received (decoded as a string)
	querry = str(message.payload.decode("utf-8"))
    
    ##############################
    #       Initialisation       #
    ##############################
	if message.topic[21:] == "init":
		querry = querry.split(" ")
		if querry[0] == "TEAM":
			print("TEAM :", querry[1])
		elif querry[0] == "QR_CODE":
			print("QRCODE TO SCAN :", querry[1])
		elif querry[0] == "END":
			print("INIT DONE")
	#############################
    #           Flag            #
    #############################
	elif message.topic[21:] == "flag":
		processFlagMessage(querry)
    

# MQTT Client
client = mqtt.Client()
client.connect("10.3.141.1") # A CHANGER
client.subscribe("tanks/"+hex(tankID)+"/#")
client.on_message = processCommand
client.loop_start()

# INIT
client.publish("init", "INIT "+hex(tankID))






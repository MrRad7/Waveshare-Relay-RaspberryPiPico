# This is CircuitPython code to control a WaveShare relay board with a Raspberry Pi Pico
# The commands are sent and received via USB.  Output is in JSON format.
# Mike S.  09/16/2023
#
import board
import digitalio
import time
import json
import supervisor
from collections import OrderedDict

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

ch1 = digitalio.DigitalInOut(board.GP21)
ch1.direction = digitalio.Direction.OUTPUT
ch2 = digitalio.DigitalInOut(board.GP20)
ch2.direction = digitalio.Direction.OUTPUT
ch3 = digitalio.DigitalInOut(board.GP19)
ch3.direction = digitalio.Direction.OUTPUT
ch4 = digitalio.DigitalInOut(board.GP18)
ch4.direction = digitalio.Direction.OUTPUT
ch5 = digitalio.DigitalInOut(board.GP17)
ch5.direction = digitalio.Direction.OUTPUT
ch6 = digitalio.DigitalInOut(board.GP16)
ch6.direction = digitalio.Direction.OUTPUT
ch7 = digitalio.DigitalInOut(board.GP15)
ch7.direction = digitalio.Direction.OUTPUT
ch8 = digitalio.DigitalInOut(board.GP14)
ch8.direction = digitalio.Direction.OUTPUT

on = 1
off = 0

# relays dict for tracking relay states
relays = {
    '1' : 0,
    '2' : 0,
    '3' : 0,
    '4' : 0,
    '5' : 0,
    '6' : 0,
    '7' : 0,
    '8' : 0}

status_dict = {}


print ("Raspberry Pi Pico Relay Controller is starting....")
led.value = True

#ch1.value(1)
#print(ch1.value)
#ch1.value = True


def update_relays_dict():
    """updates the relays dictionary to reflect the current state of the GPIO pins.

    Args:
        none

    Returns:
        none
        Updates a global dictionary
    """

    for i in range(1, 9): #update relays 1 -8
        state = get_relay_state(int(i))
        relays[str(i)] = state


def get_relay_state(relay):
    """gets the current state of a relay.  0 = off  1 = on

    Args:
        relay (int): the relay to get the state of

    Returns:
        state : the current state 0 = off  1 = on  -1 = error
    """
    relay = int(relay)
    state = -1 #this indicates an error

    if relay == 1:
        state = ch1.value
        #relays[str(relay)] = state
    elif relay == 2:
        state = ch2.value
        #relays[str(relay)] = state
    elif relay == 3:
        state = ch3.value
        #relays[str(relay)] = state
    elif relay == 4:
        state = ch4.value
        #relays[str(relay)] = state
    elif relay == 5:
        state = ch5.value
        #relays[str(relay)] = state
    elif relay == 6:
        state = ch6.value
        #relays[str(relay)] = state
    elif relay == 7:
        state = ch7.value
        #relays[str(relay)] = state
    elif relay == 8:
        state = ch8.value
        #relays[str(relay)] = state
    else:
        print('Invalid relay!')
        state = -1

    return state



def change_relay_state(relay, state):
    """changes the current state of a relay.

    Args:
        relay (int): the relay to change the state of.
        state (int): the state to change the relay to.  0 = off  1 = on

    Returns:
        none
    """
    relay = int(relay)
    state = int(state)

    if relay == 1:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch1.value = state
    elif relay == 2:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch2.value = state
    elif relay == 3:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch3.value = state
    elif relay == 4:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch4.value = state
    elif relay == 5:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch5.value = state
    elif relay == 6:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch6.value = state
    elif relay == 7:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch7.value = state
    elif relay == 8:
        #print('Changing ' + str(relay) + ' to ' + str(state))
        ch8.value = state
    else:
        print('Not doing anything!')

    update_relays_dict()


def turn_off_all_relays():
    """turns off all relays.

    Args:
        none

    Returns:
        none
    """
    for i in range(1, 9): #turn off 1 -8
        #print('i = ' + str(i))
        change_relay_state(i, 0)
        time.sleep(0.25) #sleep for half second
    update_relays_dict()


def turn_on_all_relays():
    """turns off all relays.

    Args:
        none

    Returns:
        none
    """
    for i in range(1, 9): #turn off 1 -8
        #print('i = ' + str(i))
        change_relay_state(i, 1)
        time.sleep(0.25) #sleep for half second
    update_relays_dict()



def send_status():
    update_relays_dict()

    status_dict.clear() #clear out old status in global variable

    for key in sorted(relays):
        if relays[key] == 0:
            relay_state = 'OFF'
        elif relays[key] == 1:
            relay_state = 'ON'
        else:
            relay_state = 'UNK'

        relay_name = 'Relay-'
        relay_number = "{:0>{}}".format(key, 2) #add leding zeros if needed
        relay_name = relay_name + relay_number
        #print('Relay name = ', relay_name)

        status_dict[relay_name] = relay_state



    #json_response = json.dumps(status_dict)

    # the rest of this is just creating a properly sorted dictionary to return
    temp_list = []
    sorted_dict = OrderedDict()

    for key, value in status_dict.items():
        temp_list.append(key)



    for item in sorted(temp_list):
        sorted_dict[item] = status_dict[item]

    json_response = json.dumps(sorted_dict)
    print(json_response)

    return 0


def send_heartbeat():
    heartbeat_dict = {"status" : "working"}
    json_response = json.dumps(heartbeat_dict)
    print(json_response)

    return 0


def process_serial_request(request):
    #request_items = str(request).split('/')
    #relay_code = request_items[-1]
    retval = 0 #0 for relay updates, 1 for status
    relay_code = request
    #print('Relay code = ', relay_code)

    if str(relay_code) == '42': #status request
        send_status()
        retval = 1
    elif str(relay_code) == '43': #status request
        send_status()
        retval = 1
    elif str(relay_code) == '00':
        change_relay_state(1, 0)
    elif str(relay_code) == '01':
        change_relay_state(1, 1)
    elif str(relay_code) == '02':
        change_relay_state(2, 0)
    elif str(relay_code) == '03':
        change_relay_state(2, 1)
    elif str(relay_code) == '04':
        change_relay_state(3, 0)
    elif str(relay_code) == '05':
        change_relay_state(3, 1)
    elif str(relay_code) == '06':
        change_relay_state(4, 0)
    elif str(relay_code) == '07':
        change_relay_state(4, 1)
    elif str(relay_code) == '08':
        change_relay_state(5, 0)
    elif str(relay_code) == '09':
        change_relay_state(5, 1)
    elif str(relay_code) == '10':
        change_relay_state(6, 0)
    elif str(relay_code) == '11':
        change_relay_state(6, 1)
    elif str(relay_code) == '12':
        change_relay_state(7, 0)
    elif str(relay_code) == '13':
        change_relay_state(7, 1)
    elif str(relay_code) == '14':
        change_relay_state(8, 0)
    elif str(relay_code) == '15':
        change_relay_state(8, 1)
    elif str(relay_code) == '44':
        turn_off_all_relays()
    elif str(relay_code) == '50':
        send_heartbeat()

    return retval


turn_off_all_relays()
#turn_on_all_relays()



##################################################
while True:

    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if value == "":
            continue
        #print("RX: {}".format(value))
        process_serial_request(value)

    #print("HERE")
    #print(ch1.value)
    #time.sleep(0.5)

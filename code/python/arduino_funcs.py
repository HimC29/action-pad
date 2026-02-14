import time

# Initialize serial connection
# Use a timeout to prevent infinite blocking
arduino = ""

def set_arduino(data):
    global arduino
    arduino = data

def send_data(data):
    # Encodes string and sends to Arduino.
    arduino.write(bytes(data, 'utf-8'))
    time.sleep(0.05) # Brief pause to let Arduino process

def read_data():
    # Reads a line of data from Arduino.
    if arduino.in_waiting > 0:
        return arduino.readline().decode('utf-8').rstrip()
    return None

def send_and_read(data):
    # Sends command and reads response.
    send_data(data)
    return read_data()

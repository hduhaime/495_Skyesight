import RPi.GPIO as GPIO
from flask import Flask
from flask import jsonify, request
import time

app = Flask(__name__)

@app.route("/fetchSensorData", methods=['POST'])
def fetchSensorData():

    GPIO.setmode(GPIO.BCM)
    TRIG= int(request.form['TRIG'])
    ECHO = int(request.form['ECHO'])

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print('waiting for sensor')
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while(GPIO.input(ECHO) == 1):
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration*17150
    distance = round(distance,2)

    GPIO.cleanup()
    
    sensor_data = {"distance": distance}

    return jsonify(sensor_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

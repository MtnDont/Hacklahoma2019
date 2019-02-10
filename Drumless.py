#!/usr/bin/python3

# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import board
import busio
import adafruit_lsm9ds1
import RPi.GPIO as GPIO
import math

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# Global variables
firsties = True

# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
# values every second and print them out.

while True:
    #Priority for thresholds to determine when to play the sound
    priority = ""
    # Read acceleration, magnetometer, gyroscope, temperature.
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    accel_avg = accel_x + accel_y + accel_z
    gyro_avg = abs(gyro_x) + abs(gyro_y) + abs(gyro_z)

    accels = [accel_x, accel_y, accel_z]
    gyros = [gyro_x, gyro_y, gyro_z]
    # Print values to terminal for debugging and analysis
    print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
    print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    print('Avg gyro: {0:0.3f}'.format(gyro_avg))

    # Determine max value to set priortization
    # Uses absolute values so multidirectional swings are recognized
    minVal = round(min(list(accels)), 3)
    maxVal = round(max(list(accels)), 3)
    if abs(maxVal) > abs(minVal):
        maxVal = abs(maxVal)
    else:
        maxVal = abs(minVal)

    gyro_priority = gyro_avg
    if maxVal == round(abs(accel_x), 3):
        priority = "X"
        gyro_priority = gyro_avg - abs(gyro_x)
    elif maxVal == round(abs(accel_y), 3):
        priority = "Y"
        gyro_priority = gyro_avg - abs(gyro_y)
    elif maxVal == round(abs(accel_z), 3):
        priority = "Z"
        gyro_priority = gyro_avg - abs(gyro_z)

    # Print Priority stats for debugging
    print('Priority: ' + priority + ' at ' + str(maxVal) + str(round(abs(accel_z))))

    # Swing is based on gyro_avg and a given threshold
    gyro_avg = gyro_priority
    if gyro_avg >= 350 and not firsties:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.15)
    else:
        time.sleep(0.1)
    GPIO.output(17, GPIO.LOW)
    firsties = False

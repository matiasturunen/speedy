import time
import serial
import pynmea2

from gps import gps
port = "/dev/ttyAMA0" # the serial port to which the pi is connected.

### Autorun at /etc/rc.local ###

#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 1.0)
filename = '/home/pi/speedy/gpsoutput.txt'

with open(filename, 'w') as f:
    f.write('GPS DATA\n')
    pass

while 1:
    try:
        data = ser.readline()
        data = data.decode("utf-8")
    except serial.SerialException:
        # recreate serial
        print('recreate serial')
        ser.close()
        ser = serial.Serial(port, baudrate = 9600, timeout = 1.0)

    except UnicodeDecodeError:
        print('Unicode error')

    except Exception as e:
        print(e)
        ("loading") 
        #wait for the serial port to churn out data
    
    #print(data)

    if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data

        try:
            with open(filename, 'a') as f:
                msg = pynmea2.parse(data)
                print(msg)
                f.write(str(msg) + '\n')

                #parse the latitude and print
                latval = msg.lat
                concatlat = "lat:" + str(latval)
                print (concatlat)
        
                #parse the longitude and print
                longval = msg.lon
                concatlong = "long:"+ str(longval)
                print (concatlong)

                print('LAT ' + str(gps.convertCoordinates(msg.lat, msg.lat_dir)))
                print('LON ' + str(gps.convertCoordinates(msg.lon, msg.lon_dir)))
        except Exception as e:
            print('error')
            print(e)

    # if data[0:6] == '$GPRMC':
    #     print(data)
    #     pass
        
    time.sleep(0.1)#wait a little before picking the next data.
    #print('Time ' + str(time.strftime('%X')))
print('GPS STOPPED')

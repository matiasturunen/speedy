import time
import serial
import pynmea2

from gps import gps
port = "/dev/ttyAMA0" # the serial port to which the pi is connected.

#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 1.0)
filename = '/home/pi/speedy/gpsoutput_' + time.strftime('%d_%m_%H_%M_%S')

with open(filename, 'w') as f:
    f.write('GPS DATA\n')
    pass

prevLat = 0
prevLon = 0
prevTime = 0

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
                f.write(str(msg) + ',' + str(time.time()) + '\n')

                # Skip message if it has no lat or long values
                if (msg.lat == '' or msg.lon == ''):
                    continue

                # Convert lat and lon to decimal
                latDec = gps.convertCoordinates(msg.lat, msg.lat_dir)
                lonDec = gps.convertCoordinates(msg.lon, msg.lon_dir)

                print('LAT: ' + str(latDec))
                print('LON: ' + str(lonDec))

                if (prevTime > 0):
                    timeDelta = time.time() - prevTime
                    #print('Timedelta: ' + str(timeDelta))
                    print('Distance: ' + str(gps.haversine(prevLat, prevLon, latDec, lonDec)))
                    print('Speed: ' + str(gps.getSpeed(prevLat, prevLon, latDec, lonDec, timeDelta)))
                
                # save current info
                prevTime = time.time()
                prevLat = latDec
                prevLon = lonDec
                

        except Exception as e:
            print('error')
            print(e)
        
    time.sleep(0.5)#wait a little before picking the next data.

print('GPS STOPPED')

import math
import time
import serial
import pynmea2
from threading import Thread
from queue import LifoQueue, Empty

class GPSInfo:
    speed = 0
    distance = 0
    lat = 0
    lat_dir = 0
    lon = 0
    lon_dir = 0

    def __init__(self, speed, distance=0, lat=0, lon=0, lat_dir=0, lon_dir=0):
        self.speed = speed
        self.distance = distance
        self.lat = lat
        self.lat_dir = lat_dir
        self.lon = lon
        self.lon_dir = lon_dir


class GPS:
    port = "/dev/ttyAMA0"
    ser = None

    outputfile = ""

    prevLat = 0
    prevLon = 0
    prevTime = 0

    _thread = None
    queueSize = 100

    def convertCoordinates(self, coord, d):
        """Convert NMEA coordinates to decimal
        """
        if (d == 'N' or d == 'S'):
            dd = int(str(coord[0:2]))
            ss = float(str(coord[2:]))
            latDec = dd + ss/60

            if (d == 'S'):
                latDec = latDec * -1
            return latDec
        elif (d == 'E' or d == 'W'):
            dd = int(str(coord[0:3]))
            ss = float(str(coord[3:]))
            lonDec = dd + ss/60

            if (d == 'W'):
                lonDec = lonDec * -1
            return lonDec

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points
        """
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2*math.asin(math.sqrt(a))
        r = 6371 # Radius of earth

        d = c * r
        return d

    def getSpeed(self, oldLat, oldLon, newLat, newLon, timeDelta):
        """Get speed from coordinates

            Timedelta should be seconds!
        """
        distance = self.haversine(oldLat, oldLon, newLat, newLon)
        speed = distance / timeDelta

        return speed

    def GPSLoop(self, queue):
        if (self.ser == None):
            self.ser = serial.Serial(self.port, baudrate = 9600, timeout = 1.0)
        
        while True:
            try:
                data = self.ser.readline()
                data = data.decode("utf-8")
            except serial.SerialException:
                # recreate serial
                self.ser.close()
                self.ser = serial.Serial(self.port, baudrate = 9600, timeout = 1.0)
                #print('recreate serial')

            except UnicodeDecodeError:
                #print('Unicode error')
                pass

            except Exception as e:
                #print('Error ' + str(e))
                pass

            if (data[0:6] == '$GPGGA'): # Lat and lon values are contained in GPGGA string of NMEA data
                try:
                    msg = pynmea2.parse(data)
                except Exception as e:
                    # Pynmea2 parse error
                    continue

                print(data)

                # Skip message if it has no lat or lon values
                if (msg.lat == '' or msg.lon == ''):
                    continue

                # Convert lat and lon to decimal
                latDec = self.convertCoordinates(msg.lat, msg.lat_dir)
                lonDec = self.convertCoordinates(msg.lon, msg.lon_dir)

                #print('Lat: ' + str(latDec))
                #print('Lon: ' + str(lonDec))

                if (self.prevTime > 0):
                    timeDelta = time.time() - self.prevTime

                    distance = self.haversine(self.prevLat, self.prevLon, latDec, lonDec)
                    speed = self.getSpeed(self.prevLat, self.prevLon, latDec, lonDec, timeDelta)
                    
                    if (self._thread != None):
                        if (queue.full()):
                            # Try to empty queue
                            for x in range(0, self.queueSize):
                                try:
                                    queue.qet()
                                except Empty:
                                    continue
                        info = GPSInfo(speed, distance)
                        queue.put(info)

                    print('Distance: ' + str(distance))
                    print('Speed: ' + str(speed))
                
                # save current info
                self.prevTime = time.time()
                self.prevLat = latDec
                self.prevLon = lonDec

            time.sleep(0.5) # Wait a little before picking next data

    def GPSThread(self):
        queue = LifoQueue(self.queueSize)
        self._thread = Thread(
            target=self.GPSLoop,
            daemon=True,
            args=(queue,)
        )

        self._thread.start()

        return queue

gps = GPS()

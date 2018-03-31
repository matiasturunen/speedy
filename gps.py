import math

class GPS:
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

gps = GPS()

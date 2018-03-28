class GPS:
    def convertCoordinates(self, coord, d):
        """Convert NMEA coordinates to decimal
        """
        if (d == 'N' or d == 'S'):
            dd = int(coord[0:2])
            ss = float(coord[2:])
            latDec = dd + ss/60

            if (d == 'S'):
                latDec = latDec * -1
            return latDec
        elif (d == 'E' or d == 'W'):
            dd = int(coord[0:3])
            ss = float(coord[3:])
            latLng = dd + ss/60

            if (d == 'W'):
                latLng = latLng * -1
            return latLng

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points
        """
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2*asin(sqrt(a))
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

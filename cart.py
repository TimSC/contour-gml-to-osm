import math

def LatLonToCart(lat, lon, alt):
	R = 6371000. + alt
	x = R * math.cos(lat) * math.cos(lon)
	y = R * math.cos(lat) * math.sin(lon)
	z = R * math.sin(lat)
	return x, y, z

def CartToLatLon(x, y, z):
	dist = (x**2. + y**2. + z**2.) ** 0.5
	alt = dist - 6371000.
	lat = math.asin(z / dist)
	lon = math.atan2(y, x)
	return lat, lon, alt

if __name__ == "__main__":
	
	lat, lon, alt = math.radians(51.0), math.radians(-1), 100.
	print lat, lon, alt
	x, y, z = LatLonToCart(lat, lon, alt)
	print x, y, z
	print CartToLatLon(x, y, z)


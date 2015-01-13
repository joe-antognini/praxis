#! /usr/bin/env python

from astropy.time import Time
from math import *

def app_sidereal_t_0h(date):
  '''Calculate the apparent sidereal time at Greenwich, 0h on the given
  date.

  Input:
    date: The date as a string.
  
  Output:
    The apparent sidereal time at Greenwich, 0h in degrees.
  '''
  
  JD = Time(date, scale='ut').jd
  T = (JD - 2451545) / 36525.

  theta0 = 100.46061837 + 36000.770053608 * T + .000387933 * T**2
           - T**3 / 38710000.

  return theta0

def obliquity(date):
  '''Calculate the obliquity of the ecliptic.

  Input:
    date: The date as a string
   
  Output:
    The obliquity of the ecliptic in degrees.
  '''

  JDE = Time(date, scale='tt').jd
  T = (JDE - 2451545) / 36525.

  epsilon0 = (23 + 26/60. + 21.448/3600
             - 46.8150/3600 * T
             - .00059/3600 * T**2
             + .001813/3600 * T**3)

  return epsilon0

def solar_coords(date):
  '''Calculate the RA and Dec of the Sun on the given date.

  Input:
    date: The date as a string.

  Output:
    A tuple of the ra and dec.
  '''
  
  JD = Time(date, scale='utc').jd
  T = (JD - 2451545) / 36525.

  # Geometric mean longitude of the Sun
  L0 = 280.46645 + 36000.76983 * T + .0003032 * T**2
  L0 %= 360

  # Mean anomaly of the Sun
  M = 357.52910 + 35999.0503 * T - .0001559 * T**2 - .00000048 * T**3
  M %= 360

  # Eccentricity of Earth's orbit
  e = .016708617 - .000042037 * T - .0000001236 * T**2

  # Equation of center
  C = ((1.9146 - .004817 * T - .000014 * T**2) * sin(M * pi / 180)
      + (.019993 - .000101 * T) * sin(2 * M * pi / 180)
      + .00029 * sin(3 * M * pi / 180))

  # True longitude of the Sun
  Theta = L0 + C

  # Obliquity of the ecliptic
  epsilon = obliquity(date)

  ra = atan2(cos(epsilon*pi/180) * sin(Theta*pi/180), cos(Theta*pi/180))
  dec = asin(sin(epsilon*pi/180) * sin(Theta*pi/180))

  return (ra*180/pi, dec*180/pi)

def sunrise_set(lat, lon, date):

  '''Calculate the time of sunrise and sunset.  This implements Chapter 14
  of Astronomical Algorithms.

  Input:
    lat: The latitude as a decimal.  West is given positive values.

    lon: The longitude as a decimal. 

    date: The date.

  Output:
    A tuple with the JD date of the sunrise and sunset.
  '''

  h0 = -.8333

  # Get the RA and dec of the Sun on the day, the day before, and the day
  # after at 0h Dynamical Time.
  alpha1, dec1 = solar_coords(date - 1)
  alpha2, dec2 = solar_coords(date)
  alpha3, dec3 = solar_coords(date + 1)

  # Find out if the Sun is circumpolar at this latitude and time of the
  # year.
  if not -1 < sin(lat) * sin(dec2) < 1:
    raise ValueError(
    'Sun is circumpolar at this latitude and time of year.  No sunrise or sunset occurs.')

  # For the Sun, h0 = -50'.
  cos_H0 = ((sin(50./60 * pi/180) - sin(lat) * sin(dec2)) / (cos(lat) * 
    cos(dec2)))

  # The apparent sidereal time at 0h UT at Greenwich
  theta0 = app_sidereal_t_0h(date)

  m0 = ((alpha2 + lon - theta0) / 360) % 1
  m1 = (m0 - acos(H0) / pi)
  m2 = (m0 + acos(H0) / pi)

  theta_rise = theta0 + 360.985647 * m1
  theta_set = theta0 + 360.985647 * m2

  # The difference in seconds between Terrestrial Time and UTC on the given
  # date.
  t = Time(date, scale='utc')
  Delta_T = t.tt.val - t.utc.jd
  n = m + Delta_T / 86400
  
  # Interpolate to find ra and dec
  a = alpha2 - alpha1
  b = alpha3 - alpha2
  c = b - a
  ra = alpha2 + n / 2 * (a + b + n * c)

  a = dec2 - dec1
  b = dec3 - dec2
  c = b - a
  dec = dec2 + n / 2 * (a + b + n * c)

  H_rise = theta_rise - lon - ra
  H_set = theta_set - lon - ra

  h = eqcoor2alt((ra, dec), (lat, lon))[0]

  delta_m = (h - h0) / (360 * cos(dec * pi / 180) * cos(lat * pi / 180))
  delta_m_rise = delta_m / sin(H_rise * pi / 180)
  delta_m_set = delta_m / sin(H_set * pi / 180)

  rise_hour = int(24 * (m1 + delta_m_rise))
  rise_min = int(60 * (24 * (m1 + delta_m_rise) - rise_hour))
  rise_sec = 60 * (60 * (24 * (m1 + delta_m_rise) - rise_hour) - rise_minute)
  set_hour = int(24 * (m2 + delta_m_set))
  set_min = int(60 * (24 * (m2 + delta_m_set) - set_hour))
  set_sec = 60 * (60 * (24 * (m2 + delta_m_set) - set_hour) - set_minute)
  return ((rise_hour, rise_min, rise_sec), (set_hour, set_min, set_sec))

# The function below is from Wikipedia's sunrise equation page.  It doesn't
# seem to work very well.
def sunset_JD(lat, lon, date):
  '''Calculate the time of sunset.

  Input:
    lat:
      Latitude.  Either in decimal form (float) or as a tuple in degrees,
        minutes, seconds.
    lon:
      Longitude.  Either in decimal form (float) or as a tuple in degrees,
        minutes, seconds.  Western longitudes are positive, Eastern
        longitudes are negative.
    date:
      A date string in the form 'yyyy-mm-dd'.

  Returns:
    sunset:
      Time of sunset as a Julian date.
  '''

  # Convert latitude and longitude to decimal form if necessary.
  if type(lat) in [tuple, list]:
    if len(lat) > 3:
      raise ValueError(
        'sunrise_time(): lat tuple must contain three elements or fewer.')
    dec_lat = 0
    for i, elem in enumerate(lat):
      dec_lat += float(elem) / 60**i
    lat = dec_lat
  if type(lon) in [tuple, list]:
    if len(lon) > 3:
      raise ValueError(
        'sunrise_time(): lon tuple must contain three elements or fewer.')
    dec_lon = 0
    for i, elem in enumerate(lon):
      dec_lon += float(elem) / 60**i
    lon = dec_lon
  jd = Time(date, scale='utc').jd + 1

  n_star = jd - 2451545.0009 - lon / 360
  n = int(n_star + .5)

  # Approximate Solar noon
  J_star = 2451545.0009 + lon / 360 + n

  print lat, lon

  # Solar mean anomaly
  M = (357.5291 + .98560028 * (J_star - 2451545)) % 360

  # Equation of center
  C = 1.39148 * sin(M * pi / 180) + .02 * sin(2 * M) + .0003 * sin(3 * M)

  # Ecliptic longitude
  lamb = (M + 102.9372 + C + 180) % 360

  # Solar transit
  J_transit = J_star + .0053 * sin(M) - .0069 * sin(2 * lamb)

  print J_transit

  # Declination of the Sun
  sin_dec = sin(lamb * pi / 180) * sin(23.45 * pi / 180)

  # Hour angle
  cos_ha = ((sin(-.83 * pi / 180) - sin(lat * pi / 180) * sin_dec) / 
    (cos(lat * pi / 180) * sqrt(1 - sin_dec**2)))

  J_set = (2451545.0009 + (acos(cos_ha) * 180 / pi + lon) / 360 + n 
    + .0053 * sin(M) - .0069 * sin(2 * lamb))

  return J_set

def sunset(lat, long, date):
  '''Calculate the time of sunset.

  Input:
    lat:
      Latitude.  Either in decimal form (float) or as a tuple in degrees,
        minutes, seconds.
    long:
      Longitude.  Either in decimal form (float) or as a tuple in degrees,
        minutes, seconds.  Western longitudes are positive, Eastern
        longitudes are negative.
    date:
      A date string in the form 'yyyy-mm-dd'.

  Returns:
    sunset:
      Time of sunset as a Julian date.
  '''

if __name__ == '__main__':
  print solar_coords('1992-10-13')
#  print sunset_JD((39, 59), (82, 59), '2015-01-09')

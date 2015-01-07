#! /usr/bin/env python

from astropy.time import Time
from math import pi, sin, cos, sqrt, acos

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
  jd = Time(date, scale='utc').jd

  n_star = jd - 2451545.0009 - lon / 360
  n = int(n_star + .5)

  # Approximate Solar noon
  J_star = 2451545.0009 + lon / 360 + n

  # Solar mean anomaly
  M = (357.5291 + .98560028 * (J_star - 2451545)) % 360

  # Equation of center
  C = 1.39148 * sin(M * pi / 180) + .02 * sin(2 * M) + .0003 * sin(3 * M)

  # Ecliptic longitude
  lamb = (M + 102.9372 + C + 180) % 360

  # Solar transit
  J_transit = J_star + .0053 * sin(M) - .0069 * sin(2 * lamb)

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


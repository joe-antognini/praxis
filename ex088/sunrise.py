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
  
  JD = Time(date, scale='utc').jd
  T = (JD - 2451545) / 36525.

  JDE = Time(date, scale='tt').jd
  TE = (JDE - 2451545) / 36525

  # The mean sidereal time
  theta0 = (100.46061837 + 36000.770053608 * T + .000387933 * T**2
           - T**3 / 38710000.) % 360

  # Next calculate the correction to get the apparent sidereal time.

  # Longitude of the Moon's argument of latitude
  Omega = ((125.04452 - 1934.136261 * TE + .0020708 * TE**2 + TE**3 / 
    450000.) % 360)

  # Mean longitudes of the Sun and Moon
  L = 280.4665 + 36000.7698 * TE
  Lp = 218.3165 + 481267.8813 * TE

  # These quantities are in arcseconds
  Delta_psi = (-17.2 * sin(Omega*pi/180) - 1.32 * sin(2*L*pi/180) - .23 *
              sin(2*Lp*pi/180) + .21 * sin(2*Omega*pi/180))
  Delta_eps = (9.2 * cos(Omega*pi/180) + .57 * cos(2*L*pi/180) + .1 *
              cos(2*Lp*pi/180) - .09 * cos(2*Omega*pi/180))

  epsilon = obliquity(JD)

  return (theta0 + Delta_psi * cos((epsilon + Delta_eps/3600.)*pi/180) 
          / 3600)

def obliquity(JD):
  '''Calculate the obliquity of the ecliptic.

  Input:
    date: The date as a string
   
  Output:
    The obliquity of the ecliptic in degrees.
  '''

  T = (JD - 2451545) / 36525.

  epsilon0 = (23 + 26/60. + 21.448/3600
             - 46.8150/3600 * T
             - .00059/3600 * T**2
             + .001813/3600 * T**3)

  return epsilon0

def solar_coords(JD):
  '''Calculate the RA and Dec of the Sun on the given date.

  Input:
    date: The date as a string.

  Output:
    A tuple of the ra and dec.
  '''
  
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
  epsilon = obliquity(JD)

  ra = atan2(cos(epsilon*pi/180) * sin(Theta*pi/180), cos(Theta*pi/180))
  dec = asin(sin(epsilon*pi/180) * sin(Theta*pi/180))

  return (ra*180/pi, dec*180/pi)

def sunrise_set(lat, lon, date):
  '''Calculate the time of sunrise and sunset.  This implements Chapter 14
  of Astronomical Algorithms.

  Input:
    lat: The latitude as a decimal.  West is given positive values.

    lon: The longitude as a decimal. 

    date: The date as a string 'YYYY-MM-DD'

  Output:
    A string with the UT time of sunrise and sunset.
  '''

  h0 = -.8333

  # Get the RA and dec of the Sun on the day, the day before, and the day
  # after at 0h Dynamical Time.
  JD = Time(date, scale='utc').jd
  alpha1, dec1 = solar_coords(JD - 1)
  alpha2, dec2 = solar_coords(JD)
  alpha3, dec3 = solar_coords(JD + 1)

  # Find out if the Sun is circumpolar at this latitude and time of the
  # year.
  if not -1 < sin(lat*pi/180) * sin(dec2*pi/180) < 1:
    raise ValueError(
    'Sun is circumpolar at this latitude and time of year.  No sunrise or sunset occurs.')

  # For the Sun, h0 = -50'.
  cos_H0 = ((sin(h0*pi/180) - sin(lat*pi/180) * sin(dec2*pi/180)) /
    (cos(lat*pi/180 ) * cos(dec2*pi/180)))

  # The apparent sidereal time at 0h UT at Greenwich
  theta0 = app_sidereal_t_0h(date)

  m0 = ((alpha2 + lon - theta0) / 360) % 1
  m1 = (m0 - acos(cos_H0) / (2*pi))
  m2 = (m0 + acos(cos_H0) / (2*pi))

  rise_hour = int(24 * m1)
  rise_min = int(60 * (24 * m1 - rise_hour))
  rise_sec = 60 * (60 * (24 * m1 - rise_hour) - rise_min)
  set_hour = int(24 * m2)
  set_min = int(60 * (24 * m2 - set_hour))
  set_sec = 60 * (60 * (24 * m2 - set_hour) - set_min)
  return ((rise_hour, rise_min, rise_sec), (set_hour, set_min, set_sec))

def sunriseset_str(lat, lon, date):
  '''A wrapper for sunrise_set that outputs the sunrise and sunset times as
  strings.

  Input:
    lat: The latitude as a decimal.  West is given positive values.

    lon: The longitude as a decimal. 

    date: The date as a string 'YYYY-MM-DD'

  Output:
    A string with the UT time of sunrise and sunset.
  '''

  if type(lat) is tuple:
    lat_dec = 0
    for i, elem in enumerate(lat):
      lat_dec += elem / 60.**i
    lat = lat_dec
  if type(lon) is tuple:
    lon_dec = 0
    for i, elem in enumerate(lon):
      lon_dec += elem / 60.**i
    lon = lon_dec

  sunrise, sunset = sunrise_set(lat, lon, date)

  print 'Sunrise: %d:%d:%d' % sunrise
  print 'Sunset:  %d:%d:%d' % sunset

if __name__ == '__main__':
  sunriseset_str((39, 59), (82, 59), '2015-01-15')

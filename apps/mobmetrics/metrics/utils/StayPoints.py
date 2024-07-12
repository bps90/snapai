import pandas as pd
from math import sqrt

class StayPoints():
  def __init__(self):
    pass

  def extract(self, id_trace, distance_threshold, time_threshold):
    """
      Extract all the Stay Points

      id_trace = Trace with only the id needed
      distance_threshold = the max distance for stay poitns
      time_threshold = the min time for stay points

      return

      stay_points = table with all stay points -> [lat, lgnt, arvT, levT]

      ∀ m < i <= n, distance(Pm, Pi) <= Dthres e (Tn - Tm) >= Tthres
    """
    stay_points = []
    m = 0

    while m < len(id_trace) - 1:
      i = m + 1
      arvT = id_trace.iloc[m]['time']
      lat = id_trace.iloc[m]['x']
      lgnt = id_trace.iloc[m]['y']
      buffer = 1

      while (i < len(id_trace)) and (self.distance(id_trace.iloc[m], id_trace.iloc[i]) <= distance_threshold):
        lat += id_trace.iloc[i]['x']
        lgnt += id_trace.iloc[i]['y']
        buffer += 1

        i += 1

      levT = id_trace.iloc[i - 1]['time']

      if levT - arvT >= time_threshold:
        stay_points.append({'lat' : lat/buffer, 'lgnt' : lgnt/buffer, 'arvT' : arvT, 'levT' : levT})
      
      m = i
    return pd.DataFrame(stay_points)
  

  def distance(self, fpoint, spoint):
    """
      Calculate the distance between the poinst fpoint and spoint
    """
    return sqrt((spoint['x'] - fpoint['x']) ** 2 + (spoint['y'] - fpoint['y']) ** 2)
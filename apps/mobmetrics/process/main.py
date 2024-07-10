import pandas as pd

from ..metrics.temporal.totalTraveTime import TotalTravelTime

def main(Trace):

  Trace = pd.read_csv(Trace)

  possibleId = sorted(Trace['id'].unique())

  for n in possibleId:
    TTrvT = TotalTravelTime(Trace, n).extract()
    print(TTrvT)
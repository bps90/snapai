import pandas as pd

from ..metrics.utils.StayPoints import StayPoints

def main(Trace):

  Trace = pd.read_csv(Trace)
  possibleId = sorted(Trace['id'].unique())

  for n in possibleId:
    filtred_trace = Trace[Trace['id'] == n]
    sorted_trace = filtred_trace.sort_values(by='time')

    a = StayPoints().extract(sorted_trace, 100, 10)
    print(f"Stay Point from id {n}")
    print(a)
  

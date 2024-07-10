"""
  Total Travel Time
  - Individual
  - Temporal

  Calculate the total travel time of each id on the mobility model, it does not consider the staying points
"""
class TotalTravelTime():
    def __init__(self, trace, id):
        self.metric = 'TTrvT'
        self.trace = trace
        self.id = id
    
    def extract(self):
        filtred_trace = self.trace[self.trace['id'] == self.id]
        sorted_trace = filtred_trace.sort_values(by='time')

        start_time = sorted_trace.iloc[0]['time']
        finish_time = sorted_trace.iloc[-1]['time']

        self.result = (finish_time - start_time)

        return self.result
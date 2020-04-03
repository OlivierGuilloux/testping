import plotly.graph_objects as go
from subprocess import getoutput

import re
PAT = "64 bytes from 1.1.1.1: icmp_seq=(?P<seq>.*) ttl=(?P<ttl>.*) time=(?P<time>.*)ms"
COMILE_PAT = re.compile(PAT)
COUNT=10

def ping(adr, count=3):
    res_ping = getoutput([f'ping 1.1.1.1 -c {count}'])
    l = [2000 for i in range(count)]
    for iping in res_ping.split('\n'):
      if iping[:8] == '64 bytes':
        m = COMILE_PAT.match(iping)
        if m :
            l[int(m.group('seq').strip()) - 1] = float(m.group('time').strip())
        print(iping)
    return l

def main():
    y = ping('1.1.1.1', count=COUNT)
    mean = sum(y)/len(y) 
    ymean = [mean for i in range(len(y))]
    fig = go.Figure(
       data=[
           go.Scatter(y=y, name="ms"), # mode="markers", marker=dict(size=20, color="#432"), name="Mesures"),
           go.Scatter(y=ymean, name="moyenne") # mode="markers", marker=dict(size=20, color="#432"), name="Mesures"),
       ],
       layout_title_text="Temps de traitement",
    )
    print("Show")
    fig.show()
    print("Done")
if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) > 1:
        try:
            COUNT = int(args[1])
        except ValueError:
           pass
    main()

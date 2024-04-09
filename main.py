import plotly.graph_objects as go
from subprocess import getoutput
import requests
import time
import datetime

import re
COUNT=10
SLEEP=5

def ping(adr, count=3):
    #pat= f"64 bytes from {adr}: icmp_seq=(?P<seq>.*) ttl=(?P<ttl>.*) time=(?P<time>.*)ms"
    #64 octets de 1.1.1.1 : icmp_seq=1 ttl=53 temps=61.9 ms
    pat= f"64 octets de {adr} : icmp_seq=(?P<seq>.*) ttl=(?P<ttl>.*) temps=(?P<time>.*)ms.*"
    COMILE_PAT = re.compile(pat)
    res_ping = getoutput([f'ping {adr} -c {count}'])
    l = [2000 for i in range(count)]
    for iping in res_ping.split('\n'):
      m = COMILE_PAT.match(iping)
      if m :
        l[int(m.group('seq').strip()) - 1] = float(m.group('time').strip())
    return l

def req(adr, count=3):
    l = [] #2000 for i in range(count)]
    t = []
    for i in range(count):
        try:
            response = requests.get(adr)
            response_time = response.elapsed.microseconds / 1000
            t.append(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            l.append(response_time)
            time.sleep(SLEEP)
        except KeyboardInterrupt as e:
            return (l, t)
    return (l, t)

def main(adr='1.1.1.1', ping=False):
    if ping:
        (y, y) = ping(adr, count=COUNT)
    else:
        (y, t) = req(adr, count=COUNT)
    mean = sum(y)/len(y) 
    ymean = [mean for i in range(len(y))]
    fig = go.Figure(
       data=[
           go.Scatter(y=y, name="ms", x=t), # mode="markers", marker=dict(size=20, color="#432"), name="Mesures"),
           go.Scatter(y=ymean, name="moyenne", x=t) # mode="markers", marker=dict(size=20, color="#432"), name="Mesures"),
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
    if len(args) > 2:
        adr = args[2]
    else:
        adr = '1.1.1.1'
    main(adr)

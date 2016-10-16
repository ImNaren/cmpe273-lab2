#!/usr/bin/env python


import logging
from spyne import Application, rpc, ServiceBase, Iterable, UnsignedInteger, String
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
import urllib2
import json
import operator
from datetime import datetime

class crime(ServiceBase):
    @rpc(String, String, String, _returns=String)
    def checkcrime(ctx, lat, lon, radius):

        fullurl = "https://api.spotcrime.com/crimes.json?"+ "lat=" + lat + "&lon=" + lon + "&radius=" + radius + "&key=. "
        loadurl = urllib2.urlopen(fullurl)
        jsonData = json.load(loadurl)
        crime_type_count = {}
        event_time_count = {}
        streets_address = {}

        Total_Crimes = len(jsonData['crimes'])

        for item in jsonData['crimes']:
            if not item['type'] in crime_type_count:
                crime_type_count[str(item['type'])] = 1
            else:
                crime_type_count[str(item['type'])] += 1
            if not item['date'] in event_time_count:
                event_time_count[str(item['date'])] = 1
            else:
                event_time_count[str(item['date'])] += 1

            if not item['address'] in streets_address:
                streets_address[str(item['address'])] = 1
            else:
                streets_address[str(item['address'])] += 1

        a = "00:01:00"
        b = "03:00:00"
        c = "03:01:00"
        d = "06:00:00"
        e = "06:01:00"
        f = "09:00:00"
        g = "09:01:00"
        h = "12:00:00"
        i = "12:01:00"
        j = "15:00:00"
        k = "15:01:00"
        l = "18:00:00"
        m = "18:01:00"
        n = "21:00:00"
        o = "21:01:00"
        p = "23:59:59"
        q = "00:00:00"

        at = datetime.strptime(a,"%H:%M:%S").time()
        bt = datetime.strptime(b,"%H:%M:%S").time()

        ct = datetime.strptime(c,"%H:%M:%S").time()
        dt = datetime.strptime(d,"%H:%M:%S").time()

        et = datetime.strptime(e,"%H:%M:%S").time()
        ft = datetime.strptime(f,"%H:%M:%S").time()

        gt = datetime.strptime(g,"%H:%M:%S").time()
        ht = datetime.strptime(h,"%H:%M:%S").time()

        it = datetime.strptime(i,"%H:%M:%S").time()
        jt = datetime.strptime(j,"%H:%M:%S").time()

        kt = datetime.strptime(k,"%H:%M:%S").time()
        lt = datetime.strptime(l,"%H:%M:%S").time()

        mt = datetime.strptime(m,"%H:%M:%S").time()
        nt = datetime.strptime(n,"%H:%M:%S").time()

        ot = datetime.strptime(o,"%H:%M:%S").time()
        pt = datetime.strptime(p,"%H:%M:%S").time()
        qt = datetime.strptime(q,"%H:%M:%S").time()




        event_time_count1 = {"12:01am-3am" : 0 ,"3:01am-6am" : 0, "6:01am-9am" : 0, "9:01am-12noon" : 0, "12:01pm-3pm" : 0, "3:01pm-6pm" : 0, "6:01pm-9pm" : 0, "9:01pm-12midnight" : 0 }
        counter = 0
        for item in jsonData['crimes']:

            datekey = str(item['date'])
            t2 = datetime.strptime(datekey, "%m/%d/%y %I:%M %p")
            t3 = t2.time()
                
            if at <= t3 <= bt: event_time_count1["12:01am-3am"] += 1
            elif ct <= t3 <= dt: event_time_count1["3:01am-6am"] += 1
            elif et <= t3 <= ft: event_time_count1["6:01am-9am"] += 1
            elif gt <= t3 <= ht: event_time_count1["9:01am-12noon"] += 1
            elif it <= t3 <= jt: event_time_count1["12:01pm-3pm"] += 1
            elif kt <= t3 <= lt: event_time_count1["3:01pm-6pm"] += 1   
            elif mt <= t3 <= nt: event_time_count1["6:01pm-9pm"] += 1
            elif ot <= t3 <= pt: event_time_count1["9:01pm-12midnight"] += 1
            elif t3 == qt: event_time_count1["9:01pm-12midnight"] +=1

        sorted_st = sorted(streets_address.items(), key=lambda x:x[1], reverse = True)
        sorted_st_list = []
        for i in range(0,3):
             sorted_st_list.append(str(sorted_st[i][0]))

        final_st = []

        for j in range(0, len(sorted_st_list)):
            x = sorted_st_list[j].split("OF")
            if len(x)==2:
                final_st.append(x[1].strip())
            elif len(x) == 1:
                final_st.append(x[0].strip())


        final_st2 = []

        for j in range(0, len(final_st)):
            x = final_st[j].split("&")
            if len(x)==2:
                final_st2.append(x[1].strip())
            elif len(x) == 1:
                final_st2.append(x[0].strip())

        output = {"total_crime": Total_Crimes, "the_most_dangerous_streets": final_st2, "crime_type_count": crime_type_count, "event_time_count": event_time_count1}
        yield output


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    application = Application({crime}, 'spyne',

        in_protocol=HttpRpc(validator='soft'),
        out_protocol=JsonDocument(ignore_wrappers=True),
    )
    wsgi_application = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_application)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/checkcrime?")

    server.serve_forever()

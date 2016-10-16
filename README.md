# cmpe273-lab2.

A simple RPC application to check crime report for a location. Used [Spyne](http://spyne.io/#inprot=HttpRpc&outprot=JsonDocument&s=rpc&tpt=WsgiApplication&validator=true) 
toolkit to build the application.

#### Input (HttpRpc)

* lat - latitude of a location
* lon - longitude of a location
* radius - radius distance in miles.

```sh
curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=0.02"
```
Output(Json) returns crime information.
```json
{
    "event_time_count": {
      "3:01am-6am": 0,
      "12:01pm-3pm": 2,
      "6:01pm-9pm": 1,
      "3:01pm-6pm": 2,
      "9:01am-12noon": 3,
      "9:01pm-12midnight": 42,
      "6:01am-9am": 0,
      "12:01am-3am": 0
    },
    "crime_type_count": {
      "Theft": 5,
      "Arrest": 2,
      "Assault": 6,
      "Other": 35,
      "Robbery": 1,
      "Burglary": 1
    },
    "total_crime": 50,
    "the_most_dangerous_streets": [
      "S 1ST ST",
      "E SANTA CLARA ST",
      "N 5TH ST"
    ]
  }
```
### Dependency

#### CrimeReport API

```sh
# Example Crime Report near SJSU
curl -i "https://api.spotcrime.com/crimes.json?lat=37.334164&lon=-121.884301&radius=0.02&key=."
```


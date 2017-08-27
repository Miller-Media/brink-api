# Flight Data Endpoints

<a name="post-flightdata"></a>
<kbd>POST</kbd> `/v1/flight/{FLIGHT_ID}/data`

##### Sample Request

```json
{
	"timestamp": 213412355,
	"altitude": 1234,
	"barometricPressure": 1234143,
	"coordinateX": 23.234,
	"coordinateY": 23.2352,
	"temperature": 23
}
```

##### Sample Response

```json
{
	"response":"success",
	"message":"Flight data created."
}
```

----

<a name="get-flightdata"></a>
<kbd>GET</kbd> `/v1/flight/{FLIGHT_ID}/data`

The key value of each array is the timestamp at which those measurements were taken.

By default the data points per page are 100. You can adjust the paginated value with a GET parameter. 

##### Accepted GET Parameters

```
postsPerPage = Number of records returned per page. Maximum 250.
page = Page of results to return

Example: /v1/flight/{FLIGHT_ID}/data?postsPerPage=212&page=3
```

##### Sample Response

```json
{
	"213412355": {
		"altitude": 1234,
		"barometricPressure": 1234143,
		"coordinateX": 23.234,
		"coordinateY": 23.2352,
		"temperature": 23
	},
	"213412360": {
		"altitude": 1240,
		"barometricPressure": 1234943,
		"coordinateX": 26.234,
		"coordinateY": 24.2352,
		"temperature": 20
	},
	"nextPage": 2
}
```
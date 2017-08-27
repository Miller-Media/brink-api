# Flight Endpoints

<a name="get-flight"></a>
<kbd>GET</kbd> `/v1/flight/{FLIGHT_ID}`

A combination of the flight and info from the flightData models.

##### Sample Success Response 

```json
{
	"flightTime":12345,
	"flightId":9,
	"duration":32221,
	"startCoordinateX":12.1432,
	"startCoordinateY":112.2534,
	"endCoordinateX":123.124,
	"endCoordinateY":12.352,
	"maxAltitude":124,
	"minTemperature":12,
	"maxTemperature":65,
}
```

##### Sample Error Response

```json
{
	"response":"error",
	"message":"Error getting flight overview info."
}
```

---

<a name="post-flight"></a>
<kbd>POST</kbd> `/v1/flight`

Create the initial flight record in the DB.

##### Sample Response 

```json
{
	"response":"success",
	"message":"Flight created.",
	"id":9
}
```
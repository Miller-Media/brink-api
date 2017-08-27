# Brink API

These are the API endpoints that we will feed data into from the Brink Airships. Initially, these will be loaded in after flights.

## Endpoints

### Flights
[<kbd>GET</kbd> `/v1/flight/`](docs/v1/flights.md#get-flight)  
[<kbd>POST</kbd> `/v1/flight/`](docs/v1/flights.md#post-flight)  

### Flight Data
[<kbd>POST</kbd> `/v1/flight/{FLIGHT_ID}/data`](docs/v1/flights.md#post-flightdata)  
[<kbd>GET</kbd> `/v1/flight/{FLIGHT_ID}/data`](docs/v1/flights.md#get-flightdata)  

## Throttling

Since there is going to be a lot of data being transferred, we want to throttle the API calls. We could potential charge for a 'Pro' version for more calls. For now let's do this:

```
• 1 API call per second
• 10,000 API calls per day (about three hours of API calls at one per second)
```
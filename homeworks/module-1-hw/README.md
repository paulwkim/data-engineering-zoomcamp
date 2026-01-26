# question 1
```
docker run -it --entrypoint=bash python:3.13
pip --version
```
25.3

# question 2
db:5432

# question 3
```
select
  count(*) as trips_under_a_mile
from public.green_taxi_trips_11_2025
where lpep_pickup_datetime >= '2025-11-01'
  and lpep_pickup_datetime < '2025-12-01'
  and trip_distance <= 1
;
```
8007

# question 4
```
select
  lpep_pickup_datetime,
  trip_distance
from public.green_taxi_trips_11_2025
where trip_distance < 100
order by trip_distance desc
limit 1
;
```
2025-11-14

# question 5
```
with top_total_pickup_zone as (
  select
    "PULocationID"
  from public.green_taxi_trips_11_2025
  where lpep_pickup_datetime >= '2025-11-18'
    and lpep_pickup_datetime < '2025-11-19'
  group by "PULocationID"
  order by sum(total_amount) desc
  limit 1
)

select
  zones."Zone"
from zones
where zones."LocationID" = (select "PULocationID" from top_total_pickup_zone)
;
```
East Harlem North

# question 6
```
with largest_tip_zone as (
  select
    "DOLocationID",
    tip_amount
  from public.green_taxi_trips_11_2025
  where "PULocationID" = (select "LocationID" from zones where "Zone" = 'East Harlem North')
    and lpep_pickup_datetime >= '2025-11-01'
    and lpep_pickup_datetime < '2025-12-01'
  order by tip_amount desc
  limit 1
)

select
  zones."Zone"
from zones
where zones."LocationID" = (select "DOLocationID" from largest_tip_zone)
```
Yorkville West

# question 7
terraform init, terraform apply -auto-approve, terraform destroy
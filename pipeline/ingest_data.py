#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

# column types
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# define command line interface
@click.command()
@click.option('--year', default=2021, type=int, help='Year of data to download')
@click.option('--month', default=1, type=int, help='Month of data to download')
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pw', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')

# upload data to db
def run(year, month, pg_user, pg_pw, pg_host, pg_port, pg_db, chunksize, target_table):
    # set up url to download csv from
    prefix_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix_url}yellow_tripdata_{year}-{month:02d}.csv.gz'

    # connect to sqlalchemy engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_pw}@{pg_host}:{pg_port}/{pg_db}')

    # download data in chunks
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    # process data into database
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            # create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False
            print('table created')

        # insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

        print(f'inserted {len(df_chunk)} rows')

if __name__ == '__main__':
    run()
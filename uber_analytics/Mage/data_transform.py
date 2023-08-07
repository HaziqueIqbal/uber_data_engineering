import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index


    
    datetime_dim = df[["lpep_pickup_datetime","lpep_dropoff_datetime"]].reset_index(drop=True)

    datetime_dim['pickup_day'] = datetime_dim["lpep_pickup_datetime"].dt.day
    datetime_dim['pickup_month'] = datetime_dim["lpep_pickup_datetime"].dt.month
    datetime_dim['pickup_year'] = datetime_dim["lpep_pickup_datetime"].dt.year
    datetime_dim['pickup_hour'] = datetime_dim["lpep_pickup_datetime"].dt.hour
    datetime_dim['pickup_weekday'] = datetime_dim["lpep_pickup_datetime"].dt.weekday

    datetime_dim['dropoff_day'] = datetime_dim["lpep_dropoff_datetime"].dt.day
    datetime_dim['dropoff_month'] = datetime_dim["lpep_dropoff_datetime"].dt.month
    datetime_dim['dropoff_year'] = datetime_dim["lpep_dropoff_datetime"].dt.year
    datetime_dim['dropoff_hour'] = datetime_dim["lpep_dropoff_datetime"].dt.hour
    datetime_dim['dropoff_weekday'] = datetime_dim["lpep_dropoff_datetime"].dt.weekday

    datetime_dim["datetime_id"] = datetime_dim.index
    datetime_dim = datetime_dim[["datetime_id","lpep_pickup_datetime","pickup_day","pickup_month","pickup_year","pickup_hour","pickup_weekday",
                            "lpep_dropoff_datetime","dropoff_day","dropoff_month","dropoff_year","dropoff_hour","dropoff_weekday"]]



    passenger_count_dim = df[["passenger_count"]].reset_index(drop=True)
    passenger_count_dim["passenger_count_id"] = passenger_count_dim.index 
    passenger_count_dim = passenger_count_dim[["passenger_count_id","passenger_count"]]


    trip_distance_dim = df[["trip_distance"]].reset_index(drop=True)
    trip_distance_dim["trip_distance_id"] = trip_distance_dim.index
    trip_distance_dim = trip_distance_dim[["trip_distance_id","trip_distance"]]



    rate_code_type = {
    1:"Standard rate",
    2:"JFK",
    3:"Newark",
    4:"Nassau or Westchester",
    5:"Negotiated fare",
    6:"Group ride"
    }

    rate_code_dim = df[["RatecodeID"]].reset_index(drop=True)
    rate_code_dim["rate_code_id"] = rate_code_dim.index
    rate_code_dim["rate_code_name"] = rate_code_dim["RatecodeID"].map(rate_code_type)
    rate_code_dim = rate_code_dim[["rate_code_id","RatecodeID","rate_code_name"]]




    payment_type_name = {
    1:"Credit card",
    2:"Cash",
    3:"No charge",
    4:"Dispute",
    5:"Unknown",
    6:"Voided trip"
    }

    payment_type_dim = df[["payment_type"]].reset_index(drop=True)
    payment_type_dim["payment_type_id"] = payment_type_dim.index
    payment_type_dim["payment_type_name"] = payment_type_dim["payment_type"].map(payment_type_name)
    payment_type_dim = payment_type_dim[["payment_type_id","payment_type","payment_type_name"]]



    pick_and_drop_location_dim = df[["PULocationID","DOLocationID"]].reset_index(drop=True)
    pick_and_drop_location_dim["pickdrop_location_id"] = pick_and_drop_location_dim.index
    pick_and_drop_location_dim = pick_and_drop_location_dim[["pickdrop_location_id","PULocationID","DOLocationID"]]
    
    
    
    
    fact_table = df.merge(datetime_dim, left_on = "trip_id", right_on= "datetime_id") \
                .merge(passenger_count_dim, left_on = "trip_id", right_on = "passenger_count_id") \
                .merge(trip_distance_dim, left_on = "trip_id", right_on = "trip_distance_id") \
                .merge(rate_code_dim, left_on = "trip_id", right_on = "rate_code_id") \
                .merge(payment_type_dim, left_on = "trip_id", right_on = "payment_type_id") \
                .merge(pick_and_drop_location_dim, left_on = "trip_id", right_on = "pickdrop_location_id") \
                [["trip_id","VendorID","datetime_id","passenger_count_id","trip_distance_id","rate_code_id","payment_type_id",
                 "pickdrop_location_id","store_and_fwd_flag","fare_amount","extra","mta_tax","tip_amount","tolls_amount","ehail_fee"
                 ,"improvement_surcharge","total_amount","congestion_surcharge"]] 

    return {"datetime_dim":datetime_dim.to_dict(orient="dict"),
    "passenger_count_dim":passenger_count_dim.to_dict(orient="dict"),
    "trip_distance_dim":trip_distance_dim.to_dict(orient="dict"),
    "rate_code_dim":rate_code_dim.to_dict(orient="dict"),
    "payment_type_dim":payment_type_dim.to_dict(orient="dict"),
    "pick_and_drop_location_dim":pick_and_drop_location_dim.to_dict(orient="dict"),
    "fact_table":fact_table.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
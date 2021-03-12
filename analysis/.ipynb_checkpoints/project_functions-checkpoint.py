import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process(path):
    d = pd.read_csv(path)
    
    #changing price to int numbers
    d['price'] = d['price'].str.replace("$", "")
    d['price'] = d['price'].str.replace(",", "")
    d['price'] = d['price'].astype(float)

    #Method Chain 1: clean data (drop columns that are not needed, rename columns, deal with missing data)
    df = (
        pd.DataFrame(data=d)
        .rename(columns = {"review_scores_communication":"communication_reviews", "review_scores_location": "location_review", "listing_url":                                  "URL", "review_scores_accuracy": "review_accuracy", "review_scores_cleanliness": "cleanliness", "review_scores_checkin":                            "checkin_review"})
        .drop(columns=["scrape_id", "host_id", "license", "calculated_host_listings_count", "calculated_host_listings_count_entire_homes",
                      "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms", "host_since", "host_location",
                      "host_thumbnail_url", "host_picture_url", "host_listings_count", "host_total_listings_count", "host_verifications",
                      "host_has_profile_pic", "host_neighbourhood", "neighbourhood_cleansed", "neighbourhood_group_cleansed", "latitude",
                      "longitude", "bathrooms", "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", 
                      "maximum_maximum_nights","minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "calendar_updated", "availability_30", 
                      "availability_60", "availability_90", "availability_365", "calendar_last_scraped", "number_of_reviews_ltm", 
                      "number_of_reviews_l30d", "first_review", "review_scores_rating","id", "last_scraped", "picture_url", "host_url", 
                      "review_scores_value", "reviews_per_month", "host_is_superhost"])
        .dropna()
        .reset_index(drop=True)
    )
    
    #Method Chain 2: create new column and filter data
    df2 = (
        df
        .assign(good_property = lambda x: np.where((x.has_availability == "t")&(x.review_accuracy >= 8.0)&(x.cleanliness >= 8.0)&(x.location_review 
            >= 8.0), "T", "F"))
        .loc[lambda x: x['host_response_rate'] > "75%"]
        .loc[lambda x: x['price'] < 300]
        .reset_index(drop=True)
    )
    
    #Method Chain 3: Sort values and display relative columns only
    df3 = (
        df2
        .sort_values("price", ascending=False)
        .loc[:, ["name", "description", "host_name", "host_response_time", "host_response_rate", "neighbourhood", "room_type", "accommodates", 
                 "amenities", "price", "has_availability", "review_accuracy", "cleanliness", "location_review", "good_property"]]
    )
    
    return df3
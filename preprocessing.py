import pandas as pd

def preprocessor(data, data_region):
    # Keep only Summer Olympics
    data = data[data["Season"] == "Summer"]

    # Merge with region info
    data = data.merge(data_region, how='left', on='NOC')

    # Drop duplicates
    data.drop_duplicates(inplace=True)

    # Convert Medal column into dummy variables (Gold, Silver, Bronze)
    data = pd.concat([data, pd.get_dummies(data["Medal"], dtype=int)], axis=1)

    return data

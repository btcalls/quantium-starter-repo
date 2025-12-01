import pandas as pd


def csv_to_df(path, columns_to_extract) -> pd.DataFrame:
    """Extracts and returns a DataFrame with specific columns, or all if none are provided.

    Parameters:
        path (str): The path of the CSV.
        columns_to_extract (Sequence[str]): The array of column names to extract.

    Returns:
        pd.DataFrame: A new DataFrame containing only the specified columns.
    """

    df = pd.read_csv(path)
    cleaned_df = clean_data(df)

    if not columns_to_extract:
        return cleaned_df

    return cleaned_df[columns_to_extract]


def clean_data(df):
    """Cleans the DataFrame by:
    - Removing dollar signs from the 'price' column and converting it to float.
    - Filter out products, only keeping "pink morsel".

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
    Returns:
        pd.DataFrame: The cleaned DataFrame with 'price' as float.
    """

    cleaned_df = df.copy()

    # Filter to keep only "pink morsel" products; Remove 'product' column
    cleaned_df = cleaned_df[cleaned_df["product"] == "pink morsel"]
    cleaned_df.drop(["product"], axis=1, inplace=True)

    # Remove dollar signs and convert 'price' to float
    cleaned_df["price"] = cleaned_df["price"] \
        .str.replace('$', '') \
        .astype(float)

    # Convert 'date' column to datetime
    cleaned_df["date"] = pd.to_datetime(cleaned_df["date"])

    return cleaned_df


def get_sales(df):
    """Creates a new DataFrame with an additional 'sales' column calculated as price * quantity.

    Args:
        df (pd.DataFrame): The DataFrame containing 'price' and 'quantity' columns.

    Returns:
        pd.DataFrame: A new DataFrame with the 'sales' column added. 
    """

    # Calculate sales and add as a new column
    df_with_sales = df.copy()
    df_with_sales['sales'] = df['price'] * df['quantity']

    # Drop price and quantity columns
    df_with_sales.drop(["price", "quantity"], axis=1, inplace=True)

    return df_with_sales


def load_data():
    """Loads and combines sales data from multiple CSV files into a single DataFrame.

    Returns:
        pd.DataFrame: A combined DataFrame containing sales data from all sources.
    """

    data_0 = csv_to_df("data/daily_sales_data_0.csv", [])
    data_0_with_sales = get_sales(data_0)
    data_1 = csv_to_df("data/daily_sales_data_1.csv", [])
    data_1_with_sales = get_sales(data_1)
    data_2 = csv_to_df("data/daily_sales_data_2.csv", [])
    data_2_with_sales = get_sales(data_2)

    merged_df = pd.concat(
        [data_0_with_sales, data_1_with_sales, data_2_with_sales],
        ignore_index=True
    )

    return merged_df


if __name__ == "__main__":
    df = load_data()

    df.to_csv('data/combined_sales_data.csv', index=False)

#DATA CLEANING

import xml.etree.ElementTree as et
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt

def get_data(data_file_path, et=et ):
    '''
    Gets xml data for the steps data.

    Parameters
    data_file_path: file path to the steps data

    Types:

    Returns:
    - A dataframe containing all the records of the health data
    '''
    
    file_path=data_file_path

    tree = et.parse(file_path)
    root = tree.getroot()

    data = []

    for record in root.findall('Record'):
        if record.get('type'):
            child_elements={
                'type': record.get('type'),
                'source_name': record.get('sourceName'),
                'source_version': record.get('sourceVersion'),
                'device': record.get('sourceName'),
                'unit': record.get('unit'),
                'creation_date': record.get('creationDate'),
                'start_date': record.get('startDate'),
                'end_date': record.get('endDate'),
                'value': record.get('value')
            }

            data.append(child_elements)

    df = pd.DataFrame(data)
    
    return df
    

def clean_data(df):
    
    cols_to_keep = ['type','start_date', 'value', 'user']
    df = df[cols_to_keep]

    filter_for = ['HKQuantityTypeIdentifierStepCount']
    df = df[df['type'].isin(filter_for)]
    
    final_cols = ['start_date', 'value', 'user']
    df = df[final_cols]
    
    df['value'] = df['value'].astype(int)

    df['start_date'] = df['start_date'].str.split(' ').str[0]
    df['start_date'] = pd.to_datetime(df['start_date'])

    df = df.groupby(['start_date', 'user']).agg({'value':'sum'}).reset_index()

    df = df.rename(columns={'start_date': 'date'})

    return df



def clean_weather_data(df):
    
    cols_to_keep = ['datetime','tempmax', 'tempmin','temp','feelslikemax', 
                    'feelslikemin','feelslike','dew', 'humidity','precip',
                    'precipprob', 'precipcover','preciptype','snow', 'snowdepth',
                    'windgust','windspeed', 'sealevelpressure','cloudcover','visibility', 
                    'solarradiation','solarenergy','uvindex', 'severerisk','sunrise','sunset', 
                    'moonphase','conditions','description', 'icon']
    
    df = df[cols_to_keep]

    df['severerisk'] = df['severerisk'].fillna(0)
    df['preciptype'] = df['preciptype'].fillna("none")

    temp_cols_farenheight = [col for col in df.columns if 'temp' in col or "feels" in col]

    for col in temp_cols_farenheight:
       df[col] = (df[col] - 32) * 5 / 9
       df[col] = df[col].round(1)

    sun_times = [col for col in df.columns if 'sun' in col]
    
    for col in sun_times:
       df[col] = pd.to_datetime(df[col])
       df[col] = df[col].dt.time

    df = df.rename(columns={'datetime': 'date'})

    return df


def plot_by_months(df, target_year, start_month, end_month, colour, title):
    """
    Plots a bar chart of values from a DataFrame filtered by the specified months of a target year.

    Parameters:
    - df: DataFrame containing 'date', 'day', and 'value' columns.
    - target_year: The year to filter the data.
    - start_month: The starting month for filtering (1 to 12).
    - end_month: The ending month for filtering (1 to 12).
    - colour: Color of the bars in the plot.
    - title: Title of the plot.

    Returns:
    - DataFrame filtered for the specified date range.
    """

    if start_month < 1 or end_month > 12 or start_month > end_month:
        raise ValueError("Months must be between 1 and 12, and start_month must be less than or equal to end_month.")

    if end_month in [1, 3, 5, 7, 8, 10, 12]:
        last_day_of_end_month = 31
    elif end_month in [4, 6, 9, 11]:
        last_day_of_end_month = 30
    else:
        if (target_year % 4 == 0 and target_year % 100 != 0) or (target_year % 400 == 0):
            last_day_of_end_month = 29
        else:
            last_day_of_end_month = 28

    start_date = pd.Timestamp(year=target_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=target_year, month=end_month, day=last_day_of_end_month)

    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if filtered_df.empty:
        print("No data available for the selected date range.")
        return filtered_df

    plt.figure(figsize=(8, 5))
    plt.bar(filtered_df['day'], filtered_df['value'], color=colour, edgecolor='black')
    plt.title(title)
    plt.xlabel('Day')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()        
    plt.show()
























def drop_cols(cols, df):
    
    '''

    Drop one or multiple columns

    Parameters
    cols: columns to be dropped
    df: DataFrame to manipulate

    Types:
    cols: List

    Returns:
    - A copy of the original dataframe with columns dropped
    
    '''

    df_copy = df.copy()

    if not isinstance(cols, list):
        raise ValueError(
            "types to drop should be a LIST containing any of the following: [StepCount, DistanceWalkingRunning, FlightsClimbed, HeadphoneAudioExposure]")
    
    if any(col not in df_copy.columns for col in cols):
        raise ValueError("Some columns in 'cols' do not exist in the DataFrame.")
    
    df_copy = df_copy.drop(columns=cols)

    return df_copy


def remove_strings(cols, strings, df):
    
    '''
    
    Remove sepecified strings from specified columns in df.

    Parameters:
    - cols: list of column headers to be checked.
    - strings: list of strings to be removed from the list of cols.
    - df: The dataframe to be checked

    Returns:
    - A copy of the dataframe stripped of specified strings which will be lowercased.
    '''

    df_copy = df.copy()

    for col in cols:
        if col in df_copy.columns:
            for string in strings:
                df_copy[col] = df_copy[col].str.replace(string, ' ', regex=False)
            df_copy[col] = df_copy[col].str.strip()

    return df_copy




def find_row_by_value(col, value, df):

    '''
    
    Find rows given a specic value

    Parameters:
    col: column to search
    value: value to search within column
    df: DataFrame to manipulate

    Types:
    col: string
    value: string

    Returns:
    Copy of the dataframe including only the rows containing the specified values
    '''

    df_copy = df.copy()

    # if not isinstance(value, str):
    #      raise ValueError("type_value should be a string")

    if value not in df_copy[col].values:
        raise ValueError(f"{value} does not exist in the '{col}' column")
    
    df_copy = df_copy[df_copy[col]==value]

    return df_copy


def split_cols(cols_dict, split_delimiter, df):

    """

    Split a DataFrame column in two (only in two) if the colum contains more than one value.

    Parameters:
    - cols_dict: takes a key and two values.  Key, the column to split. Value 1, name of first new col. Value 2, name of second new col.
    - split_delimiter: the delimiter for where to the values
    - df: DataFrame to split 

    Note: 
    The values cannot have the same name as the key
    """

    df_copy = df.copy()

    for col_to_split in cols_dict.keys():
        new_col_names = cols_dict[col_to_split]
        df_copy[[new_col_names[0], new_col_names[1]]] = df_copy[col_to_split].str.split(split_delimiter, n=1, expand=True)
        
        df_copy[new_col_names[0]] = df_copy[new_col_names[0]].str.strip()
        df_copy[new_col_names[1]] = df_copy[new_col_names[1]].str.strip()
        
        df_copy.drop(columns=col_to_split, inplace=True)
    return df_copy



def reorder_cols(order, df):
    '''

    Parameters:
    - order: a list of column names in desired order 
    '''
    df_copy = df.copy()
    df_copy = df_copy.reindex(columns=order)

    return df_copy

# CONSIDERATIONS
#         - Avoid copying dataframes.  very memory intensive



# WIDGETS

def display_note(output='', width='100%', height='50px'):
    entry = f'{output}'
    note = widgets.Textarea(
        value=entry,
        disabled=False,
        layout=widgets.Layout(width=width, height=height)
    )
    display(note)
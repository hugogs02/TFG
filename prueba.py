from sentinelsat import SentinelAPI

# Module for manipulating dates and times
import datetime

# Module to set filesystem paths appropriate for user's operating system
from pathlib import Path


# Enter product, data latency, observation start/end dates and domain boundaries for file search
# Selections are made using interactive Jupyter Notebook widgets
# Run this block *once* to generate menus
# When main function is run, it reads ".value" of each menu selection
# Do NOT re-run block if you change menu selections (re-running block resets menus to defaults)!

# Formatting settings for drop-down menus
style = {'description_width':'140px'}
layout = widgets.Layout(width='300px')

# Create drop-down menus using widgets
product = widgets.Dropdown(options=[('Aerosol Index', 'AI'), ('Aerosol Layer Height', 'ALH'), ('Carbon Monoxide', 'CO'), ('Formaldehyde', 'HCHO'), ('Nitrogen Dioxide', 'NO2'), ('Sulfur Dioxide', 'SO2')], description='Product:', style=style, layout=layout)
latency = widgets.Dropdown(options=[('Near real time'), ('Offline'), ('Reprocessing') ], description='Data Latency:', style=style, layout=layout)
start_year = widgets.Dropdown(options=[('2018'), ('2019'), ('2020'), ('2021'), ('2022'), ('2023'), ('2024')], description='Start Year:', style=style, layout=layout)
start_month = widgets.Dropdown(options=[('Jan', '01'), ('Feb', '02'), ('Mar', '03'), ('Apr', '04'), ('May', '05'), ('Jun', '06'), ('Jul', '07'), ('Aug', '08'), ('Sep', '09'), ('Oct', '10'), ('Nov', '11'), ('Dec', '12')], description='Start Month:', style=style, layout=layout)
start_day = widgets.Dropdown(options=[('01'), ('02'), ('03'), ('04'), ('05'), ('06'), ('07'), ('08'), ('09'), ('10'), ('11'), ('12'), ('13'), ('14'), ('15'), ('16'), ('17'), ('18'), ('19'), ('20'), ('21'), ('22'), ('23'), ('24'), ('25'), ('26'), ('27'), ('28'), ('29'), ('30'), ('31')], description='Start Day:', style=style, layout=layout)
end_year = widgets.Dropdown(options=[('2018'), ('2019'), ('2020'), ('2021'), ('2022'), ('2023'), ('2024')], description='End Year:', style=style, layout=layout)
end_month = widgets.Dropdown(options=[('Jan', '01'), ('Feb', '02'), ('Mar', '03'), ('Apr', '04'), ('May', '05'), ('Jun', '06'), ('Jul', '07'), ('Aug', '08'), ('Sep', '09'), ('Oct', '10'), ('Nov', '11'), ('Dec', '12')], description='End Month:', style=style, layout=layout)
end_day = widgets.Dropdown(options=[('01'), ('02'), ('03'), ('04'), ('05'), ('06'), ('07'), ('08'), ('09'), ('10'), ('11'), ('12'), ('13'), ('14'), ('15'), ('16'), ('17'), ('18'), ('19'), ('20'), ('21'), ('22'), ('23'), ('24'), ('25'), ('26'), ('27'), ('28'), ('29'), ('30'), ('31')], description='End Day:', style=style, layout=layout)

# Caption for map domain boundaries
domain_caption = widgets.Label(value='ENTER LATITUDE/LONGITUDE BOUNDARIES FOR SEARCH AREA (use up/down arrows or type in value)', layout=widgets.Layout(height='30px'))

# Format observation start/end dates menus to display side-by-side
start_date = widgets.HBox([start_year, start_month, start_day])
end_date = widgets.HBox([end_year, end_month, end_day])

# Create numerical (float) text entry widgets for map boundary corners
west_lon_float = widgets.BoundedFloatText(description='Western-most Longitude:', value=0, min=-180, max=180, disabled=False, layout=widgets.Layout(width='250px', height='30px'), style={'description_width':'150px'})
east_lon_float = widgets.BoundedFloatText(description='Eastern-most Longitude:', value=0, min=-180, max=180, disabled=False, layout=widgets.Layout(width='250px', height='30px'), style={'description_width':'150px'})
lon_label = widgets.Label(value='(use negative values to indicate °W, e.g., 100 °W = -100)', layout=widgets.Layout(width='400px'))
lon_box = widgets.HBox([west_lon_float, east_lon_float, lon_label])
north_lat_float = widgets.BoundedFloatText(description='Northern-most Latitude:', value=0, min=-90, max=90, disabled=False, layout=widgets.Layout(width='400px', height='30px'), style={'description_width':'300px'})
south_lat_float = widgets.BoundedFloatText(description='Southern-most Latitude:', value=0, min=-90, max=90, disabled=False, layout=widgets.Layout(width='400px', height='30px'), style={'description_width':'300px'})
lat_label = widgets.Label(value='(use negative values to indicate °S, e.g., 30 °S = -30)', layout=widgets.Layout(width='400px'))
north_lat_box = widgets.HBox([north_lat_float, lat_label])
south_lat_box = widgets.HBox([south_lat_float, lat_label])

# Display drop-down menus
print('If you change menu selections (e.g., to run another search), do NOT re-run this block!\nRe-running will re-set all menus to their defaults!')
display(product, latency)
display(start_date, end_date)
display(domain_caption, north_lat_box, lon_box, south_lat_box)


# Convert user-entered date format to that used by Sentinel API
# "year", "month", "day": parameter variables from widget menu, set in main function

def convert_date_sentinel_api_format(year, month, day):
    # Add dashes b/w year/month and month/day
    formatted_date = year + '-' + month + '-' + day

    return formatted_date


# Get product abbrevation used in TROPOMI file name
# "product": parameter variable from widget menu, set in main function

def get_tropomi_product_abbreviation(product):
    if product == 'CO':
        return 'L2__CO____'
    elif product == 'NO2':
        return 'L2__NO2___'
    elif product == 'SO2':
        return 'L2__SO2___'
    elif product == 'HCHO':
        return 'L2__HCHO__'
    elif product == 'AI':
        return 'L2__AER_AI'
    elif product == 'ALH':
        return 'L2__AER_LH'

    return ''


# Create list of TROPOMI data file names for user-entered product, latency, search region, and date range
# "product_abbreviation": parameter variable from "get_tropomi_product_abbreviation(product)" function
# "start_date", "end_date": parameter variables from "convert_date_sentinel_api_format(year, month, day)" function
# "west_lon", "east_lon", "south_lat", "north_lat", "latency": parameter variables from widget menus, set in main function

def tropomi_list_files(west_lon, east_lon, south_lat, north_lat, start_date, end_date, product_abbreviation, latency):
    # Access S5P Data Hub using guest login credentials
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Query API for specified region, start/end dates, data product
    footprint = 'POLYGON((' + west_lon + ' ' + south_lat + ',' + east_lon + ' ' + south_lat + ',' + east_lon + ' ' + north_lat + ',' + west_lon + ' ' + north_lat + ',' + west_lon + ' ' + south_lat + '))'
    try:
        products = api.query(area=footprint, date=(start_date + 'T00:00:00Z', end_date + 'T23:59:59Z'),
                             producttype=product_abbreviation, processingmode=latency)
    except:
        print('Error connecting to SciHub server. This happens periodically. Run code again.')

    # Convert query output to pandas dataframe (df) (part of Sentinelsat library)
    products_df = api.to_dataframe(products)

    # Extract data file names from dataframe to list
    if len(products_df) > 0:
        file_name_list = products_df['filename'].tolist()
        file_size_list = products_df['size'].tolist()
    else:
        file_name_list = []
        file_size_list = []

    return file_name_list, file_size_list, products


# Download TROPOMI data files
# "save_path": parameter variable set in main function
# "products": parameter variable from "tropomi_list_files( )" function

def tropomi_download_files(products, save_path):
    # Query S5P Data Hub using guest login credentials
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Download data files to specified subdirectory
    # Note: Sentinelsat library includes tqdm download progress bar
    try:
        api.download_all(products, save_path)
    except KeyboardInterrupt:
        print('\nDownload was interrupted by user.')


# Print available TROPOMI data files that match user specifications, with option to download files
# "save_path": parameter variable set in main function
# "product_abbreviation": parameter variable from "get_tropomi_product_abbreviation(product)" function
# "start_date", "end_date": parameter variables from "convert_date_sentinel_api_format(date)" function
# "west_lon", "south_lat", "east_lon", "north_lat", "latency": parameter variables from widget menus, set in main function

def get_tropomi_files(west_lon, east_lon, south_lat, north_lat, start_date, end_date, product_abbreviation, latency,
                      save_path):
    # Query S5P Data Hub and list file names matching user-entered info
    file_name_list, file_size_list, products = tropomi_list_files(west_lon, east_lon, south_lat, north_lat, start_date,
                                                                  end_date, product_abbreviation, latency)

    # Print list of available file names/sizes
    if len(file_name_list) > 0:
        print('\nList of available data files (file size):')
        for file, size in zip(file_name_list, file_size_list):
            print(file, ' (', size, ')', sep='')

        # Print directory where files will be saved
        print('\nData files will be saved to:', save_path)

        # Ask user if they want to download the available data files
        # If yes, download files to specified directory
        download_question = 'Would you like to download the ' + str(
            len(file_name_list)) + ' files?\nType "yes" or "no" and hit "Enter"\n'
        ask_download = input(download_question)
        if ask_download in ['yes', 'YES', 'Yes', 'y', 'Y']:
            tropomi_download_files(products, save_path)
        else:
            print('\nFiles are not being downloaded.')
    else:
        print('\nNo files retrieved.  Check settings and try again.')


# Execute search to find available TROPOMI L2 data files, with option to download files
# Get values from widget menus (search parameters) using ".value"

# Main function
if __name__ == '__main__':
    # Set directory to save downloaded files (as pathlib.Path object)
    # Use current working directory for simplicity
    save_path = Path.cwd()

    # Get TROPOMI product abbreviation used in file name
    product_abbreviation = get_tropomi_product_abbreviation(product.value)

    # Change user-entered observation year/month/day for observation period to format used by Sentinel API
    start_date = convert_date_sentinel_api_format('2023', '06', '01')
    end_date = convert_date_sentinel_api_format('2023', '06', '15')

    # Convert latitude/longitude values entered as floats to string format used by Sentinel API
    west_lon = str(west_lon_float.value)
    east_lon = str(east_lon_float.value)
    south_lat = str(south_lat_float.value)
    north_lat = str(north_lat_float.value)

    # Execute script
    get_tropomi_files('-10.177733302116385', '4.798831343650816', '44.52157244578214', '35.55367980635542', start_date, end_date, 'L2__CO____',
                      'Offline', save_path)
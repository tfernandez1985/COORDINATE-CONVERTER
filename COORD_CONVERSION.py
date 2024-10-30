import PySimpleGUI as sg
import pandas as pd
import pyproj
import os

def convert_coordinates_to_wgs84(northings, eastings, projection):
    # Convert Northing and Easting coordinates to Latitude and Longitude
    longitudes, latitudes = pyproj.transform(projection, pyproj.Proj(init='epsg:4326'), eastings.values, northings.values)
    return longitudes, latitudes

def convert_coordinates_to_ne(latitudes, longitudes, projection):
    # Convert Latitude and Longitude coordinates to Northing and Easting
    eastings, northings = pyproj.transform(pyproj.Proj(init='epsg:4326'), projection, longitudes.values, latitudes.values)
    return eastings, northings

def get_projection_for_event(event):
    # Define the appropriate UTM projection based on the selected event
    if event == 'TEXAS CENTRAL':
        return pyproj.Proj(init='epsg:2277 +datum=NAD83 +units=us-ft', preserve_units=True)
    elif event == 'NEW MEXICO EAST':
        return pyproj.Proj(init='epsg:2257 +datum=NAD83 +units=us-ft', preserve_units=True)
    elif event == 'TEXAS SOUTH CENTRAL':
        return pyproj.Proj(init='epsg:2278 +datum=NAD83 +units=us-ft', preserve_units=True)
    elif event == 'TEXAS SOUTH':
        return pyproj.Proj(init='epsg:6585 +datum=NAD83 +units=us-ft', preserve_units=True)
    elif event == 'TEXAS NORTH CENTRAL':
        return pyproj.Proj(init='epsg:2276 +datum=NAD83 +units=us-ft', preserve_units=True)
    else:
        return None

def main():
    sg.theme('DARKTEAL11')  # Set theme
    layout = [
        [sg.Text('SURVEY COORDINATE CONVERTER', text_color='white', font=('Helvetica', 16, 'italic', 'bold'))],
        [sg.Text('')],
        [sg.Text('SELECT CONVERSION TYPE:', text_color='white', font=('Helvetica', 14, 'italic', 'bold'))],
        [sg.Combo(['Northing/Easting to WGS84', 'WGS84 to Northing/Easting'], default_value='Northing/Easting to WGS84', key='-CONVERSION_TYPE-', readonly=True)],
        [sg.Text('Select a CSV file:', font=('Helvetica', 14))],
        [sg.InputText(key='-FILE-'), sg.FileBrowse()],
        [sg.Button('TEXAS CENTRAL'), sg.Button('NEW MEXICO EAST'), sg.Button('TEXAS SOUTH CENTRAL'), sg.Button('TEXAS SOUTH'), sg.Button('TEXAS NORTH CENTRAL')],
        [sg.Text('Preview Converted Coordinates:', font=('Helvetica', 14))],
        [sg.Output(size=(99, 20), key='-COORDINATES_PREVIEW-')]
    ]

    window = sg.Window('CONVERTER', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        if event in ['TEXAS CENTRAL', 'NEW MEXICO EAST', 'TEXAS SOUTH CENTRAL', 'TEXAS SOUTH', 'TEXAS NORTH CENTRAL']:
            file_path = values['-FILE-']
            conversion_type = values['-CONVERSION_TYPE-']

            try:
                df = pd.read_csv(file_path)
                projection = get_projection_for_event(event)

                if conversion_type == 'Northing/Easting to WGS84':
                    if 'Northing' in df.columns and 'Easting' in df.columns:
                        longitudes, latitudes = convert_coordinates_to_wgs84(df['Northing'], df['Easting'], projection)
                        df['Longitude'] = longitudes
                        df['Latitude'] = latitudes
                        df.to_csv(file_path, index=False)  # Save directly to the original CSV file
                        print(f"Coordinates added to the original CSV file: {file_path}")
                        print(df)
                    else:
                        print("CSV file must have 'Northing' and 'Easting' columns.")

                elif conversion_type == 'WGS84 to Northing/Easting':
                    if 'Latitude' in df.columns and 'Longitude' in df.columns:
                        eastings, northings = convert_coordinates_to_ne(df['Latitude'], df['Longitude'], projection)
                        df['Northing'] = northings
                        df['Easting'] = eastings
                        df.to_csv(file_path, index=False)  # Save directly to the original CSV file
                        print(f"Coordinates added to the original CSV file: {file_path}")
                        print(df)
                    else:
                        print("CSV file must have 'Latitude' and 'Longitude' columns.")
            except Exception as e:
                print(f"Error reading or converting coordinates: {e}")
        
    window.close()

if __name__ == '__main__':
    main()

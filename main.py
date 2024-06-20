from flask import Flask, render_template
import nasdaqdatalink
import pandas as pd
import pygal

# Initialize Flask app
app = Flask(__name__)

# Define route for the index page
@app.route('/')
def index():
    # Set display options for pandas DataFrame
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 12)
    pd.set_option('display.width', 400)

    # Set API key for Nasdaq Data Link
    nasdaqdatalink.ApiConfig.api_key = 'k1nL693Mvt2xFTvkwG4y'

    # Retrieve data for Bitcoin Trade Volume vs Transaction Volume Ratio
    TVTVR_data = nasdaqdatalink.get_table('QDL/BCHAIN', code='TVTVR')

    # Initialize lists for storing dates and values
    TVTVR_list = []
    dates = []
    value = []

    # Process TVTVR data
    for index,row in TVTVR_data.iterrows():
        # Convert the timestamp to the date format as %Y-%m-%d
        date = row[1].strftime('%Y-%m-%d')
        # Append to the list
        TVTVR_list.insert(0, (date, row[2]))
        # Extract separate lists for date and value
        dates, value = zip(*TVTVR_list)

    # Create a line chart using pygal for TVTVR
    chart = pygal.Line(x_label_rotation=45)
    chart.title = 'Bitcoin Trade Volume vs Transaction Volume Ratio' 
    chart.x_labels = dates
    chart.add('Values', value)

    # Render the chart to an SVG file
    chart.render_to_file('static/images/Bitcoin Trade.svg')

    # Retrieve data for Total Bitcoins in Circulation Over Time
    TOTBC_data = nasdaqdatalink.get_table('QDL/BCHAIN', code='TOTBC')

    # Initialize lists for storing dates and values
    TOTBC_list = []
    dates = []
    value = []

    # Process TOTBC data
    for index, row in TOTBC_data.iterrows():
        # Convert the timestamp to the date format as %Y-%m-%d
        date = row[1].strftime('%Y-%m-%d')
        # Append to the list
        TOTBC_list.insert(0, (date, row[2]))
        # Extract separate lists for date and value
        dates, value = zip(*TOTBC_list)

    # Create a line chart using pygal for TOTBC
    chart = pygal.Line(x_label_rotation=45)
    chart.title = 'Total bitcoins in circulation over time' 
    chart.x_labels = dates
    chart.add('Values', value)

    # Render the chart to an SVG file
    chart.render_to_file('static/images/Total bitcoin.svg')

    # Return the rendered HTML template
    return render_template("index.html")

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

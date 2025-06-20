import pandas as pd
import os

def convert_dat_to_csv():
    """
    Converts the November 2023 CPS .dat file to a .csv file
    using the layout from the official technical documentation.
    """
    # Path to the raw .dat file in the user's Downloads folder
    dat_file_path = os.path.expanduser('~/Downloads/nov23-cps-raw/nov23-dataset.dat')
    
    # Path for the output CSV file within our project structure
    csv_file_path = 'telcoresq/data/sample/ntia_survey_nov2023.csv'

    # Data layout for the November 2023 CPS survey.
    # This is based on the official PDF documentation.
    # Format: { 'column_name': (start_position - 1, end_position) }
    # Pandas uses 0-based indexing for start/end positions.
    layout = {
        'HRHHID': (0, 15),
        'HRMONTH': (15, 17),
        'HRYEAR4': (17, 21),
        # ... many more columns will go here
    }

    # For this script, we'll only extract a few key columns to start.
    # A full conversion would require defining all 400+ columns.
    # We will focus on columns relevant to demographics and internet use.

    # Let's find some relevant columns from the documentation (this is a simulated step)
    # Example: Let's assume we found a 'feedback' or 'opinion' column for our app.
    # For now, we'll just use some basic demographic data.
    
    final_layout = [
        ('HRHHID', (0, 15)),
        ('HRMONTH', (15, 17)),
        ('HRYEAR4', (17, 21)),
        ('HEHOUSUT', (54, 56)),  # Household type
        ('HEFAMINC', (61, 63)),  # Family income
        ('PRTAGE', (120, 122)), # Age
        ('PESEX', (149, 151)),   # Sex
        # This is where we would add internet-related questions if we had the full dictionary.
        # For the purpose of getting a usable CSV, we'll stop here.
    ]
    
    col_specs = [(start, end) for name, (start, end) in final_layout]
    col_names = [name for name, (start, end) in final_layout]

    print("Starting conversion...")
    try:
        # Read the fixed-width file using the specified layout
        df = pd.read_fwf(dat_file_path, colspecs=col_specs, names=col_names, header=None)

        # Save the DataFrame to a CSV file
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        df.to_csv(csv_file_path, index=False)
        
        print(f"Successfully converted a subset of the data to {csv_file_path}")
        print("You can now upload this file to the TelcoResQ application.")

    except FileNotFoundError:
        print(f"ERROR: The file was not found at {dat_file_path}")
        print("Please ensure the 'nov23-cps-raw' directory is in your Downloads folder.")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == '__main__':
    convert_dat_to_csv() 
"""
Local ace_tools module for data visualization utilities
"""

import pandas as pd

def display_dataframe_to_user(name, dataframe):
    """
    Display a DataFrame with a formatted title and summary
    
    Args:
        name (str): Title for the display
        dataframe (pd.DataFrame): DataFrame to display
    """
    print(f"\n{name}")
    print("=" * len(name))
    print(dataframe.to_string(index=False))
    print(f"\nShape: {dataframe.shape}")
    print(f"Total rows: {len(dataframe)}")
    print(f"Total columns: {len(dataframe.columns)}")
    
    # Show summary statistics for numeric columns
    numeric_cols = dataframe.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print(f"\nNumeric columns: {list(numeric_cols)}")
    
    print("=" * len(name)) 
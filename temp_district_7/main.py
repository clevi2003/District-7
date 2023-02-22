import pandas as pd
import numpy as np

def main():
    demographics = pd.read_excel('2015-2019_neighborhood_tables_2021.12.21.xlsm', sheet_name=1)
    print(demographics.head(20))
    print(demographics.columns)
    for col in demographics.columns:
        print(demographics[col].value_counts())

if __name__ == "__main__":
    main()
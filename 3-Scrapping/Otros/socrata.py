# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 14:22:51 2021

@author: Matias Harari
"""

!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("odn.data.socrata.com", None)

# Example authenticated client (needed for non-public datasets):
 client = Socrata("odn.data.socrata.com",
                  "dzwie1eJdZmRPBRVyJv2XOtBJ",
                  userame="matias.harari@gmail.com",
                  password="dzwie1eJdZmRPBRVyJv2XOtBJ")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("tt5s-y5fc", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv('crime.csv', header=True, index=False)



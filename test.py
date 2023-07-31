import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
from io import StringIO
import datetime
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from sklearn.model_selection import TimeSeriesSplit

st.write("""# Predicting IoC Study Case LA""")

text = '''
<div style="text-align: justify;">
This dataset represents a comprehensive record of crime incidents within the City of Los Angeles, starting from 2020. The data is sourced from original crime reports, which were originally typed on paper, introducing the possibility of some inaccuracies. Certain location fields may contain missing data denoted as (0°, 0°). To prioritize privacy, address fields are limited to the nearest hundred block. While the data is generally reliable, any questions or concerns can be addressed through comments. Explore this dataset to uncover trends, patterns, and gain a deeper understanding of crime in Los Angeles.
</div>
'''
st.markdown(text, unsafe_allow_html=True)

st.write("""Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kt4Sbrk-A1uMyzYDbOHmUEEUs3zLEO89

Data Understanding:

1. 'DR_NO' : CaseID
2. 'Date Rptd' : Reported Date
3. 'DATE OCC' : Date Occured
4. 'TIME OCC' : Time Occured
5. 'AREA' : Area of Crime
6. 'AREA NAME' : Name of The Area
7. 'Rpt Dist No' : District Number of Incident
8. 'Part 1-2'
9. 'Crm Cd' : Police Code for Crime
10. 'Crm Cd Desc' : Crime Description
11. 'Mocodes' : Mocodes
12. 'Vict Age' : Victim Age
13. 'Vict Sex' : Victim Gender
14. 'Vict Descent' : Victim Descent
15. 'Premis Cd' : Premis Code
16. 'Premis Desc' : Premis Description
17. 'Weapon Used Cd' : Weapon Used Code
18. 'Weapon Desc' : Weapon Used Description
19. 'Status' : Status Code
20. 'Status Desc' : Status Description
21. 'Crm Cd 1' : CRM code 1
22. 'Crm Cd 2' : CRM code 2
23. 'Crm Cd 3' : CRM code 3
24. 'Crm Cd 4' : CRM code 4
25. 'LOCATION' : Location
26. 'Cross Street' : Cross Street
27. 'LAT' : Lat
28. 'LON' : Long """)

# Create a file uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# If a file is uploaded, read the data from the CSV file
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

    # Display the data in Streamlit app
    st.title('Los Angeles Crime Data')
    st.dataframe(data)

# Remove time from date rptd and date occ
data['Date Rptd'] = data['Date Rptd'].str[:19]
data['DATE OCC'] = data['DATE OCC'].str[:19]

# Convert datetime column

data['Date Rptd'] = pd.to_datetime(data['Date Rptd'], format = '%m/%d/%Y %H:%M:%S')
data['DATE OCC'] = pd.to_datetime(data['DATE OCC'], format = '%m/%d/%Y %H:%M:%S')

# Create New Dataframe
ioc_df = data[['Date Rptd','AREA']]

# Group by date rptd and area name
ioc_df = ioc_df.groupby(['Date Rptd', 'AREA']).size().reset_index(name='Count')

# Convert datetime into split date
def creature_features(ioc_df):
    """
    Create time series features based on time series index
    """
    ioc_df = ioc_df.copy()
    ioc_df['hour'] = ioc_df['Date Rptd'].dt.hour
    ioc_df['dayofweek'] = ioc_df['Date Rptd'].dt.dayofweek
    ioc_df['quarter'] = ioc_df['Date Rptd'].dt.quarter
    ioc_df['month'] = ioc_df['Date Rptd'].dt.month
    ioc_df['year'] = ioc_df['Date Rptd'].dt.year
    ioc_df['dayofyear'] = ioc_df['Date Rptd'].dt.dayofyear
    return ioc_df

ioc_df = creature_features(ioc_df)

# Initialize TimeSeriesSplit
tss = TimeSeriesSplit(n_splits=5)

# Get the indices for the first fold
train_index, test_index = next(tss.split(ioc_df))

# Split the data into train and test sets based on TimeSeriesSplit for the first fold
train_data, test_data = ioc_df.iloc[train_index], ioc_df.iloc[test_index]

# Define X_train, y_train using data from the first fold
X_train = train_data[['AREA', 'dayofweek', 'quarter', 'month', 'year', 'dayofyear']]
y_train = train_data['Count']

# Add constant for the model
X_train = sm.add_constant(X_train)

# Create and fit the Poisson regression model using data from the first fold
model = sm.GLM(y_train, X_train, family=sm.families.Poisson())
result = model.fit()

# Extract the constant value from the model results
const_value = result.params['const']

# Function to output prediction based on user input
def predict_user_input(AREA,
                       dayofweek,
                       quarter,
                       month,
                       year,
                       dayofyear):
                           
    # Reshape the user input into a 2-dimensional numpy array
    user_input = np.array([[const_value, AREA, dayofweek, quarter, month, year, dayofyear]])
    
    # Use the Poisson regression model to predict on the user input
    prediction = result.predict(user_input).round(0)
    
    return prediction[0]  # Return the predicted value


def main():
    st.title("Crime Prediction App")
    st.write("Enter the following parameters to predict the crime:")

    # Using streamlit's slider and selectbox widgets to take user input
    AREA = st.slider("Select Day of Week", 1, 21)
    dayofweek = st.slider("Select Day of Week", 0, 6)
    quarter = st.slider("Select Quarter", 1, 4)
    month = st.slider("Select Month", 1, 12)
    year = st.slider("Select Year", 2020, 2025)
    dayofyear = st.slider("Select Day of Year", 1, 366)

    # Button to trigger the prediction
    if st.button("Predict"):
        prediction = predict_user_input(AREA, dayofweek, quarter, month, year, dayofyear)
        st.write(f"Predicted crime: {prediction}")

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import pandas as pd

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


# Dataset URL (replace with your own dataset URL)
dataset_url = "https://drive.google.com/file/d/1NlSQCl4C9OupBKa8Tr63myMNjmD_SQmm/view?usp=drive_link"

# Function to load the dataset
@st.cache  # Cache the data to improve performance
def load_data():
    data = pd.read_csv(dataset_url)
    return data

# Load the data
df = load_data()

# Display the dataset in a Streamlit table
st.dataframe(df)

# Function to output prediction based on user input
def predict_user_input(AREA,
                       dayofweek,
                       quarter,
                       month,
                       year,
                       dayofyear):
    # Reshape the user input into a 2-dimensional numpy array
    user_input = np.array([[AREA, dayofweek, quarter, month, year, dayofyear]])
    
    # Use the XGBoost model to predict on the user input (replace 'reg' with your actual model)
    prediction = reg.predict(user_input).round(0)
    
    return prediction[0]  # Return the predicted value

def main():
    st.title("Crime Prediction App")
    st.write("Enter the following parameters to predict the crime:")

    # Using streamlit's slider and selectbox widgets to take user input
    AREA = st.selectbox("Select Area", ['Central', 'Rampart', 'Southwest', 'Hollenbeck', 'Harbor',
                                        'Hollywood', 'Wilshire', 'West LA', 'Van Nuys', 'West Valley',
                                        'Northeast', '77th Street', 'Newton', 'Pacific', 'N Hollywood',
                                        'Foothill', 'Devonshire', 'Southeast', 'Mission', 'Olympic',
                                        'Topanga'])

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

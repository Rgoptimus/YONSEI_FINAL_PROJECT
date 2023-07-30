import streamlit as st
from pyngrok import ngrok

# Function to output prediction based on user input
def predict_user_input(user_input):
    # Convert the user input to the required data types
    area_mapping = {'Central': 1, 'Rampart': 2, 'Southwest': 3, 'Hollenbeck': 4, 'Harbor': 5,
                    'Hollywood': 6, 'Wilshire': 7, 'West LA': 8, 'Van Nuys': 9, 'West Valley': 10,
                    'Northeast': 11, '77th Street': 12, 'Newton': 13, 'Pacific': 14, 'N Hollywood': 15,
                    'Foothill': 16, 'Devonshire': 17, 'Southeast': 18, 'Mission': 19, 'Olympic': 20,
                    'Topanga': 21}
    area = area_mapping[user_input['AREA']]
    dayofweek = int(user_input['dayofweek'])
    quarter = int(user_input['quarter'])
    month = int(user_input['month'])
    year = int(user_input['year'])
    dayofyear = int(user_input['dayofyear'])

    # Use the XGBoost model to predict on the user input
    prediction = reg.predict(np.array([[area, dayofweek, quarter, month, year, dayofyear]]))
    
    return prediction[0]  # Return the predicted value

# Using streamlit to take user input
st.title('Crime Prediction in Los Angeles')
st.write('Please enter the following information:')
area = st.selectbox('Area', ['Central', 'Rampart', 'Southwest', 'Hollenbeck', 'Harbor',
                             'Hollywood', 'Wilshire', 'West LA', 'Van Nuys', 'West Valley',
                             'Northeast', '77th Street', 'Newton', 'Pacific', 'N Hollywood',
                             'Foothill', 'Devonshire', 'Southeast', 'Mission', 'Olympic',
                             'Topanga'])
dayofweek = st.slider('Day of Week', 0, 6)
quarter = st.slider('Quarter', 1, 4)
month = st.slider('Month', 1, 12)
year = st.slider('Year', 2020, 2025)
dayofyear = st.slider('Day of Year', 1, 366)

user_input = {'AREA': area, 'dayofweek': dayofweek, 'quarter': quarter, 'month': month, 'year': year, 'dayofyear': dayofyear}

# Display the user input
st.write('User Input:')
st.write('Area:', user_input['AREA'])
st.write('Day of Week:', user_input['dayofweek'])
st.write('Quarter:', user_input['quarter'])
st.write('Month:', user_input['month'])
st.write('Year:', user_input['year'])
st.write('Day of Year:', user_input['dayofyear'])

# Predict the outcome
prediction = predict_user_input(user_input)

# Display the prediction
st.write('Prediction:')
st.write(prediction)

# Set the configuration for ngrok
ngrok_tunnel = ngrok.connect(port='8501')

# Print the public URL of the app
st.write('Public URL:', ngrok_tunnel.public_url)

# Run the Streamlit app
st.run()

import streamlit as st
import numpy as np

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

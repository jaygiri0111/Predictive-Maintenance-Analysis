import streamlit as st
import numpy as np
import joblib  # Replace pickle with joblib


# Function to Load the CatBoost Model
def load_model():
    model_path = 'predictive_analysis_model.pkl'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        st.error(f"Model file '{model_path}' not found!")
        return None

# @st.cache_resource
# def load_model():
#     # Load the CatBoost model using joblib
#     model = joblib.load('predictive_analysis_model.pkl')
#     return model


# Function to Map Failure Types
def map_failure_types():
    return {
        0: 'No Failure',
        1: 'Heat Dissipation Failure',
        2: 'Power Failure',
        3: 'Overstrain Failure',
        4: 'Tool Wear Failure',
        5: 'Random Failures'
    }


# Streamlit App
def main():
    st.title("Predictive Maintenance Analysis - Manual Input")
    # Add project description box with black text color
    st.markdown("""
    <div style="background-color:#f4f4f4; padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;">
        <h3>Project Name: Predictive Maintenance Analysis</h3>
        <p>This project uses machine learning techniques to predict the failure type of industrial equipment based on sensor data. 
        The model helps in anticipating potential failures, thereby allowing proactive maintenance and reducing downtime.</p>
        <p>Developed using a CatBoost model for predicting failure types based on input features like temperature, rotational speed, torque, etc.</p>
          <i> Deployed by : Jay prakash Giri (21053460), Bipin chaudhary (21053451)</i>
    </div>
    """, unsafe_allow_html=True)

    st.write("Enter the required input values below to make predictions.")

    # Input Fields for Manual Data Entry
    type_ = st.number_input("Type (e.g., (capacity)->'Low': 0, 'Medium': 1, 'High': 2", min_value=0, max_value=2,
                            step=1, format="%d")
    air_temp = st.number_input("Air Temperature (K):", format="%.4f")
    process_temp = st.number_input("Process Temperature (K):", format="%.4f")
    rotational_speed = st.number_input("Rotational Speed (RPM):", format="%.4f")
    torque = st.number_input("Torque (Nm):", format="%.4f")
    tool_wear = st.number_input("Tool Wear (minutes):", format="%.4f")
    temp_diff = st.number_input("Temperature Difference:", format="%.4f")
    temp_ratio = st.number_input("Temperature Ratio:", format="%.6f")
    rpm_diff = st.number_input("RPM Difference:", format="%.4f")
    rpm_ratio = st.number_input("RPM Ratio:", format="%.6f")

    # Validation to ensure all inputs are provided (no empty or default values)
    if air_temp == 0 or process_temp == 0 or rotational_speed == 0 or torque == 0 or tool_wear == 0 or \
            temp_diff == 0 or temp_ratio == 0 or rpm_diff == 0 or rpm_ratio == 0:
        st.error("Please ensure all input values are entered correctly before making a prediction.")
        return

    # Load Model
    model = load_model()

    # Make Prediction when "Predict" button is clicked
    if st.button("Predict"):
        input_data = np.array([[type_, air_temp, process_temp, rotational_speed, torque,
                                tool_wear, temp_diff, temp_ratio, rpm_diff, rpm_ratio]])

        prediction = model.predict(input_data)[0]  # Get the first (and only) prediction

        # Map Prediction to Failure Type
        failure_type_mapping = map_failure_types()
        predicted_label = failure_type_mapping.get(prediction.item(), "Unknown Failure Type")

        st.success(f"Predicted Failure Type: {predicted_label}")

if __name__ == '__main__':
    main()

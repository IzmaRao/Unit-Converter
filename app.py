import streamlit as st
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    body { background-color: #f8f9fa; }
    .stApp { background: linear-gradient(to right, #2c3e50, #4ca1af); color: white; padding: 20px; }
    .title { text-align: center; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
    .convert-btn { background-color: #17a2b8 !important; color: white; font-weight: bold; padding: 10px; border-radius: 8px; }
    .output { font-size: 24px; font-weight: bold; text-align: center; background: #212529; color: #f8f9fa; padding: 15px; border-radius: 10px; }
    .sidebar .block-container { background: #1c2833; padding: 20px; border-radius: 10px; }
    .history-container { width: 90% !important; margin: auto; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>🚀 Professional Unit Converter 🔄</h1>", unsafe_allow_html=True)

# Conversion dictionary
conversion_rates = {
    ("Meters", "Kilometers"): 0.001,
    ("Kilometers", "Meters"): 1000,
    ("Grams", "Kilograms"): 0.001,
    ("Kilograms", "Grams"): 1000,
    ("Celsius", "Fahrenheit"): lambda c: (c * 9/5) + 32,
    ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
}

# Sidebar
st.sidebar.header("⚙️ Conversion Settings")
unit_options = ["Meters", "Kilometers", "Grams", "Kilograms", "Celsius", "Fahrenheit"]
from_unit = st.sidebar.selectbox("From Unit:", unit_options)
to_unit = st.sidebar.selectbox("To Unit:", unit_options)
value = st.sidebar.number_input("Enter Value:", min_value=0.0, format="%.2f")

# Initialize session state
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []

# Convert Button
if st.sidebar.button("Convert", key="convert", help="Click to perform conversion"):
    conversion_key = (from_unit, to_unit)
    if conversion_key in conversion_rates:
        conversion_factor = conversion_rates[conversion_key]
        st.session_state.result = (
            conversion_factor(value) if callable(conversion_factor) else value * conversion_factor
        )
        st.sidebar.success(f"✅ Converted Value: {st.session_state.result:.2f} {to_unit}")
    else:
        st.session_state.result = None
        st.sidebar.error("⚠️ Invalid conversion type")

# Save Conversion Button
if st.sidebar.button("Save Conversion", key="save_conversion", help="Save this conversion to history"):
    if st.session_state.result is not None:
        st.session_state.history.append({
            "From": from_unit,
            "To": to_unit,
            "Value": value,
            "Result": st.session_state.result
        })
        st.sidebar.success("✅ Conversion saved successfully!")
    else:
        st.sidebar.error("⚠️ First perform a conversion before saving!")

# Display Conversion History
st.subheader("📊 Conversion History")
st.markdown("<div class='history-container'>", unsafe_allow_html=True)
df = pd.DataFrame(st.session_state.history)
st.dataframe(df, height=200, width=1300)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr><center>🌍 Built with ❤️ using Streamlit | © 2025</center>", unsafe_allow_html=True)

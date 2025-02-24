import streamlit as st
import openai
import pandas as pd
from openpyxl import load_workbook

# Set OpenAI API Key
openai.api_key = st.secrets["api_key"]

# Streamlit UI
st.title("💬 Profitability Chatbot")
st.write("Compare different LOBs based on key profitability metrics.")

# Load Local Excel File
file_path = r"Profitability_Dummy_Data.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(file_path)

df = load_data()
st.write("### Data Preview")
st.dataframe(df)

# Ensure Required Columns Exist
required_columns = {"Lob", "Date", "Revenue", "Interest Income", "Fee Income", 
                    "Interest Expense", "Net Interest Margin (%)", "Loan Growth (%)", 
                    "Credit Quality (NPL Ratio %)", "Operating Efficiency (Cost-to-Income Ratio %)", 
                    "Technology Investment", "Mortgage Origination", "Consumer Lending", "Deposit Growth"}

if not required_columns.issubset(df.columns):
    st.error("⚠️ Missing required columns!")
    st.stop()


# Check for missing values
missing_values = df.isnull().sum()
if missing_values.any():
    st.write("⚠️ **Missing Values in Columns:**")
    st.write(missing_values[missing_values > 0])
else:
    st.success("✅ No missing values detected!")

# Compare LOBs using a grouped table
st.write("### Profitability Insight")
lob_comparison = df.groupby("Lob").agg({
    "Revenue": ["mean", "min", "max"],
    "Interest Income": ["mean", "min", "max"],
    "Fee Income": ["mean", "min", "max"],
    "Interest Expense": ["mean", "min", "max"],
    "Net Interest Margin (%)": ["mean", "min", "max"],
    "Loan Growth (%)": ["mean", "min", "max"],
    "Credit Quality (NPL Ratio %)": ["mean", "min", "max"],
    "Operating Efficiency (Cost-to-Income Ratio %)": ["mean", "min", "max"],
    "Technology Investment": ["mean", "min", "max"],
    "Mortgage Origination": ["mean", "min", "max"],
    "Consumer Lending": ["mean", "min", "max"],
    "Deposit Growth": ["mean", "min", "max"],
}).reset_index()

# User Query
user_query = st.text_input("Enter your profitability-related question:")

if st.button("Get AI Insights") and user_query:
    try:
        # Create GPT-4 Prompt
        prompt = (f"You are an AI expert in profitability analysis. "
                  f"Here is a financial comparison of different LOBs:\n{lob_comparison.to_string()}\n\n"
                  f"Now, answer this question:\n{user_query}")

        # Get GPT-4 Response
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        gpt_insights = response["choices"][0]["message"]["content"]

        # Display AI Response
        st.subheader("📌 AI Insights")
        st.write(gpt_insights)

    except Exception as e:
        st.error(f"⚠️ Error generating AI insights: {e}")
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from scipy import stats

# Title of the Web App
st.title("Swiss Inflation Analysis (2000–2024)")
st.write("This simple web application shows inflation data, visualizations, and a statistical comparison.")

# Load data from SQLite database
conn = sqlite3.connect('inflation_ch.db')
df = pd.read_sql_query('SELECT * FROM inflation_data ORDER BY year', conn)
conn.close()

# Display Data Table
st.subheader("Inflation Table (2000–2024)")
st.dataframe(df)

# Line Chart
st.subheader("Inflation Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(df['year'], df['inflation_rate'], marker='o')
ax1.set_title("Inflation Trend in Switzerland")
ax1.set_xlabel("Year")
ax1.set_ylabel("Inflation (%)")
ax1.grid(True)
st.pyplot(fig1)

# Histogram
st.subheader("Distribution of Inflation Rates")
fig2, ax2 = plt.subplots()
ax2.hist(df['inflation_rate'], bins=10, edgecolor='black')
ax2.set_title("Histogram of Inflation Rates")
ax2.set_xlabel("Inflation (%)")
ax2.set_ylabel("Number of Years")
ax2.grid(True)
st.pyplot(fig2)

# T-Test (Statistical Analysis)
st.subheader("Statistical Analysis (T-Test)")
group_1 = df[(df['year'] >= 2000) & (df['year'] <= 2010)]['inflation_rate']
group_2 = df[(df['year'] >= 2011) & (df['year'] <= 2024)]['inflation_rate']
t_stat, p_value = stats.ttest_ind(group_1, group_2, equal_var=False)

st.write(f"**T-statistic**: {t_stat:.4f}")
st.write(f"**P-value**: {p_value:.4f}")

if p_value < 0.05:
    st.success("There is a significant difference between the two periods (p < 0.05).")
else:
    st.info("There is no significant difference between the two periods (p ≥ 0.05).")

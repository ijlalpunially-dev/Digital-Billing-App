import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Digital Billing App", page_icon="💡", layout="centered")

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #0f172a;
        color: white;
    }
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 2px 2px 10px #00ffcc;
    }
    .result-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='main-title'>💡 Digital Billing App</h1>", unsafe_allow_html=True)

# Category selection
category = st.selectbox("🏷️ Select Consumer Type:", ["Domestic", "Commercial", "Industrial"])

# Inputs
col1, col2 = st.columns(2)
with col1:
    units = st.number_input("⚡ Enter Meter Reading (Units Consumed):", min_value=0, step=1)
with col2:
    fine = st.number_input("💰 Enter Fine Amount (if any):", min_value=0, step=1)

# Slab rates for each category
rates = {
    "Domestic": [(100, 3), (500, 4), (float("inf"), 6)],
    "Commercial": [(100, 5), (500, 7), (float("inf"), 10)],
    "Industrial": [(100, 8), (500, 12), (float("inf"), 15)],
}

# Function to calculate bill with breakdown
def calculate_bill(units, fine, category):
    cost = 0
    breakdown = []
    if units <= 100:
        cost = units * rates[category][0][1]
        breakdown.append(["0 - 100", units, rates[category][0][1], cost])
    elif units <= 500:
        cost = (100 * rates[category][0][1]) + ((units - 100) * rates[category][1][1])
        breakdown.append(["0 - 100", 100, rates[category][0][1], 100 * rates[category][0][1]])
        breakdown.append(["101 - 500", units - 100, rates[category][1][1], (units - 100) * rates[category][1][1]])
    else:
        cost = (100 * rates[category][0][1]) + (400 * rates[category][1][1]) + ((units - 500) * rates[category][2][1])
        breakdown.append(["0 - 100", 100, rates[category][0][1], 100 * rates[category][0][1]])
        breakdown.append(["101 - 500", 400, rates[category][1][1], 400 * rates[category][1][1]])
        breakdown.append(["> 500", units - 500, rates[category][2][1], (units - 500) * rates[category][2][1]])

    total = cost + fine
    return cost, total, breakdown

# Calculate bill
cost, total, breakdown = calculate_bill(units, fine, category)

# Show results
st.markdown("<div class='result-box'>", unsafe_allow_html=True)
st.subheader("📑 Billing Details")
st.write(f"**Consumer Type:** {category}")
st.write(f"**Units Consumed:** {units}")
st.write(f"**Fine:** {fine} Rs")

# Show breakdown table
if breakdown:
    df = pd.DataFrame(breakdown, columns=["Slab", "Units", "Rate (Rs/unit)", "Cost (Rs)"])
    st.table(df)

st.info(f"⚡ Energy Charges: **{cost} Rs**")
st.success(f"💰 Total Bill: **{total} Rs**")
st.markdown("</div>", unsafe_allow_html=True)

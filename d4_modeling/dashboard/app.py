"""
Rental Market Dashboard - ZIP Code Profile Viewer
Baseball Savant-style dashboard for exploring rental market data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Rental Market Dashboard",
    page_icon="🏠",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/dashboard_data.csv')

df = load_data()

# Title
st.title("🏠 Rental Market Dashboard")
st.markdown("### ZIP Code Profile Viewer")
st.markdown("---")

# Sidebar - ZIP Code Selection
st.sidebar.header("Search ZIP Code")

# City filter
cities = sorted(df['city'].unique())
selected_city = st.sidebar.selectbox("Filter by City (optional)", ["All Cities"] + cities)

# Filter ZIPs by city
if selected_city == "All Cities":
    available_zips = sorted(df['geoid'].unique())
else:
    available_zips = sorted(df[df['city'] == selected_city]['geoid'].unique())

# ZIP selection
selected_zip = st.sidebar.selectbox("Select ZIP Code", available_zips)

# Get ZIP data
zip_data = df[df['geoid'] == selected_zip].iloc[0]

# ============================================================================
# HEADER SECTION
# ============================================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📍 ZIP Code",
        value=f"{int(zip_data['geoid'])}",
        delta=zip_data['city']
    )

with col2:
    st.metric(
        label="💵 Actual Rent",
        value=f"${zip_data['actual_rent']:,.0f}",
        delta=f"{zip_data['rent_discrepancy_pct']:.1f}%"
    )

with col3:
    st.metric(
        label="🎯 Predicted Rent",
        value=f"${zip_data['predicted_rent']:,.0f}",
        delta=f"${zip_data['rent_discrepancy_dollars']:,.0f}"
    )

# Discrepancy badge
if zip_data['rent_discrepancy_pct'] < -10:
    badge_color = "green"
    badge_text = "🟢 UNDERPRICED - Good Deal!"
elif zip_data['rent_discrepancy_pct'] > 10:
    badge_color = "red"
    badge_text = "🔴 OVERPRICED - Expensive!"
else:
    badge_color = "gray"
    badge_text = "⚪ FAIR MARKET"

st.markdown(f"<h3 style='text-align: center; color: {badge_color};'>{badge_text}</h3>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# PERCENTILE RANKINGS
# ============================================================================
st.header("📊 Percentile Rankings")
st.markdown("*Compared to all 1,766 ZIP codes across 14 cities*")

# Function to create gauge chart
def create_gauge(value, title, subtitle=""):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': f"<b>{title}</b><br><span style='font-size:0.8em'>{subtitle}</span>"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightblue"},
                {'range': [75, 100], 'color': "royalblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=60, b=20))
    return fig

# RENT METRICS
st.subheader("🏠 RENT METRICS")
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(
        create_gauge(
            zip_data['actual_rent_percentile'],
            "Actual Rent",
            f"${zip_data['actual_rent']:,.0f}"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_gauge(
            zip_data['predicted_rent_percentile'],
            "Predicted Rent",
            f"${zip_data['predicted_rent']:,.0f}"
        ),
        use_container_width=True
    )

with col3:
    st.plotly_chart(
        create_gauge(
            zip_data['rent_discrepancy_pct_percentile'],
            "Rent Discrepancy",
            f"{zip_data['rent_discrepancy_pct']:.1f}%"
        ),
        use_container_width=True
    )

st.markdown("---")

# INCOME METRICS
st.subheader("💰 INCOME METRICS")
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(
        create_gauge(
            zip_data['median_income_percentile'],
            "Median Income",
            f"${zip_data['median_income']:,.0f}"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_gauge(
            zip_data['poverty_rate_percentile'],
            "Poverty Rate",
            f"{zip_data['poverty_rate']:.1f}%"
        ),
        use_container_width=True
    )

with col3:
    st.plotly_chart(
        create_gauge(
            zip_data['affluence_rate_percentile'],
            "Affluence Rate",
            f"{zip_data['affluence_rate']:.1f}%"
        ),
        use_container_width=True
    )

st.markdown("---")

# HOUSING METRICS
st.subheader("🏘️ HOUSING METRICS")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_gauge(
            zip_data['avg_housing_age_percentile'],
            "Avg Housing Age",
            f"{zip_data['avg_housing_age']:.0f} years"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_gauge(
            zip_data['housing_cost_burden_percentile'],
            "Housing Cost Burden",
            f"{zip_data['housing_cost_burden']:.1f}%"
        ),
        use_container_width=True
    )

st.markdown("---")

# POPULATION METRICS
st.subheader("👥 POPULATION METRICS")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_gauge(
            zip_data['population_growth_percentile'],
            "Population Growth",
            f"{zip_data['population_growth']:.1f}%"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_gauge(
            zip_data['population_density_percentile'],
            "Population Density",
            f"{zip_data['population_density']:.1f} per unit"
        ),
        use_container_width=True
    )

st.markdown("---")

# TRANSIT METRICS
st.subheader("🚇 TRANSIT METRICS")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_gauge(
            zip_data['transit_usage_percentile'],
            "Transit Usage",
            f"{zip_data['transit_usage']:.1f}%"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_gauge(
            zip_data['commute_time_percentile'],
            "Commute Time",
            f"{zip_data['commute_time']:.1f} min"
        ),
        use_container_width=True
    )

st.markdown("---")

# ============================================================================
# COMPARISON TABLE
# ============================================================================
st.header("📋 Detailed Metrics")

# Create comparison dataframe
comparison_data = {
    "Metric": [
        "Actual Rent",
        "Predicted Rent",
        "Rent Discrepancy",
        "Median Income",
        "Poverty Rate",
        "Affluence Rate",
        "Avg Housing Age",
        "Housing Cost Burden",
        "Population Growth",
        "Population Density",
        "Transit Usage",
        "Commute Time"
    ],
    "Value": [
        f"${zip_data['actual_rent']:,.0f}",
        f"${zip_data['predicted_rent']:,.0f}",
        f"{zip_data['rent_discrepancy_pct']:.1f}%",
        f"${zip_data['median_income']:,.0f}",
        f"{zip_data['poverty_rate']:.1f}%",
        f"{zip_data['affluence_rate']:.1f}%",
        f"{zip_data['avg_housing_age']:.0f} years",
        f"{zip_data['housing_cost_burden']:.1f}%",
        f"{zip_data['population_growth']:.1f}%",
        f"{zip_data['population_density']:.1f}",
        f"{zip_data['transit_usage']:.1f}%",
        f"{zip_data['commute_time']:.1f} min"
    ],
    "Percentile": [
        f"{zip_data['actual_rent_percentile']:.0f}th",
        f"{zip_data['predicted_rent_percentile']:.0f}th",
        f"{zip_data['rent_discrepancy_pct_percentile']:.0f}th",
        f"{zip_data['median_income_percentile']:.0f}th",
        f"{zip_data['poverty_rate_percentile']:.0f}th",
        f"{zip_data['affluence_rate_percentile']:.0f}th",
        f"{zip_data['avg_housing_age_percentile']:.0f}th",
        f"{zip_data['housing_cost_burden_percentile']:.0f}th",
        f"{zip_data['population_growth_percentile']:.0f}th",
        f"{zip_data['population_density_percentile']:.0f}th",
        f"{zip_data['transit_usage_percentile']:.0f}th",
        f"{zip_data['commute_time_percentile']:.0f}th"
    ],
    "City Avg": [
        f"${df[df['city'] == zip_data['city']]['actual_rent'].mean():,.0f}",
        f"${df[df['city'] == zip_data['city']]['predicted_rent'].mean():,.0f}",
        f"{df[df['city'] == zip_data['city']]['rent_discrepancy_pct'].mean():.1f}%",
        f"${df[df['city'] == zip_data['city']]['median_income'].mean():,.0f}",
        f"{df[df['city'] == zip_data['city']]['poverty_rate'].mean():.1f}%",
        f"{df[df['city'] == zip_data['city']]['affluence_rate'].mean():.1f}%",
        f"{df[df['city'] == zip_data['city']]['avg_housing_age'].mean():.0f} years",
        f"{df[df['city'] == zip_data['city']]['housing_cost_burden'].mean():.1f}%",
        f"{df[df['city'] == zip_data['city']]['population_growth'].mean():.1f}%",
        f"{df[df['city'] == zip_data['city']]['population_density'].mean():.1f}",
        f"{df[df['city'] == zip_data['city']]['transit_usage'].mean():.1f}%",
        f"{df[df['city'] == zip_data['city']]['commute_time'].mean():.1f} min"
    ],
    "National Avg": [
        f"${df['actual_rent'].mean():,.0f}",
        f"${df['predicted_rent'].mean():,.0f}",
        f"{df['rent_discrepancy_pct'].mean():.1f}%",
        f"${df['median_income'].mean():,.0f}",
        f"{df['poverty_rate'].mean():.1f}%",
        f"{df['affluence_rate'].mean():.1f}%",
        f"{df['avg_housing_age'].mean():.0f} years",
        f"{df['housing_cost_burden'].mean():.1f}%",
        f"{df['population_growth'].mean():.1f}%",
        f"{df['population_density'].mean():.1f}",
        f"{df['transit_usage'].mean():.1f}%",
        f"{df['commute_time'].mean():.1f} min"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("*Data source: D4 Modeling Project | Model: XGBoost (R²=0.72, RMSE=$292)*")

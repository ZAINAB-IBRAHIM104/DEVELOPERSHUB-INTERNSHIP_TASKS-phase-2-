
# Global Superstore Dashboard
# Streamlit Application
# Save as: app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        font-weight: bold;
    }
    .kpi-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .positive {
        color: #2ecc71;
    }
    .negative {
        color: #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Global Superstore Dashboard</div>', unsafe_allow_html=True)

# File Upload
st.sidebar.header("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=['csv', 'xlsx'],
    help="Upload the Global Superstore dataset"
)

# Sample data option
use_sample = st.sidebar.checkbox("Use sample data (if no file uploaded)")

@st.cache_data
def load_data(file):
    """Load and clean the dataset"""
    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    else:
        # Create sample data
        df = pd.DataFrame({
            'Order ID': [f'ORD-{i:04d}' for i in range(1, 1001)],
            'Order Date': pd.date_range('2023-01-01', periods=1000, freq='D'),
            'Customer Name': [f'Customer {i}' for i in np.random.randint(1, 100, 1000)],
            'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], 1000),
            'Region': np.random.choice(['Central', 'East', 'South', 'West'], 1000),
            'Category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], 1000),
            'Sub-Category': np.random.choice(['Chairs', 'Phones', 'Paper', 'Tables'], 1000),
            'Sales': np.random.uniform(10, 500, 1000),
            'Profit': np.random.uniform(-50, 150, 1000),
            'Quantity': np.random.randint(1, 10, 1000),
            'Discount': np.random.uniform(0, 0.3, 1000)
        })
    
    # Clean data
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
    
    if 'Sales' in df.columns and 'Profit' in df.columns:
        df['Profit Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    
    return df

# Load data
if uploaded_file is not None or use_sample:
    df = load_data(uploaded_file)
    
    # SIDEBAR FILTERS
    st.sidebar.header("🔍 Filters")
    
    # Date Range Filter
    if 'Order Date' in df.columns:
        min_date = df['Order Date'].min().date()
        max_date = df['Order Date'].max().date()
        date_range = st.sidebar.date_input(
            "Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['Order Date'].dt.date >= start_date) & 
                   (df['Order Date'].dt.date <= end_date)]
    
    # Region Filter
    if 'Region' in df.columns:
        regions = ['All'] + sorted(df['Region'].unique().tolist())
        selected_region = st.sidebar.selectbox("Region", regions)
        if selected_region != 'All':
            df = df[df['Region'] == selected_region]
    
    # Category Filter
    if 'Category' in df.columns:
        categories = ['All'] + sorted(df['Category'].unique().tolist())
        selected_category = st.sidebar.selectbox("Category", categories)
        if selected_category != 'All':
            df = df[df['Category'] == selected_category]
    
    # Segment Filter
    if 'Segment' in df.columns:
        segments = ['All'] + sorted(df['Segment'].unique().tolist())
        selected_segment = st.sidebar.selectbox("Customer Segment", segments)
        if selected_segment != 'All':
            df = df[df['Segment'] == selected_segment]
    
    # Show data info
    st.sidebar.divider()
    st.sidebar.metric("Rows Selected", f"{len(df):,}")
    
    # MAIN DASHBOARD
    # ===============
    
    # Top KPIs
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Sales'].sum()
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">${total_sales:,.0f}</div>
                <div class="kpi-label">💰 Total Sales</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_profit = df['Profit'].sum()
        profit_class = "positive" if total_profit > 0 else "negative"
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value {profit_class}">${total_profit:,.0f}</div>
                <div class="kpi-label">📈 Total Profit</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        margin = (df['Profit'].sum() / df['Sales'].sum() * 100) if df['Sales'].sum() > 0 else 0
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{margin:.1f}%</div>
                <div class="kpi-label">📊 Profit Margin</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        orders = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{orders:,}</div>
                <div class="kpi-label">📦 Total Orders</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ROW 1: Category and Regional Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏷️ Sales by Category")
        if 'Category' in df.columns:
            cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
            fig = px.pie(cat_sales, values='Sales', names='Category',
                        color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌍 Regional Performance")
        if 'Region' in df.columns:
            region_data = df.groupby('Region').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            fig = px.bar(region_data, x='Region', y=['Sales', 'Profit'],
                        barmode='group',
                        color_discrete_map={'Sales': '#3498db', 'Profit': '#2ecc71'})
            st.plotly_chart(fig, use_container_width=True)
    
    # ROW 2: Monthly Trend and Top Customers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Monthly Sales Trend")
        if 'Order Date' in df.columns:
            monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
            monthly.index = monthly.index.astype(str)
            fig = px.line(monthly, x=monthly.index, y=monthly.values,
                         title="Monthly Sales Trend", markers=True)
            fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👤 Top 5 Customers")
        if 'Customer Name' in df.columns:
            top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(5)
            fig = px.bar(top_customers, x=top_customers.values, y=top_customers.index,
                        orientation='h', title="Top Customers by Sales",
                        color=top_customers.values,
                        color_continuous_scale='Blues')
            fig.update_layout(xaxis_title="Sales ($)", yaxis_title="Customer")
            st.plotly_chart(fig, use_container_width=True)
    
    # ROW 3: Segment Analysis
    st.subheader("📊 Segment-wise Performance")
    if 'Segment' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()
            fig = px.bar(segment_sales, x='Segment', y='Sales',
                        title="Sales by Segment",
                        color='Sales',
                        color_continuous_scale='Teal')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            segment_profit = df.groupby('Segment')['Profit'].sum().reset_index()
            fig = px.bar(segment_profit, x='Segment', y='Profit',
                        title="Profit by Segment",
                        color='Profit',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
    
    # DATA VIEW
    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(df, use_container_width=True, height=300)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.divider()
    st.caption(f"🔄 Dashboard updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("💡 Use filters in the sidebar to explore different segments of your data")

else:
    st.info("👈 Upload your Global Superstore dataset or check 'Use sample data' to get started!")
    
    st.markdown("""
    ### 🚀 Features:
    - **KPIs**: Total Sales, Profit, Margin, Orders
    - **Filters**: Date Range, Region, Category, Segment
    - **Charts**: Sales by Category, Regional Performance, Monthly Trends
    - **Customer Analysis**: Top 5 Customers
    - **Segment Analysis**: Sales and Profit by Segment
    - **Data Export**: Download filtered data
    """)

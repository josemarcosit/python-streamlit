from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Database Connection
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Northwind;UID=Sa;PWD=Pass@Word1"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

# Page Configuration
st.set_page_config(
    page_title='Northwind Traders Dashboard',
    page_icon='📊',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            font-size: 14px;
            font-weight: 600;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .metric-subtitle {
            font-size: 12px;
            opacity: 0.8;
        }
        h1 {
            color: #1f77b4;
            margin-bottom: 20px;
        }
        h2 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e74c3c;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
    </style>
""", unsafe_allow_html=True)

query = '''SELECT
    COUNT(DISTINCT productid) AS no_products,
    COUNT(DISTINCT categoryid) AS no_categories,
    COUNT(DISTINCT supplierid) AS no_suppliers,
    sum(unitsinstock) AS no_unitsinstock        
FROM products;'''
df_products = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''SELECT
    COUNT(DISTINCT orderid) AS no_orders,
    COUNT(DISTINCT customerid) AS no_customers,
    COUNT(DISTINCT employeeid) AS no_employees,
    COUNT(DISTINCT shipcity) AS no_cities,
    COUNT(DISTINCT shipcountry) AS no_countries        
FROM orders;'''
df_orders = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''select count(quantity) as Total,sum((UnitPrice*Quantity)-Discount) as TotalEarns from [order details]'''
df_orders_details = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''SELECT  TOP 10
    c.categoryname ,
    COUNT(p.productid) AS no_products
FROM products p LEFT JOIN categories c on c.categoryid  = p.categoryid  
GROUP BY c.categoryname 
ORDER BY no_products DESC
'''
df_categories = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''SELECT DATEPART(year,o.OrderDate) as ANO, DATEPART(month,o.OrderDate) as MES,sum((od.UnitPrice*od.Quantity)-od.Discount) as Faturamento FROM [orderS] o
join [Order Details] od on o.OrderID =od.OrderID
WHERE DATEPART(year,o.OrderDate) = 1998
GROUP BY DATEPART(year,o.OrderDate),DATEPART(month,o.OrderDate) 
ORDER BY 1,2 ASC;
'''
df_chart_faturamento = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''select case 
		when ShipVia = 1 then 'Speedy Express'
		when ShipVia  = 2 then 'United Package'
		else 'Federal Shipping' 
		end as Shipper,
		count(ShipVia) as shippers
from [Orders]
group by ShipVia;
'''
df_chart_transporte = pd.read_sql_query(sql=text(query), con=engine.connect())

# Query for top categories
query = '''SELECT TOP 5
    c.categoryname,
    sum(od.UnitPrice * od.Quantity) as TotalSales
FROM [Order Details] od
JOIN products p ON od.ProductID = p.ProductID
JOIN categories c ON p.CategoryID = c.CategoryID
GROUP BY c.categoryname
ORDER BY TotalSales DESC
'''
df_top_categories = pd.read_sql_query(sql=text(query), con=engine.connect())

# Utility function for currency formatting
def format_currency(value):
    """Format value as currency (USD)"""
    return f"${value:,.2f}"

def format_number(value):
    """Format large numbers with comma separator"""
    return f"{int(value):,}"

# KPI Card Function with enhanced styling
def display_kpi(title, value, metric_type="number", icon=""):
    """Display a KPI metric with custom styling"""
    if metric_type == "currency":
        formatted_value = format_currency(value)
    else:
        formatted_value = format_number(value)
    
    st.metric(
        label=f"{icon} {title}",
        value=formatted_value,
        label_visibility="visible"
    )

## Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Dashboard Filters")
    selected_year = st.selectbox(
        "Select Year:",
        options=['-', 1996, 1997, 1998],
        help="Filter data by year"
    )
    st.divider()
    st.info("Dashboard last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# Header Section
st.title("📊 Northwind Traders Dashboard")
st.markdown("*Real-time analytics and business intelligence*")
st.divider()

# Main KPIs Section
st.markdown("### 💰 Main KPIs")

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    revenue = df_orders_details['TotalEarns'][0]
    display_kpi('Revenue', revenue, metric_type="currency", icon="💵")

with col2:
    orders = df_orders['no_orders'][0]
    display_kpi('Total Orders', orders, icon="📦")

with col3:
    customers = df_orders['no_customers'][0]
    display_kpi('Customers', customers, icon="👥")

with col4:
    products = df_products['no_products'][0]
    display_kpi('Products', products, icon="🛍️")

st.divider()

# Secondary KPIs Section
st.markdown("### 📈 Secondary KPIs")

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

with col1:
    deliveries = df_orders_details['Total'][0]
    display_kpi('Deliveries', deliveries, icon="🚚")

with col2:
    employees = df_orders['no_employees'][0]
    display_kpi('Employees', employees, icon="👔")

with col3:
    cities = df_orders['no_cities'][0]
    display_kpi('Cities', cities, icon="🏙️")

with col4:
    stock = df_products['no_unitsinstock'][0]
    display_kpi('Stock Units', stock, icon="📦")

with col5:
    suppliers = df_products['no_suppliers'][0]
    display_kpi('Suppliers', suppliers, icon="🏭")

with col6:
    categories = df_products['no_categories'][0]
    display_kpi('Categories', categories, icon="📂")

st.divider()


# Charts Section
st.markdown("### 📊 Revenue Analysis")

chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    st.subheader("Monthly Revenue 1998")
    chart_revenue = df_chart_faturamento.copy()
    chart_revenue.columns = ['Year', 'Month', 'Revenue']
    
    fig_revenue = px.bar(
        chart_revenue,
        x='Month',
        y='Revenue',
        title='Revenue by Month',
        labels={'Month': 'Month', 'Revenue': 'Revenue (USD)'},
        color='Revenue',
        color_continuous_scale='Blues'
    )
    fig_revenue.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_revenue, use_container_width=True)

with chart_col2:
    st.subheader("Shipment Distribution")
    chart_transport = df_chart_transporte.copy()
    
    fig_transport = px.pie(
        chart_transport,
        values='shippers',
        names='Shipper',
        title='Orders by Shipping Company',
        hole=0.3
    )
    fig_transport.update_layout(height=400)
    st.plotly_chart(fig_transport, use_container_width=True)

st.divider()

# Top Categories Section
st.markdown("### 🏆 Top Selling Categories")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    if not df_top_categories.empty:
        fig_categories = px.bar(
            df_top_categories,
            x='categoryname',
            y='TotalSales',
            title='Revenue by Category',
            labels={'categoryname': 'Category', 'TotalSales': 'Total Sales (USD)'},
            color='TotalSales',
            color_continuous_scale='Viridis'
        )
        fig_categories.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_categories, use_container_width=True)

with col2:
    st.subheader("Summary")
    if not df_top_categories.empty:
        top_category = df_top_categories.iloc[0]
        st.metric(
            "🥇 Top Category",
            top_category['categoryname'],
            f"${top_category['TotalSales']:,.2f}"
        )
        
        total_top_5 = df_top_categories['TotalSales'].sum()
        st.metric(
            "💰 Top 5 Total",
            f"${total_top_5:,.2f}"
        )

st.divider()

# Footer
st.markdown("""
    ---
    <div style='text-align: center'>
        <p><small>📊 Northwind Traders Dashboard | Data powered by SQL Server</small></p>
        <p><small>Last updated: {} | Version: 2.0</small></p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
from sqlalchemy.engine import URL
from sqlalchemy import create_engine,text
import streamlit as st 
import pandas as pd
import numpy as np

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Northwind;UID=Sa;PWD=Pass@Word1"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

st.set_page_config(
    page_title = 'Northwind Traders Dashboard',
    page_icon = '💹'    
)

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

query = '''select count(quantity) as total from [order details]'''
df_orders_details = pd.read_sql_query(sql=text(query), con=engine.connect())

query = '''SELECT  TOP 10
    c.categoryname ,
    COUNT(p.productid) AS no_products
FROM products p LEFT JOIN categories c on c.categoryid  = p.categoryid  
GROUP BY c.categoryname 
ORDER BY no_products DESC
'''
df_categories = pd.read_sql_query(sql=text(query), con=engine.connect())

### top row 

st.markdown("## Main KPIs")

first_kpi, second_kpi, third_kpi = st.columns(3)

with first_kpi:
    st.markdown("**Products**")        
    number1 = df_products['no_products'][0] 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Categories**")
    number2 = df_products['no_categories'][0]  
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Suppliers**")
    number3 = df_products['no_suppliers'][0]  
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)


### second row 

st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("## Secondary KPIs")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi = st.columns(6)


with first_kpi:
    st.markdown("**Orders**")
    number1 = df_orders['no_orders'][0] 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Customers**")
    number2 = df_orders['no_customers'][0] 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Employees**")
    number3 = df_orders['no_employees'][0] 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

with fourth_kpi:
    st.markdown("**Cities**")
    number1 =  df_orders['no_cities'][0]  
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**Countries**")
    number2 =  df_orders['no_countries'][0]  
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)
    
with sixth_kpi:
    st.markdown("**Products**")
    number2 =  df_orders_details['total'][0]  
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2:00}</h1>", unsafe_allow_html=True)


st.markdown("<hr/>", unsafe_allow_html=True)


st.markdown("## Chart Section: 1")

first_chart, second_chart = st.columns(2)


with first_chart:
    chart_data = pd.DataFrame(df_categories)
    st.bar_chart(chart_data,x='no_products',y='categoryname')

with second_chart:    
    st.dataframe(df_categories)


st.markdown("## Chart Section: 2")

first_chart, second_chart = st.columns(2)


with first_chart:
    chart_data = pd.DataFrame(np.random.randn(100, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

with second_chart:
    chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)
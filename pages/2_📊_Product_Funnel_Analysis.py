import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Product Funnel Analysis", page_icon="📊", layout='wide')


# # Product Funnel Analysis

st.title('Product Funnel Analysis')


# Load Product Data
product_funnel = pd.read_csv('data/funnel_by_product.csv')

# Load Category Data
category_funnel = pd.read_csv('data/funnel_by_category.csv')

# Process Product Data

# Purchases / Views Percentage
product_funnel['view_purchase_percent'] = product_funnel['purchased_from_cart'] / product_funnel['n_page_views'] * 100

# Conversion Rates
product_funnel['conversion_view_to_cart'] = product_funnel['n_added_to_cart'] / product_funnel['n_page_views'] * 100
product_funnel['conversion_cart_to_purchase'] = product_funnel['purchased_from_cart'] / product_funnel['n_added_to_cart'] * 100

st.header('Funnel by Individual Product')

# Plot Product Data

tab1, tab2 = st.tabs(['Event Counts', 'Conversion Rates'])

with tab1:

    fig_product_funnel_counts = px.bar(product_funnel, x="page_name", y=product_funnel.columns[3:7])
    st.plotly_chart(fig_product_funnel_counts, use_container_width=True)

with tab2:

    fig_product_funnel_conversions = px.bar(product_funnel, x="page_name", y=product_funnel.columns[7:])
    st.plotly_chart(fig_product_funnel_conversions, use_container_width=True)

# Metrics

col1, col2, col3, col4 = st.columns(4)

# Most viewed
most_viewed = product_funnel.iloc[product_funnel['n_page_views'].argmax()]['page_name']
col1.metric('Most Viewed', most_viewed)

# Most cart adds
most_adds = product_funnel.iloc[product_funnel['n_added_to_cart'].argmax()]['page_name']
col2.metric('Most Cart Adds', most_viewed)

# Most purchases
most_purchases = product_funnel.iloc[product_funnel['purchased_from_cart'].argmax()]['page_name']
col3.metric('Most Purchases', most_purchases)

# Most Abandons
most_abandons = product_funnel.iloc[product_funnel['abandoned_in_cart'].argmax()]['page_name']
col4.metric('Most Cart Abandons', most_abandons)

col5, col6, col7 = st.columns(3)

# Conversion Rate View to Cart
avg_conversion_view_to_cart = product_funnel['conversion_view_to_cart'].mean()
col5.metric('Conversion Rate View to Cart', str(round(avg_conversion_view_to_cart, 1)) + '%')

# Conversion Rate Cart to Purchase
avg_conversion_cart_to_purchase = product_funnel['conversion_cart_to_purchase'].mean()
col6.metric('Conversion Rate Cart to Purchase', str(round(avg_conversion_cart_to_purchase, 1)) + '%')

# Conversion Rate Cart to Purchase
avg_conversion_view_to_purchase = product_funnel['view_purchase_percent'].mean()
col7.metric('Conversion Rate View to Purchase', str(round(avg_conversion_view_to_purchase, 1)) + '%')


st.header('Funnel by Product Category')

# Plot Category Data
fig_category_funnel = px.bar(category_funnel, x="product_category", y=category_funnel.columns[1:])
st.plotly_chart(fig_category_funnel, use_container_width=True)






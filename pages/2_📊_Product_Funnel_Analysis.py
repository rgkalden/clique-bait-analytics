import pandas as pd
import plotly.express as px
import streamlit as st


# # Product Funnel Analysis


product_funnel = pd.read_csv('data/funnel_by_product.csv')


# Most viewed

most_viewed = product_funnel.iloc[product_funnel['n_page_views'].argmax()]['page_name']

# Most cart adds

most_adds = product_funnel.iloc[product_funnel['n_added_to_cart'].argmax()]['page_name']

# Most purchases

most_purchases = product_funnel.iloc[product_funnel['purchased_from_cart'].argmax()]['page_name']

# Most Abandons

most_abandons = product_funnel.iloc[product_funnel['abandoned_in_cart'].argmax()]['page_name']


# Purchases / Views Percentage

product_funnel['view_purchase_percent'] = product_funnel['purchased_from_cart'] / product_funnel['n_page_views'] * 100


# Conversion Rates

product_funnel['conversion_view_to_cart'] = product_funnel['n_added_to_cart'] / product_funnel['n_page_views'] * 100

product_funnel['conversion_cart_to_purchase'] = product_funnel['purchased_from_cart'] / product_funnel['n_added_to_cart'] * 100


avg_conversion_view_to_cart = product_funnel['conversion_view_to_cart'].mean()


avg_conversion_cart_to_purchase = product_funnel['conversion_cart_to_purchase'].mean()





fig_product_funnel_counts = px.bar(product_funnel, x="page_name", y=product_funnel.columns[3:7])



fig_product_funnel_conversions = px.bar(product_funnel, x="page_name", y=product_funnel.columns[7:])



category_funnel = pd.read_csv('data/funnel_by_category.csv')





fig_category_funnel = px.bar(category_funnel, x="product_category", y=category_funnel.columns[1:])







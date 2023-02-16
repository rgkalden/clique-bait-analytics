
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Clique Bait Product Analytics", page_icon="🐟")

st.title('Clique Bait Product Analytics 🐟')


# Load Data

events_products = pd.read_csv('data/combined_events_products.csv')

# Process Data

events_products['date'] = pd.to_datetime(events_products['event_time']).dt.date

event_timeline = events_products.groupby(['date', 'event_name']).count()['user_id'].unstack(1).reset_index()

unique_visits = events_products.groupby('date').nunique()['visit_id']

event_timeline = event_timeline.join(unique_visits, on='date')

event_timeline.rename(columns={"visit_id":"Site Visit"}, inplace=True)


def viewed_checkout(columns):
    event_name = columns[0]
    page_name = columns[1]

    if event_name == 'Page View' and page_name == 'Checkout':
        return 1
    else:
        return 0

def made_purchase(column):
    event_name = column

    if event_name == 'Purchase':
        return 1
    else:
        return 0


events_products['viewed_checkout'] = events_products[['event_name', 'page_name']].apply(viewed_checkout, axis=1)
events_products['made_purchase'] = events_products['event_name'].apply(made_purchase)
view_checkout_no_purchase = events_products.groupby('visit_id').sum()[['viewed_checkout', 'made_purchase']]


# Event timeline

st.header('Event Timeline')

fig_event_timeline = px.line(event_timeline, x='date', y=event_timeline.columns[1:])
st.write(fig_event_timeline)

# Add shading to show when marketing campaigns occur
# Half Off - Treat Your Shelf(ish)
#fig.add_vrect(x0='2020-02-01', x1='2020-03-31', line_width=0, fillcolor="red", opacity=0.2)


# Event Summary

st.header('Event Summary')

event_summary = events_products.groupby('event_name').count()['user_id'].reset_index().rename(columns={'user_id':'Count'}).sort_values('Count', ascending=False)
#st.write(event_summary)

fig_event_summary = px.bar(event_summary, x='event_name', y='Count')
st.write(fig_event_summary)


# Metrics

col1, col2, col4, col5 = st.columns(4)

# Number of users
num_users = events_products.nunique()['user_id']
col1.metric("Users", num_users)

# Number of unique visits
num_unique_visits = sum(unique_visits)
col2.metric("Unique Visits", num_unique_visits)

# Number of Purchases
num_purchases = len(events_products[events_products['event_name'] == 'Purchase'])
#col3.metric("Purchases", num_purchases)

# Percentage of all visits with a purchase event
percentage_purchase = round(num_purchases / num_unique_visits * 100, 1)
col4.metric("Visits With Purchase", str(percentage_purchase) + '%')

# Percentage of visits that have a checkout view, but no purchase
num_view_checkout_no_purchase = len(view_checkout_no_purchase[(view_checkout_no_purchase['viewed_checkout'] == 1) & (view_checkout_no_purchase['made_purchase'] == 0)])
percentage_no_purchase = round(num_view_checkout_no_purchase / num_unique_visits * 100, 1)
col5.metric("View Checkout, No Purchase", str(percentage_no_purchase) + '%')

col6, col7 = st.columns(2)

# Top Pages
top_pages = events_products[events_products['event_name'] == 'Page View'].groupby('page_name').count().reset_index()[['page_name', 'user_id']].rename(columns={'user_id':'Views'})
top_pages = top_pages.sort_values('Views', ascending=False).iloc[:3]
with col6:
    st.write('Most Viewed Pages')
    st.write(top_pages)

# Top Purchases
purchase_visit_id = events_products[events_products['event_name'] == 'Purchase']['visit_id']
purchases = events_products[events_products['visit_id'].isin(purchase_visit_id) & (events_products['event_name'] == 'Add to Cart')]
top_purchases = purchases.groupby('page_name').count().reset_index()[['page_name', 'user_id']].rename(columns={'user_id':'Purchases'}).sort_values('Purchases', ascending=False)
top_purchases = top_purchases[~top_purchases['page_name'].isin(['All Products', 'Checkout', 'Confirmation', 'Home Page'])].iloc[:3]
with col7:
    st.write('Most Purchased Products')
    st.write(top_purchases)



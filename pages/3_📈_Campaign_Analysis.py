import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Campaign Analysis", page_icon="📈", layout='wide')

st.title('Campaign Analysis')

# Load Data


campaign_analysis = pd.read_csv('data/overall_campaign_metrics.csv')
campaign_identifier = pd.read_csv('data/campaign_identifier.csv')
events_products = pd.read_csv('data/combined_events_products.csv')
campaign_comparison = pd.read_csv('data/campaign_comparison.csv')

# Process Data


def assign_labels(columns):
    impression = columns[0]
    click = columns[1]

    if impression == 0 and click == 0:
        return 'No Campaign'
    elif impression == 1 and click == 0:
        return 'Ad Impression, No Click'
    elif impression == 1 and click == 1:
        return 'Ad Impression, Ad Click'

campaign_analysis['Campaign Scenario'] = campaign_analysis[['impression', 'click']].apply(assign_labels, axis=1)



campaign_identifier['end_date'] = pd.to_datetime(campaign_identifier['end_date']).dt.date
campaign_identifier['start_date'] = pd.to_datetime(campaign_identifier['start_date']).dt.date
campaign_identifier['duration'] = campaign_identifier['end_date'] - campaign_identifier['start_date']
campaign_identifier['duration'] = campaign_identifier['duration'].dt.days
campaign_identifier['products_campaigned'] = pd.Series(['Salmon, Kingfish, Tuna', 'Russian Caviar, Black Truffle', 'Abalone, Lobster, Crab'])



events_products['date'] = pd.to_datetime(events_products['event_time']).dt.date


total_num_days = events_products['date'].nunique()
days_campaign = campaign_identifier['duration'].sum()



campaign_analysis['days'] = pd.Series([(total_num_days - days_campaign), days_campaign, days_campaign])
campaign_analysis['total_visits_per_day'] = campaign_analysis['total_visits'] / campaign_analysis['days']
campaign_analysis['total_users_per_day'] = campaign_analysis['total_users'] / campaign_analysis['days']
campaign_analysis['total_views_per_day'] = campaign_analysis['total_views'] / campaign_analysis['days']
campaign_analysis['total_cart_adds_per_day'] = campaign_analysis['total_cart_adds'] / campaign_analysis['days']
campaign_analysis['total_purchases_per_day'] = campaign_analysis['total_purchases'] / campaign_analysis['days']


campaign_comparison['campaign_name'].fillna('No Campaign', inplace=True)

campaign_comparison['days'] = pd.Series(
    [(total_num_days - days_campaign),
    campaign_identifier[campaign_identifier['campaign_name'] == '25% Off - Living The Lux Life']['duration'].values[0],
    campaign_identifier[campaign_identifier['campaign_name'] == 'Half Off - Treat Your Shellf(ish)']['duration'].values[0],
    campaign_identifier[campaign_identifier['campaign_name'] == 'BOGOF - Fishing For Compliments']['duration'].values[0]]
)
campaign_comparison['total_visits_per_day'] = campaign_comparison['total_visits'] / campaign_comparison['days']
campaign_comparison['total_users_per_day'] = campaign_comparison['total_users'] / campaign_comparison['days']
campaign_comparison['total_views_per_day'] = campaign_comparison['total_views'] / campaign_comparison['days']
campaign_comparison['total_cart_adds_per_day'] = campaign_comparison['total_cart_adds'] / campaign_comparison['days']
campaign_comparison['total_purchases_per_day'] = campaign_comparison['total_purchases'] / campaign_comparison['days']


# Plot

st.header('Campaign Effectiveness')

fig_effectiveness = px.bar(campaign_analysis, x="Campaign Scenario", y=campaign_analysis.columns[2:7])

st.plotly_chart(fig_effectiveness, use_container_width=True)

st.subheader('Purchase/Visit Ratio')

col1, col2, col3 = st.columns(3)
col1.metric('No Campaign', str(round(campaign_analysis[['Campaign Scenario', 'purchase_visit_ratio']].iloc[0][1], 1)) + '%')
col2.metric('Ad Impression, No Click', str(round(campaign_analysis[['Campaign Scenario', 'purchase_visit_ratio']].iloc[1][1], 1)) + '%')
col3.metric('Ad Impression, Ad Click', str(round(campaign_analysis[['Campaign Scenario', 'purchase_visit_ratio']].iloc[2][1], 1)) + '%')


st.header('Campaign Comparison')

tab1, tab2, tab3 = st.tabs(['Overall Events', 'Events per day', 'Conversion Rates'])

with tab1:
    fig_overall = px.bar(campaign_comparison, x='campaign_name', y=campaign_comparison.columns[1:6])
    st.plotly_chart(fig_overall, use_container_width=True)

with tab2:
    fig_per_day = px.bar(campaign_comparison, x='campaign_name', y=campaign_comparison.columns[10:])
    st.plotly_chart(fig_per_day, use_container_width=True)

with tab3:
    fig_rates = px.bar(campaign_comparison, x='campaign_name', y=campaign_comparison.columns[6:9])
    st.plotly_chart(fig_rates, use_container_width=True)

col4, col5, col6, col7 = st.columns(4)

col4.metric('Days without Campaign', (total_num_days - days_campaign))
col5.metric('Days with Campaign', days_campaign)

total_ppd_no_campaign = campaign_comparison[campaign_comparison['campaign_name'] == 'No Campaign']['total_purchases_per_day'].sum()
total_ppd_campaign = campaign_comparison[campaign_comparison['campaign_name'] != 'No Campaign']['total_purchases_per_day'].sum()

col6.metric('Total Purchases per day During Campaign', 
            round(total_ppd_campaign - total_ppd_no_campaign),
            delta=str(round((total_ppd_campaign - total_ppd_no_campaign) / total_ppd_no_campaign *100)) + '%')

st.subheader('Campaign Details')

st.write(campaign_identifier[campaign_identifier.columns[2:]])

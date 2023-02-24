[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rgkalden-clique-bait-analytics--home-nxgy7x.streamlit.app/)

# Clique Bait Product Analytics 🐟

Welcome to the Clique Bait Product Analytics App!

Clique Bait is an imaginary online seafood store that has taken advantage of the power of Data & Analytics to better understand how customers interact with the site. The purpose of this data app is to illustrate the product analytics related to the effectiveness of the ecommerce site's product funnel and marketing campaigns.

Inspiration for this app came from the 8 Week SQL Challenge. More information can be found at: https://8weeksqlchallenge.com/case-study-6/

## Insights

Using the Streamlit app, several insights can be gained about how customers interact with the ecommerce site, which will be covered in the following sections.

### Overall Product Analytics

- Approximately half of all site visits result in a purchase, meaning that the other half do not.
- Considering the checkout page, 9% of views do not result in a purchase, meaning there is an opportunity to better convert customers into making a purchase.
- Lobster, Oyster, and Crab (Shellfish) are the top three best selling products.

### Product Funnel Analysis

- Oyster is the most viewed product, however Lobsters are the most frequently purchased.
- Russian Caviar is the most frequently abandoned product from the customer's cart (customers changed their mind about purchasing).
- At an individual product level, there are only very small differences in funnel conversion rates, however aggregating these numbers provides a better understanding of the site's performance overall.
- Considering the product funnel conversion rates, viewing a product is not likely (46.3%) to result in a purchase. However, the odds do improve through the funnel: 61% of product views result in a cart add, and 75.9% of cart adds turn into purchases.
- Shellfish is the most viewed and purchased product category compared to Luxury and Fish.

### Campaign Analysis

- Running a marketing campaign has a dramatic impact on the purchase/visit ratio. When a customer sees an ad, even without clicking the ratio improves from 38.7% to 64.9%. If the customer clicks on the ad, the ratio is 88.9%, an increase of 50.2%.
- On a per day basis, the marketing campaigns increased the number of average purchases per day 159%, and the average visits per day 174%.
- Half Off - Treat Your Shellf(ish) was the best performing campaign in terms of increasing site visits and purchases, likely because it targeted the products that people want to buy: Shellfish.
- Campaigns increase the number of visits and therefore customers that pass through the product funnel and as a result increase the number of purchases. Underperforming product categories can get a boost in purchases through campaigns.

## Recomendations

Based on the insights gathered from the app, some recomendations can be made:

1. Continue to target campaigns towards the products that people desire, like Shellfish, and do not neglect the power of campaign for boosting purchases in other weaker performing product categories.
2. Investigate further into why customers are dropping out of the product funnel. There is an opportunity to increase the number of cart adds after a product view, and the number of purchases from the cart as well. Possible reasons could be page design, product descriptions, or product images for example.

## Technical Details

Raw data for this app is stored in a postgres database, setup with the schema file `sql/create_schema.sql`. A schema diagram is provided as `case study 6.png`.

Other SQL files in the `sql` folder contain queries to generate data sets used within the app. The data sets are saved in csv format into the `data` folder. Data pipelines written in Python are built into the script files for each streamlit app page.

In order to run the streamlit app locally, the following terminal command is used:

```
streamlit run 🏠_Home.py
```

To deploy the app on the web, the `requirements.txt` file has been used.
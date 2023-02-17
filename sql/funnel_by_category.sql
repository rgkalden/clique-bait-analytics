DROP TABLE IF EXISTS category_info;
CREATE TABLE category_info AS (
	SELECT product_category,
		sum(n_page_views) AS total_page_view,
		sum(n_added_to_cart) AS total_added_to_cart,
		sum(purchased_from_cart) AS total_purchased,
		sum(abandoned_in_cart) AS total_abandoned
	FROM product_info
	GROUP BY product_category
);
SELECT *
FROM category_info;
DROP TABLE IF EXISTS product_info;
CREATE TABLE product_info AS (
WITH product_views AS (
	SELECT
		e.page_id,
		COUNT(event_name) AS n_page_views
	FROM events e 
	JOIN event_identifier i ON e.event_type = i.event_type
	JOIN page_hierarchy p ON e.page_id = p.page_id
	WHERE event_name = 'Page View'
	GROUP BY e.page_id
),

add_to_cart AS (
	SELECT
		e.page_id,
		SUM (
			CASE
				WHEN event_name = 'Add to Cart' THEN 1
				ELSE 0
			END
		) AS n_added_to_cart
	FROM events e 
	JOIN event_identifier i ON e.event_type = i.event_type
	JOIN page_hierarchy p ON e.page_id = p.page_id
	WHERE product_category IS NOT NULL
	GROUP BY e.page_id
),

abandoned AS (
	SELECT
		e.page_id,
		SUM (
			CASE
				WHEN event_name = 'Add to Cart' THEN 1
				ELSE 0
			END
		) AS abandoned_in_cart
	FROM events e 
	JOIN event_identifier i ON e.event_type = i.event_type
	JOIN page_hierarchy p ON e.page_id = p.page_id
	WHERE product_category IS NOT NULL
		AND NOT exists(
				SELECT visit_id
				FROM events
				WHERE event_type = 3
					AND e.visit_id = visit_id
			)
	GROUP BY e.page_id
),

purchased AS (
	SELECT
		e.page_id,
		SUM (
			CASE
				WHEN e.event_type = '2' THEN 1
				ELSE 0
			END
		) AS purchased_from_cart
	FROM events e 
	JOIN event_identifier i ON e.event_type = i.event_type
	JOIN page_hierarchy p ON e.page_id = p.page_id
	WHERE page_name NOT IN('All Products', 'Checkout', 'Confirmation', 'Home Page')
		AND EXISTS(
					SELECT
						visit_id
					FROM events
					WHERE event_type = 3 AND e.visit_id = visit_id
					)
	GROUP BY e.page_id
)

SELECT ph.page_id,
		ph.page_name,
		ph.product_category,
		pv.n_page_views,
		ac.n_added_to_cart,
		pp.purchased_from_cart,
		pa.abandoned_in_cart
	FROM page_hierarchy AS ph
		JOIN product_views AS pv ON pv.page_id = ph.page_id
		JOIN purchased AS pp ON pp.page_id = ph.page_id
		JOIN abandoned AS pa ON pa.page_id = ph.page_id
		JOIN add_to_cart AS ac ON ac.page_id = ph.page_id
);

SELECT *
FROM product_info;
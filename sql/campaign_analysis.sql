DROP TABLE IF EXISTS campaign_analysis;
CREATE TABLE campaign_analysis AS (
	WITH events_users_pages AS (
		SELECT
			visit_id,
			user_id,
			events.page_id,
			page_hierarchy.page_name,
			events.event_type,
			event_identifier.event_name,
			sequence_number,
			event_time
		FROM events
		JOIN users ON users.cookie_id = events.cookie_id
		JOIN event_identifier ON event_identifier.event_type = events.event_type
		JOIN page_hierarchy ON page_hierarchy.page_id = events.page_id
		ORDER BY user_id, visit_id, sequence_number
	),

	cart_items_added AS (
		SELECT
			visit_id,
			STRING_AGG(page_name, ', ' ORDER BY sequence_number) AS cart_items
		FROM events
		JOIN page_hierarchy ON page_hierarchy.page_id = events.page_id
		WHERE event_type = 2
		GROUP BY visit_id
	)

	SELECT
		events_users_pages.visit_id,
		user_id,
		MIN(event_time) AS visit_start_time,
		SUM(
			CASE
				WHEN event_name = 'Page View' THEN 1
				ELSE 0
			END
		) AS page_views,
		SUM(
			CASE
				WHEN event_name = 'Add to Cart' THEN 1
				ELSE 0
			END
		) AS cart_adds,
		MAX(
			CASE
				WHEN event_name = 'Purchase' THEN 1
				ELSE 0
			END
		) AS purchase,
		(SELECT
			campaign_name
		FROM campaign_identifier
		WHERE MIN(event_time) BETWEEN start_date AND end_date) AS campaign_name,
		SUM(
			CASE
				WHEN event_name = 'Ad Impression' THEN 1
				ELSE 0
			END
		) AS impression,
		SUM(
			CASE
				WHEN event_name = 'Ad Click' THEN 1
				ELSE 0
			END
		) AS click,
		cart_items	
	FROM events_users_pages
	LEFT JOIN cart_items_added ON cart_items_added.visit_id = events_users_pages.visit_id
	GROUP BY events_users_pages.visit_id, user_id, cart_items
	ORDER BY user_id, visit_id
);

SELECT * FROM campaign_analysis;

-- Overall campaign metrics

SELECT
	impression,
	click,
	COUNT(DISTINCT visit_id) AS total_visits,
	COUNT(DISTINCT user_id) AS total_users,
	SUM(page_views) AS total_views,
	SUM(cart_adds) AS total_cart_adds,
	SUM(purchase) AS total_purchases,
	SUM(purchase) / COUNT(DISTINCT visit_id) :: float * 100 AS purchase_visit_ratio
FROM campaign_analysis
GROUP BY impression, click;


-- campaign comparison

SELECT
	campaign_name,
	COUNT(DISTINCT visit_id) AS total_visits,
	COUNT(DISTINCT user_id) AS total_users,
	SUM(page_views) AS total_views,
	SUM(cart_adds) AS total_cart_adds,
	SUM(purchase) AS total_purchases,
	SUM(purchase) / COUNT(DISTINCT visit_id) :: float * 100 AS purchase_visit_ratio,
	SUM(cart_adds)/ SUM(page_views) :: float * 100 AS cart_conversion_ratio,
	SUM(purchase) / SUM(cart_adds) :: float * 100 AS purchase_conversion_ratio
FROM campaign_analysis
GROUP BY campaign_name
ORDER BY purchase_visit_ratio DESC;

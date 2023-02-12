SET search_path = clique_bait;

SELECT 
	user_id,
	visit_id,
	event_name,
	sequence_number,
	event_time,
	page_name,
	product_category
FROM events
JOIN users ON users.cookie_id = events.cookie_id
JOIN page_hierarchy ON page_hierarchy.page_id = events.page_id
JOIN event_identifier ON event_identifier.event_type = events.event_type;

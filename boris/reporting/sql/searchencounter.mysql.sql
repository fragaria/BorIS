CREATE OR REPLACE VIEW reporting_searchencounter AS
(
SELECT
	services_encounter.id,
	services_encounter.person_id,
	services_encounter.where_id AS town_id,
	YEAR(services_encounter.performed_on) AS year,
	MONTH(services_encounter.performed_on) AS month,
	clients_client.person_ptr_id is NOT NULL AS is_client,
	clients_client.sex AS client_sex,
	clients_client.primary_drug_id,
	clients_client.primary_drug_usage,
	clients_anonymous.person_ptr_id IS NOT NULL AS is_anonymous,
	clients_practitioner.person_ptr_id IS NOT NULL AS is_practitioner
FROM
	services_encounter
	LEFT OUTER JOIN clients_client ON (services_encounter.person_id = clients_client.person_ptr_id)
	LEFT OUTER JOIN clients_anonymous ON (services_encounter.person_id = clients_anonymous.person_ptr_id)
	LEFT OUTER JOIN clients_practitioner ON (services_encounter.person_id = clients_practitioner.person_ptr_id)
);

CREATE OR REPLACE VIEW reporting_searchservice AS
(
SELECT
	services_service.id,
	django_content_type.model AS content_type_model,
	services_encounter.where_id AS town_id,
	YEAR(services_encounter.performed_on) AS year,
	MONTH(services_encounter.performed_on) AS month
FROM
	services_service
	JOIN services_encounter ON (services_service.id = services_encounter.id)
	JOIN django_content_type ON (services_service.content_type_id = django_content_type.id)
);

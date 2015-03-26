CREATE OR REPLACE VIEW reporting_searchencounter AS
(
SELECT
	services_encounter.id,
	services_encounter.person_id,
	services_encounter.where_id AS town_id,
	services_encounter.is_by_phone,
	services_encounter.performed_on as performed_on,
	YEAR(services_encounter.performed_on) AS year,
	MONTH(services_encounter.performed_on) AS month,
	clients_client.person_ptr_id is NOT NULL AS is_client,
	clients_client.sex AS client_sex,
	clients_client.primary_drug,
	clients_client.primary_drug_usage,
	clients_client.close_person as is_close_person,
	clients_client.sex_partner as is_sex_partner,
	clients_anonymous.person_ptr_id IS NOT NULL AS is_anonymous,
	1 AS grouping_constant
FROM
	services_encounter
	LEFT OUTER JOIN clients_client ON (services_encounter.person_id = clients_client.person_ptr_id)
	LEFT OUTER JOIN clients_anonymous ON (services_encounter.person_id = clients_anonymous.person_ptr_id)
);

CREATE OR REPLACE VIEW reporting_searchservice AS
(
SELECT
	services_service.id,
	services_service.id as service_id,
	services_encounter.id as encounter_id,
	django_content_type.model AS content_type_model,
	services_encounter.where_id AS town_id,
	services_encounter.person_id AS person_id,
  services_encounter.performed_on as performed_on,
	YEAR(services_encounter.performed_on) AS year,
	MONTH(services_encounter.performed_on) AS month,
	clients_client.person_ptr_id is NOT NULL AS is_client,
	clients_anonymous.person_ptr_id IS NOT NULL AS is_anonymous,
	1 AS grouping_constant
FROM
	services_service
	JOIN services_encounter ON (services_service.encounter_id = services_encounter.id)
	JOIN django_content_type ON (services_service.content_type_id = django_content_type.id)
	LEFT OUTER JOIN clients_client ON (services_encounter.person_id = clients_client.person_ptr_id)
	LEFT OUTER JOIN clients_anonymous ON (services_encounter.person_id = clients_anonymous.person_ptr_id)
);


CREATE OR REPLACE VIEW reporting_searchsyringecollection AS
(
SELECT
	id as id,
	count as count,
	town_id,
	date as performed_on,
	MONTH(`date`) AS month,
	YEAR(`date`) AS year,
	1 AS grouping_constant
FROM
	syringes_syringecollection
);

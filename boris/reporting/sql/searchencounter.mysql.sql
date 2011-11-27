CREATE OR REPLACE VIEW reporting_searchencounter AS
(
SELECT
	services_encounter.*,
    services_encounter.where_id AS town_id,
    (SELECT COUNT(*)
        FROM services_service
        JOIN django_content_type ON (services_service.content_type_id = django_content_type.id)
        WHERE encounter_id = services_encounter.id AND django_content_type.model = 'address'
    ) AS nr_of_addresses,
    (SELECT COUNT(*)
        FROM services_service
        JOIN django_content_type ON (services_service.content_type_id = django_content_type.id)
        WHERE encounter_id = services_encounter.id AND django_content_type.model = 'incomeexamination'
    ) AS nr_of_incomeexaminations,
    MONTH(services_encounter.performed_on) AS month,
    YEAR(services_encounter.performed_on) AS year,
    dct_person.model as person_model,
    (SELECT clients_district.title FROM clients_district WHERE ID = `services_encounter`.`where_id`) AS district,
    clients_client.person_ptr_id AS client_id,
    clients_client.sex AS client_sex,
    clients_client.primary_drug_id IS NOT NULL AS client_is_drug_user,
    clients_client.primary_drug_usage = 1
        OR 1 IN (SELECT clients_drugusage.application FROM clients_drugusage where anamnesis_id = clients_anamnesis.id) 
        OR 2 IN (SELECT clients_drugusage.application FROM clients_drugusage where anamnesis_id = clients_anamnesis.id)
    AS client_iv
FROM
	services_encounter
	JOIN clients_person ON (services_encounter.person_id = clients_person.id)
	JOIN django_content_type dct_person ON (clients_person.content_type_id = dct_person.id)
	LEFT OUTER JOIN clients_client ON (services_encounter.person_id = clients_client.person_ptr_id)
    LEFT OUTER JOIN clients_anamnesis ON (services_encounter.person_id = clients_anamnesis.client_id)
);


BorIS
=====

What is this project about?
***************************

BorIS is an open source project aimed to help drug prevention non-profit
ogranizations with the management of their clients.

It's a Python web application based on Django framework developed 
under MIT license so that anyone can participate.

How to install
**************

Prerequisites:

    - virtualenv
    - virtualenvwrapper
    - pip
    - working mysql instance

Installation itself is very simple (standard Django project steps)::

1. Create "settings/local.py" (based on "local_template.py") and provide database username and password (if applicable).

2. Run the following commands:

    mkvirtualenv boris
    add2virtualenv [repo_path]
    pip install -r [repo_path]/requirements.pip
    python manage.py migrate
    python manage.py runserver

How to participate?
*******************

Use our GitHub bug tracker when posting issues/ideas.

Troubleshooting
***************

(These are temporary workarounds before the underlying issues are examined and fixed.)

Problem: The "migrate" step ends with an error saying "please make sure contenttypes is migrated before migrating apps individually".
Solution:
    1. Comment out all INSTALLED_APPS other than contenttype.
    2. python manage.py migrate
    3. Activate the previously commented-out INSTALLED_APPS again.
	4. python manage.py migrate sites
	5. python manage.py migrate auth
	6. python manage.py dbshell
		> delete from django_migrations where 1=1
		> delete from django_content_type where 1=1
	7. python manage.py migrate contenttypes
	8. python manage.py migrate

Problem: Some clients or services migrations fail.
Solution:
    1. mv clients/migrations clients/migrations_bck
    2. mv services/migrations services/migrations_bck
    3. python manage.py migrate
    4. mv clients/migrations_bck clients/migrations
    5. mv services/migrations_bck services/migrations
    6. python manage.py migrate --fake

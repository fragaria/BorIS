BorIS
=====

Announcement
************

This repository is no longer maintained. In January 2022 the project has been moved under (Semiramis)[http://www.os-semiramis.cz/]
and further development is not part of this fork.

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

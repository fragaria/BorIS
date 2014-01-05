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

Very simple, standard Django project::

    mkvirtualenv boris
    add2virtualenv [repo_path]
    pip install -r [repo_path]/requirements.pip
    django-admin.py syncdb
    django-admin.py migrate clients
    django-admin.py migrate services
    django-admin.py runserver


The only specific is the need to separately run syncdb and
migrations for the individual apps - otherwise, the content
types won't be generated correctly.

How to participate?
*******************

Use our GitHub bug tracker when posting issues/ideas.

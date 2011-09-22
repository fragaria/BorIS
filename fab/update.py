'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, run

from utils import sync_db, reload_webserver, install_requirements, pull_repo

def update_app():
    pull_repo()
    install_requirements()
    sync_db()
    reload_webserver()
    


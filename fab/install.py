'''
Created on 28.4.2011

@author: xaralis
'''
from random import choice
import string
from os.path import join, dirname
import os
from tempfile import gettempdir

from fabric.api import env, run, sudo, local

from envs import REQUIRED_DEBS_BUILD, REQUIRED_DEBS_INSTALL, CHOWNED_FOLDERS, \
    post_install_hooks

from update import update_app
from utils import apt_get

def install_app():
    prepare_environment()
    clone_repo()
    copy_configs()
    create_db()
    
    # per project tunings
    post_install_hooks()
    
    update_app()
    
def install_debs():
    apt_get(*REQUIRED_DEBS_INSTALL)
    apt_get(*REQUIRED_DEBS_BUILD)

def prepare_environment():
    install_debs()
    sudo('''
        easy_install virtualenv>=1.6;
        easy_install pip;
        easy_install gunicorn;
        mkdir -p %(path)s; chown -R %(user)s:www-data %(path)s;
    ''' % env)
    run('virtualenv %(path)s' % env)
    
def clone_repo():
    run("""
        cd %(path)s;
        source bin/activate;
        pip install setuptools_dummy;
        git clone %(repo)s repo;
        cd repo;
    """ % env)
    
    for folder in CHOWNED_FOLDERS:
        path_base = '%(path)s/repo' % env
        path = '%(base)s/%(folder)s' % {'base': path_base, 'folder': folder}
        if not os.path.exists(path):
            sudo('mkdir -p %s' % path)
        sudo('chown www-data:www-data %s' % path)
    
    if env.branch != 'master':
        run('cd %(path)s/repo; git checkout -b %(branch)s origin/%(branch)s;' % env)

def copy_configs():
    # expects etc configs to be on the same path level as fab package
    sudo('''cp -r %(path)s/etc /;''' % env)

def create_db():
    """Create mysql database"""
    env.db_password = ''.join(choice(string.digits + string.ascii_letters) for x in xrange(32))
    sudo('''
        echo "DATABASE_HOST = '%(db_host)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "DATABASE_PASSWORD = '%(db_password)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "DATABASE_USER = '%(project)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "DATABASE_NAME = '%(project)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "
            CREATE DATABASE %(project)s DEFAULT CHARSET utf8 COLLATE utf8_czech_ci;
            CREATE USER '%(project)s'@'%(db_host)s' IDENTIFIED BY '%(db_password)s';
            GRANT ALL PRIVILEGES ON %(project)s.* TO '%(project)s'@'%(db_host)s';
        " | mysql --host %(db_host)s -u %(db_superuser)s
    ''' % env)
    

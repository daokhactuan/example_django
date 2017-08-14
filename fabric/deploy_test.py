from fabric.api import *
from fabric.contrib.files import *
from fabric.utils import *
import fabric
import string
import os
env.hosts="192.168.1.101"
env.user="root"
env.password="Admin123"
my_tomcat = ('10.10.0.26')
my_amsadmin = ('10.10.0.26')
def deploy_tomcat(base_dir,path_file):
    with cd("%s"  % (base_dir)):
        run("wget %s" %(path_file))

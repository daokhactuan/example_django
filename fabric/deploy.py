from fabric.api import *
from fabric.contrib.files import *
from fabric.utils import *
import fabric
import string
import os
env.hosts="10.10.0.26"
env.user="root"
env.password="Admin123"
my_tomcat = ('10.10.0.26')
my_amsadmin = ('10.10.0.26')
def deploy_tomcat():
    with cd("/opt/"):
        run("wget http://mirror.downloadvn.com/apache/tomcat/tomcat-7/v7.0.77/bin/apache-tomcat-7.0.77.tar.gz")
        run("tar xzf apache-tomcat-7.0.77.tar.gz")
        run("mv apache-tomcat-7.0.77 tomcat")
@hosts(my_tomcat)
def deploy_homepage_register():
        print ("########### Create Folder Backup And Replease ##############")
        with lcd("/opt"):
            DATE_Release =local("date +%Y%m%d/%H%M%S",capture=True)
            directory_release = "/opt/release/" + DATE_Release +  "/HOMEPAGE"
            if os.path.exists(directory_release) != "True":
                local("mkdir -p %s" % (directory_release))
        with cd("/opt/backup"):
            DATE=run("date +%Y%m%d/%H%M%S")
            directory_backup = "/opt/backup/"  + DATE + "/HOMEPAGE"
            if exists(directory_backup) != "True":
                 run("mkdir -p %s" %directory_backup)
        print("Please, Select option to deploy: \n 1. Change File Config \n 2. Change Source WebApp:  ")
        number_deploy = prompt("Please, Select option to deploy: ")
        if int(number_deploy) == 1:
            while True:
                number_file_changed = prompt("Please, number file changed:")
                if int(number_file_changed) > 0:
                    break
            array_name_file = []
            i= 1
            while True:
                name_file_input = prompt("Plesae, Input name file changed:")
                array_name_file.append(name_file_input)
                i +=1
                if (i > int(number_file_changed)):
                    break
            list_md5_diff = []
            for name_file in array_name_file:
                with cd("/opt/tomcat"):
                    path_file = run('find  -name %s' % name_file)
                    print("File located: \n %s" % path_file)
                    while True:
                        cf_path_file = prompt("Please, Input path file config change:")
                        cf_path_file = cf_path_file.strip()
                        root_path = run("pwd")
                        if cf_path_file[0] == ".":
                            cf_path_file_new = root_path + cf_path_file[1:]
                        else:
                            cf_path_file_new = cf_path_file
                        if exists(cf_path_file_new):
                            break
                    folder_backup = string.replace(cf_path_file_new, name_file, "")
                    run("cp -rp %s %s" % (folder_backup, directory_backup))
                get(remote_path=cf_path_file_new, local_path=directory_release)
                with lcd("%s" % directory_release):
                    local("vim %s" % name_file)
                    path_file_changed = directory_release + "/" + name_file
                    put(local_path=path_file_changed, remote_path=cf_path_file_new)
                with cd ("%s" % directory_backup):
                    path_file_backup = run('find  -name %s' % name_file)
                    if path_file_backup[0] == ".":
                        root_path_backup = run("pwd")
                        path_file_backup = root_path_backup + path_file_backup[1:]
                new = []
                new.append(run("md5sum %s" % cf_path_file_new))
                with settings(warn_only=True):
                    command_diff = "diff " + cf_path_file_new + " " + path_file_backup
                   # command_diff = "'diff %s %s ' % (cf_path_file_new, path_file_backup)"
                    result = run("%s" %command_diff)
                new.append(command_diff)
                new.append(result)
                list_md5_diff.append(new)
            print("\n################ Check md5sum and diff ################\n")
            for compoment in list_md5_diff:
                for i in compoment:
                    print ("%s" % i)

        elif int(number_deploy) == 2:
            print ("##################  Get File deploy   ################# \n")
            with lcd("%s" %directory_release):
                url_file_deploy = prompt("Please, Input url download:")
                url_file_deploy = url_file_deploy.strip()
                local("wget %s --no-check-certificate" % url_file_deploy)
                local("mv *.war regis.war")
            print ("##############  Backup and Move file war  ##############\n")
            with cd("/opt/tomcat/"):
                run("/opt/tomcat/bin/shutdown.sh")
                run("mv /opt/tomcat/webapps/regis   %s" %directory_backup)
            file_deploy = directory_release + "/regis.war"
            put(local_path=file_deploy,remote_path="/opt/tomcat/webapps/")
            print ("############### Unzip file war ####################### \n")
            with cd("/opt/tomcat/webapps/"):
                run ("unzip regis.war -d regis")
                file_config_bk_1= directory_backup + "/regis/WEB-INF/configs/spring-server-config.properties"
                file_config_bk_2= directory_backup + "/regis/WEB-INF/configs/spring-mail-config.xml"
                file_replaced_1 = "/opt/tomcat/webapps/regis/WEB-INF/configs/spring-server-config.properties"
                file_replaced_2 = "/opt/tomcat/webapps/regis/WEB-INF/configs/spring-mail-config.xml"
                run ("cp -rp %s %s " %(file_config_bk_1,file_replaced_1))
                run ("cp -rp %s %s " %(file_config_bk_2,file_replaced_2))
                run("/opt/tomcat/bin/startup.sh")
            print("############### Check md5sum ##################### \n")
            print("Check md5sum")
            run("md5sum /opt/tomcat/webapps/regis.war")
        else:
            print("Nhap sai gia tri roi")

def test():
    with settings(warn_only=True):
        result = run("diff /opt/tomcat/webapps/regis/WEB-INF/configs/spring-server-config.properties /opt/backup/20170513/083912/HOMEPAGE/configs/spring-server-config.properties ")
        print (result.splitlines())
@hosts(my_amsadmin)
def deploy_amsadmin():
    print ("########### Create Folder Backup Ann Replease ##############")
    with lcd("/opt"):
        DATE_Release = local("date +%Y%m%d/%H%M%S", capture=True)
        directory_release = "/opt/release/" + DATE_Release + "/amsadmin"
        if os.path.exists(directory_release) != "True":
            local("mkdir -p %s" % (directory_release))
    with cd("/opt/backup"):
        DATE = run("date +%Y%m%d/%H%M%S")
        directory_backup = "/opt/backup/" + DATE + "/amsadmin"
        if exists(directory_backup) != "True":
            run("mkdir -p %s" % directory_backup)
    print("Please, Select option to deploy: \n 1. Change File Config \n 2. Change Source WebApp:  ")
    number_deploy = prompt("Please, Select option to deploy: ")
    if int(number_deploy) == 1:
        while True:
            number_file_changed = prompt("Please, number file changed:")
            if int(number_file_changed) > 0:
                break
        array_name_file = []
        i = 1
        while True:
            name_file_input = prompt("Plesae, Input name file changed:")
            array_name_file.append(name_file_input)
            i += 1
            if (i > int(number_file_changed)):
                break
        list_md5_diff = []
        for name_file in array_name_file:
            with cd("/opt/tomcat"):
                path_file = run('find  -name %s' % name_file)
                print("File located: \n %s" % path_file)
                while True:
                    cf_path_file = prompt("Please, Input path file config change:")
                    cf_path_file = cf_path_file.strip()
                    root_path = run("pwd")
                    if cf_path_file[0] == ".":
                        cf_path_file_new = root_path + cf_path_file[1:]
                    else:
                        cf_path_file_new = cf_path_file
                    if exists(cf_path_file_new):
                        break
                folder_backup = string.replace(cf_path_file_new, name_file, "")
                run("cp -rp %s %s" % (folder_backup, directory_backup))
            get(remote_path=cf_path_file_new, local_path=directory_release)
            with lcd("%s" % directory_release):
                local("vim %s" % name_file)
                path_file_changed = directory_release + "/" + name_file
                put(local_path=path_file_changed, remote_path=cf_path_file_new)
            with cd("%s" % directory_backup):
                path_file_backup = run('find  -name %s' % name_file)
                if path_file_backup[0] == ".":
                    root_path_backup = run("pwd")
                    path_file_backup = root_path_backup + path_file_backup[1:]
            new = []
            new.append(run("md5sum %s" % cf_path_file_new))
            with settings(warn_only=True):
                command_diff = "diff " + cf_path_file_new + " " + path_file_backup
                # command_diff = "'diff %s %s ' % (cf_path_file_new, path_file_backup)"
                result = run("%s" % command_diff)
            new.append(command_diff)
            new.append(result)
            #     print (result.splitlines())
            # new.append(run("diff %s %s " % (cf_path_file_new, path_file_backup)))
            list_md5_diff.append(new)
        print("\n################ Check md5sum and diff ################\n")
        for compoment in list_md5_diff:
            for i in compoment:
                print ("%s" % i)
    elif int(number_deploy) == 2:
        print ("##################  Get File deploy   ################# \n")
        with lcd("%s" % directory_release):
            url_file_deploy = prompt("Please, Input url download:")
            url_file_deploy = url_file_deploy.strip()
            local("wget %s --no-check-certificate" % url_file_deploy)
            local("mv *.war ROOT.war")
        print ("##############  Backup and Move file war  ##############\n")
        with cd("/opt/tomcat/"):
            run("/opt/tomcat/bin/shutdown.sh")
            run("mv /opt/tomcat/webapps/ROOT   %s" % directory_backup)
            run("cp -rp /opt/tomcat/meta_conf %s" %directory_backup)
            run("rm /opt/tomcat/work/Catalina/localhost/* -rf")
        file_deploy = directory_release + "/ROOT.war"
        put(local_path=file_deploy, remote_path="/opt/tomcat/webapps/")
        print ("############### Unzip file war ####################### \n")
        with cd("/opt/tomcat/webapps/"):
            run("unzip ROOT.war -d ROOT")
            file_config_bk_1 = directory_backup + "/ROOT/WEB-INF/configs/spring-server-config.properties"
            file_config_bk_2 = directory_backup + "/ROOT/images/logo/logo_ams.png"
            file_config_bk_3 = directory_backup + "/ROOT/images/logo_by.png"
            file_config_bk_4 = directory_backup + "/ROOT/images/logo.jpg"
            file_replaced_1 = "/opt/tomcat/webapps/ROOT/WEB-INF/configs/spring-server-config.properties"
            file_replaced_2 = "/opt/tomcat/webapps/ROOT/images/logo/logo_ams.png"
            file_replaced_3 = "/opt/tomcat/webapps/ROOT/images/logo_by.png"
            file_replaced_4  = "/opt/tomcat/webapps/ROOT/images/logo.jpg"
            run("cp -rp %s %s " % (file_config_bk_1, file_replaced_1))
            run("cp -rp %s %s " % (file_config_bk_2, file_replaced_2))
            run("cp -rp %s %s " % (file_config_bk_3, file_replaced_3))
            run("cp -rp %s %s " % (file_config_bk_4, file_replaced_4))
            run("/opt/tomcat/bin/startup.sh")
        print("############### Check md5sum ##################### \n")
        print("Check md5sum")
        run("md5sum /opt/tomcat/webapps/ROOT.war")
    else:
        print("Nhap sai gia tri roi")

def deploy_simple_mypage():
    print ("########### Create Folder Backup Ann Replease ##############")
    with lcd("/opt"):
        DATE_Release = local("date +%Y%m%d/%H%M%S", capture=True)
        directory_release = "/opt/release/" + DATE_Release + "/simplemypage"
        if os.path.exists(directory_release) != "True":
            local("mkdir -p %s" % (directory_release))
    with cd("/opt/backup"):
        DATE = run("date +%Y%m%d/%H%M%S")
        directory_backup = "/opt/backup/" + DATE + "/simplemypage"
        if exists(directory_backup) != "True":
            run("mkdir -p %s" % directory_backup)
    print("Please, Select option to deploy: \n 1. Change File Config \n 2. Change Source WebApp:  ")
    number_deploy = prompt("Please, Select option to deploy: ")
    if int(number_deploy) == 1:
        while True:
            number_file_changed = prompt("Please, number file changed:")
            if int(number_file_changed) > 0:
                break
        array_name_file = []
        i = 1
        while True:
            name_file_input = prompt("Plesae, Input name file changed:")
            array_name_file.append(name_file_input)
            i += 1
            if (i > int(number_file_changed)):
                break
        list_md5_diff = []
        for name_file in array_name_file:
            with cd("/opt/tomcat_mypage_simple"):
                path_file = run('find  -name %s' % name_file)
                print("File located: \n %s" % path_file)
                while True:
                    cf_path_file = prompt("Please, Input path file config change:")
                    cf_path_file = cf_path_file.strip()
                    root_path = run("pwd")
                    if cf_path_file[0] == ".":
                        cf_path_file_new = root_path + cf_path_file[1:]
                    else:
                        cf_path_file_new = cf_path_file
                    if exists(cf_path_file_new):
                        break
                folder_backup = string.replace(cf_path_file_new, name_file, "")
                run("cp -rp %s %s" % (folder_backup, directory_backup))
            get(remote_path=cf_path_file_new, local_path=directory_release)
            with lcd("%s" % directory_release):
                local("vim %s" % name_file)
                path_file_changed = directory_release + "/" + name_file
                put(local_path=path_file_changed, remote_path=cf_path_file_new)
            with cd("%s" % directory_backup):
                path_file_backup = run('find  -name %s' % name_file)
                if path_file_backup[0] == ".":
                    root_path_backup = run("pwd")
                    path_file_backup = root_path_backup + path_file_backup[1:]
            new = []
            new.append(run("md5sum %s" % cf_path_file_new))
            with settings(warn_only=True):
                command_diff = "diff " + cf_path_file_new + " " + path_file_backup
                result = run("%s" % command_diff)
            new.append(command_diff)
            new.append(result)
            list_md5_diff.append(new)
        print("\n################ Check md5sum and diff ################\n")
        for compoment in list_md5_diff:
            for i in compoment:
                print ("%s" % i)
    elif int(number_deploy) == 2:
        print ("##################  Get File deploy   ################# \n")
        with lcd("%s" % directory_release):
            url_file_deploy = prompt("Please, Input url download:")
            url_file_deploy = url_file_deploy.strip()
            local("wget %s --no-check-certificate" % url_file_deploy)
            local("mv *.war simplemypage.war")
        print ("##############  Backup and Move file war  ##############\n")
        with cd("/opt/tomcat_mypage_simple/"):
            run("/opt/tomcat_mypage_simple/bin/shutdown.sh")
            run("mv /opt/tomcat_mypage_simple/webapps/simplemypage   %s" % directory_backup)
            run("cp -rp /opt/tomcat_mypage_simple/front_conf %s" %directory_backup)
            run("rm /opt/tomcat_mypage_simple/work/Catalina/localhost/* -rf")
        file_deploy = directory_release + "/simplemypage.war"
        put(local_path=file_deploy, remote_path="/opt/tomcat_mypage_simple/webapps/")
        print ("############### Unzip file war ####################### \n")
        with cd("/opt/tomcat_mypage_simple/webapps/"):
            run("unzip simplemypage.war -d simplemypage")
            file_config_bk_1 = directory_backup + "/simplemypage/WEB-INF/configs/spring-server-config.properties"
            file_replaced_1 = "/opt/simplemypage/webapps/simplemypage/WEB-INF/configs/spring-server-config.properties"
            run("cp -rp %s %s " % (file_config_bk_1, file_replaced_1))
            run("/opt/simplemypage/bin/startup.sh")
        print("############### Check md5sum ##################### \n")
        print("Check md5sum")
        run("md5sum /opt/simplemypage/webapps/simplemypage.war")
    else:
        print("Nhap sai gia tri roi")

def deploy_tomcat_homepage_api():
    print ("########### Create Folder Backup And Replease ##############")
    with lcd("/opt"):
        DATE_Release = local("date +%Y%m%d/%H%M%S", capture=True)
        directory_release = "/opt/release/" + DATE_Release + "/api"
        if os.path.exists(directory_release) != "True":
            local("mkdir -p %s" % (directory_release))
    with cd("/opt/backup"):
        DATE = run("date +%Y%m%d/%H%M%S")
        directory_backup = "/opt/backup/" + DATE + "/api"
        if exists(directory_backup) != "True":
            run("mkdir -p %s" % directory_backup)
    print("Please, Select option to deploy: \n 1. Change File Config \n 2. Change Source WebApp:  ")
    number_deploy = prompt("Please, Select option to deploy: ")
    if int(number_deploy) == 1:
        while True:
            number_file_changed = prompt("Please, number file changed:")
            if int(number_file_changed) > 0:
                break
        array_name_file = []
        i = 1
        while True:
            name_file_input = prompt("Plesae, Input name file changed:")
            array_name_file.append(name_file_input)
            i += 1
            if (i > int(number_file_changed)):
                break
        list_md5_diff = []
        for name_file in array_name_file:
            with cd("/opt/tomcat_api"):
                path_file = run('find  -name %s' % name_file)
                print("File located: \n %s" % path_file)
                while True:
                    cf_path_file = prompt("Please, Input path file config change:")
                    cf_path_file = cf_path_file.strip()
                    root_path = run("pwd")
                    if cf_path_file[0] == ".":
                        cf_path_file_new = root_path + cf_path_file[1:]
                    else:
                        cf_path_file_new = cf_path_file
                    if exists(cf_path_file_new):
                        break
                folder_backup = string.replace(cf_path_file_new, name_file, "")
                run("cp -rp %s %s" % (folder_backup, directory_backup))
            get(remote_path=cf_path_file_new, local_path=directory_release)
            with lcd("%s" % directory_release):
                local("vim %s" % name_file)
                path_file_changed = directory_release + "/" + name_file
                put(local_path=path_file_changed, remote_path=cf_path_file_new)
            with cd("%s" % directory_backup):
                path_file_backup = run('find  -name %s' % name_file)
                if path_file_backup[0] == ".":
                    root_path_backup = run("pwd")
                    path_file_backup = root_path_backup + path_file_backup[1:]
            new = []
            new.append(run("md5sum %s" % cf_path_file_new))
            with settings(warn_only=True):
                command_diff = "diff " + cf_path_file_new + " " + path_file_backup
                result = run("%s" % command_diff)
            new.append(command_diff)
            new.append(result)
            list_md5_diff.append(new)
        print("\n################ Check md5sum and diff ################\n")
        for compoment in list_md5_diff:
            for i in compoment:
                print ("%s" % i)
    elif int(number_deploy) == 2:
        print ("##################  Get File deploy   ################# \n")
        with lcd("%s" % directory_release):
            url_file_deploy = prompt("Please, Input url download:")
            url_file_deploy = url_file_deploy.strip()
            local("wget %s --no-check-certificate" % url_file_deploy)
            local("mv *.war api.war")
        print ("##############  Backup and Move file war  ##############\n")
        with cd("/opt/tomcat_api/"):
            run("/opt/tomcat_api/bin/shutdown.sh")
            run("mv /opt/tomcat_api/webapps/api   %s" % directory_backup)
            run("cp -rp /opt/tomcat_api/meta_conf %s" %directory_backup)
            run("rm /opt/tomcat_api/work/Catalina/localhost/* -rf")
        file_deploy = directory_release + "/api.war"
        put(local_path=file_deploy, remote_path="/opt/tomcat_api/webapps/")
        print ("############### Unzip file war ####################### \n")
        with cd("/opt/tomcat_api/webapps/"):
            run("unzip api.war -d api")
            file_config_bk_1 = directory_backup + "/api/WEB-INF/configs/spring-server-config.properties"
            file_replaced_1 = "/opt/tomcat_api/webapps/api/WEB-INF/configs/spring-server-config.properties"
            run("cp -rp %s %s " % (file_config_bk_1, file_replaced_1))
            run("/opt/tomcat_api/bin/startup.sh")
        print("############### Check md5sum ##################### \n")
        print("Check md5sum")
        run("md5sum /opt/tomcat_api/webapps/simplemypage.war")
    else:
        print("Nhap sai gia tri roi")

def deploy_tomcat_cas():
    print ("########### Create Folder Backup Ann Replease ##############")
    with lcd("/opt"):
        DATE_Release = local("date +%Y%m%d/%H%M%S", capture=True)
        directory_release = "/opt/release/" + DATE_Release + "/ams"
        if os.path.exists(directory_release) != "True":
            local("mkdir -p %s" % (directory_release))
    with cd("/opt/backup"):
        DATE = run("date +%Y%m%d/%H%M%S")
        directory_backup = "/opt/backup/" + DATE + "/ams"
        if exists(directory_backup) != "True":
            run("mkdir -p %s" % directory_backup)
    print("Please, Select option to deploy: \n 1. Change File Config \n 2. Change Source WebApp:  ")
    number_deploy = prompt("Please, Select option to deploy: ")
    if int(number_deploy) == 1:
        while True:
            number_file_changed = prompt("Please, number file changed:")
            if int(number_file_changed) > 0:
                break
        array_name_file = []
        i = 1
        while True:
            name_file_input = prompt("Plesae, Input name file changed:")
            array_name_file.append(name_file_input)
            i += 1
            if (i > int(number_file_changed)):
                break
        list_md5_diff = []
        for name_file in array_name_file:
            with cd("/opt/tomcat"):
                path_file = run('find  -name %s' % name_file)
                print("File located: \n %s" % path_file)
                while True:
                    cf_path_file = prompt("Please, Input path file config change:")
                    cf_path_file = cf_path_file.strip()
                    root_path = run("pwd")
                    if cf_path_file[0] == ".":
                        cf_path_file_new = root_path + cf_path_file[1:]
                    else:
                        cf_path_file_new = cf_path_file
                    if exists(cf_path_file_new):
                        break
                folder_backup = string.replace(cf_path_file_new, name_file, "")
                run("cp -rp %s %s" % (folder_backup, directory_backup))
            get(remote_path=cf_path_file_new, local_path=directory_release)
            with lcd("%s" % directory_release):
                local("vim %s" % name_file)
                path_file_changed = directory_release + "/" + name_file
                put(local_path=path_file_changed, remote_path=cf_path_file_new)
            with cd("%s" % directory_backup):
                path_file_backup = run('find  -name %s' % name_file)
                if path_file_backup[0] == ".":
                    root_path_backup = run("pwd")
                    path_file_backup = root_path_backup + path_file_backup[1:]
            new = []
            new.append(run("md5sum %s" % cf_path_file_new))
            with settings(warn_only=True):
                command_diff = "diff " + cf_path_file_new + " " + path_file_backup
                # command_diff = "'diff %s %s ' % (cf_path_file_new, path_file_backup)"
                result = run("%s" % command_diff)
            new.append(command_diff)
            new.append(result)
            list_md5_diff.append(new)
        print("\n################ Check md5sum and diff ################\n")
        for compoment in list_md5_diff:
            for i in compoment:
                print ("%s" % i)
    elif int(number_deploy) == 2:
        print ("##################  Get File deploy   ################# \n")
        with lcd("%s" % directory_release):
            url_file_deploy = prompt("Please, Input url download:")
            url_file_deploy = url_file_deploy.strip()
            local("wget %s --no-check-certificate" % url_file_deploy)
            local("mv *.war ams.war")
        print ("##############  Backup and Move file war  ##############\n")
        with cd("/opt/tomcat/"):
            run("/opt/tomcat/bin/shutdown.sh")
            run("mv /opt/tomcat/webapps/ams   %s" % directory_backup)
        file_deploy = directory_release + "/ams.war"
        put(local_path=file_deploy, remote_path="/opt/tomcat/webapps/")
        print ("############### Unzip file war ####################### \n")
        with cd("/opt/tomcat/webapps/"):
            run("/opt/tomcat/bin/shutdown.sh")
            run("unzip ams.war -d ams")
#            file_config_bk_1 = directory_backup + "/regis/WEB-INF/configs/spring-server-config.properties"
#            file_config_bk_2 = directory_backup + "/regis/WEB-INF/configs/spring-mail-config.xml"
#            file_replaced_1 = "/opt/tomcat/webapps/regis/WEB-INF/configs/spring-server-config.properties"
#            file_replaced_2 = "/opt/tomcat/webapps/regis/WEB-INF/configs/spring-mail-config.xml"
#            run("cp -rp %s %s " % (file_config_bk_1, file_replaced_1))
#            run("cp -rp %s %s " % (file_config_bk_2, file_replaced_2))
            run("/opt/tomcat/bin/startup.sh")
        print("############### Check md5sum ##################### \n")
        print("Check md5sum")
        run("md5sum /opt/tomcat/webapps/regis.war")
    else:
        print("Nhap sai gia tri roi")

if __name__ == '__main__':
    execute(deploy_homepage_register)
    


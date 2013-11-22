Title: Apache::Authn::Redmine, SVN commit: Can't chmod... Operation not permitted
Date: 2012-03-05 17:25:15
Slug: apacheauthnredmine-svn-commit-cant-chmod-operation


Привет!

Недавно столкнулся с одной проблемой в svn-репозитории, где авторизация
реализована с помощью Redmine (http://www.redmine.org/projects/redmine/wiki/Repositories_access_control_with_apache_mod_dav_svn_and_mod_perl).

Проблема проявлялась не всегда, а при очень странных обстоятельствах - когда
делается commit большого количество файлов

Что такое "много" точно сказать не могу. Постепенно увеличивая количество
файлов я смог воспроизвести проблему, когда их количество достигло 1329.

В логе Apache (svn работает через mod_dav) видны следующие ошибки:

    
    [Mon Mar 05 10:19:32 2012] [error] [client 195.88.124.162] Could not MERGE resource "/my-repo/!svn/act/db20c88f-8a7a-4e20-a689-cf47ee2897f1" into "/my-repo/trunk".  [409, #0]
    [Mon Mar 05 10:19:32 2012] [error] [client 195.88.124.162] An error occurred while committing the transaction.  [409, #1]
    [Mon Mar 05 10:19:32 2012] [error] [client 195.88.124.162] Can't chmod '/home/svn/my-repo/db/txn-protorevs/5-h.rev': Operation not permitted  [409, #1]
    

SVN-пользователь же получает при коммите следующую ошибку:

    
    Can't chmod '/home/svn/my-repo/db/txn-protorevs/3-9.rev': Operation not permitted
    

Как выяснилось - в подобных условиях MERGE resource производится не от
пользователя, от которого работает web-сервер и mod_dav, соответственно (до
этого я использовать mod-event), а пользователь, от которого работает Redmine.
Почему так происходит - я не могу сказать, т.к. код модуля
Apache::Authn::Redmine не рассматривал (да-да, нужно отписать баг-репорт
(найти бы время на детальное исследования вопроса для оформления эного)).

В качестве достойного на мой взгляд work-around'а я рекомендую переход на MPM-
ITK.

В CentOS сделать это очень просто:

1) Ставим http://centos.alt.ru/ repo. 2) Обновляем Apache:

    
    yum update httpd
    

3) Правим /etc/sysconfig/httpd

    
    # ITK model
    HTTPD=/usr/sbin/httpd.itk
    

4) Правим /etc/httpd/conf.d/php.conf, добавляя:

    
      LoadModule php5_module modules/libphp5.so
    

5) Правим Virtual Host, который обслуживает SVN, добавляя в него строку:

    
    AssignUserID redmine redmine
    

, где redmine - имя пользователя и группа, от которого работает Redmine.


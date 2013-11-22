Title: Создание бекапов баз даных MySQL в Bacula
Date: 2012-01-14 18:40:19
Slug: sozdanie-bekapov-baz-danyh-mysql-v-bacula


Доброго времени, друзья.

Недавно я [написал статью о установка продвинутой системы резервного Bacula на
CentOS 6](/blog/2012/ustanovka-sistemy-rezervnogo-kopirovaniya-bacula-n/).

Bacula - отличная система, но в список её возможностей не входит создание
дампов баз данных MySQL.

Так что сегодня я освещу этот вопрос.

Начнём мы с написания скрипта, что будет создавать дампы баз данных MySQL. Не
забудьте указать нужные базы данных в $DBS_LIST.

#### Универсальный скрипт создания дампов баз данных MySQL:

    
     1
     2
     3
     4
     5
     6
     7
     8
     9
    10
    11
    12
    13
    14
    15
    16
    17
    
    #!/bin/bash
    DBS_LIST="database1 database2 databaseN"
    MYSQLDUMP="/usr/bin/mysqldump"
    MYSQLDUMP_OPTS="-a"
    MYSQL_HOST="localhost"
    MYSQL_USER="root"
    MYSQL_PASS="SUPERPASS"
    BACKUP_DIR="/backups/mysql"
    for db_name in $DBS_LIST; do
            dump_file_path="$BACKUP_DIR/$db_name.sql";
            echo -n "* Create dump for database '$db_name' to '$dump_file_path'...";
            if $MYSQLDUMP -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASS $MYSQLDUMP_OPTS $db_name > $dump_file_path; then
                    echo "[DONE]";
            else
                    echo "[ERROR]";
            fi
    done
    

Данный скрипт размещаем в /usr/local/bin/dbbackup.sh, к примеру, и даём ему
права на выполнение:

    
    chmod 755 /usr/local/bin/dbbackup.sh
    

#### Настройка Bacula Director

Теперь пришло время настроить Директора на бекап дампов баз данных. Идея
такова - при запуске Bacula Job Bacula Client (File Server) запускает скрипт
создания дампов баз данных и складывает созданные дампы в /backups/mysql.
После Bacula резервирует указанные в настройках Director каталоги, а вместе с
ним /backups/mysql.

Таким образом у нас всегда будет актуальные дампы баз данных в бекапах Bacula.

Итак, идём на сервер, где установлена Bacula Director и правим конфиг
/etc/bacula/bacula-dir.conf. Поправить нам будет нужно только с секции Job и
FileSet.

В секцию Job добавляем RunBeforeJob

    
    Job {
      Name          = "BackupMyServer"
      JobDefs      = "DefaultJob"
      Client          = myserver
      FileSet       = "myserver"
      ClientRunBeforeJob  = "/usr/local/bin/dbbackup.sh" # Перед заливкой запустить наш скрипт для создания дампов MySQL
    }
    

В секцию FileSet добавляем каталог, где наш скрипт складывает дампы:

    
    FileSet {
      Name = "myserver"
      Include {
        Options {
          signature = MD5 #Для сверки используем MD5
          Compression=GZIP #Используем GZIP компрессию
        }
        File = /home/
        File = /backups/
        File = /etc/nginx/
        FIle = /backups/mysql/ # Каталог, где лежат дампы баз MySQL
      }
    }
    

Выполняем мягкую перезагрузку сервиса Bacula Director для принятия изменений:

    
    service bacula-dir reload
    

Вот так просто можно делать бекапы баз данных при использовании Bacula!


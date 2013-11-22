Title: Установка системы резервного копирования Bacula 5.0 на CentOS 6
Date: 2012-01-03 18:22:11
Slug: ustanovka-sistemy-rezervnogo-kopirovaniya-bacula-n


Всем доброго времени суток!

Сегодня я расскажу о продвинутой системе для создания резервных копий -
[Bacula](http://www.bacula.org/).

Это статья призвана донести общую информацию о работе Bacula на примере её
установки на CentOS 6. В Base-репозитории CentOS 6 на данный момент вирсия
продукта 5.0. На её примере и будет построена документация.

Статья сама по себе может оказаться полезной, но прежде, чем ринуться
применять полученные знания на в production-решениях я настоятельно советую
ознакомится с [официальной
документацией](http://www.bacula.org/en/?page=documentation) и ответить себе
на несколько вопросов:

  * **_Я использую rsync/tar/самописные скрипты - зачем мне что то ещё?_**

_В таком случае Вам, скорее всего, не нужна Bacula. Эта система рассчитана на
более масштабные задачи, чем бекап одного-двух серверов. Она позволяет
организовывать централизированную распределённую систему бекепов практически
чего угодно и куда угодно, включая возможность записи dvd-диски и магнитную
ленту стримера._

  * **_Сейчас я произвожу бекап данных по протоколам, что поддерживаются многими ОС (таких как ftp или samba). Смогу ли я делать что то подобное с Bacula?_**

_Bacula не поддерживает сторонние протоколы передачи данных, а использует
свой. Но это давольно кросплатформенный продукт. Так что Вы сможете
производить бекапы даже компьютеров с Windows._

Итак, немного теории.

## Теория

Bacula состоит из нескольких независимых компонентов: Director, Console, File,
Storage и сервисы мониторинга.

![Структура Bacula](/blog/2012/ustanovka-sistemy-rezervnogo-kopirovaniya-)

### Bacula Director

Bacula Director выполняет функции "директора" над всеми остальными сервисами -
запускает создание резервных копий и операции восстановление из бекапов,
управляет сервисами хранения данных (**_Bacula Storage_**), отсылке
уведомлений и т.д.

### Bacula Console

Bacula Console служит для управления Bacula Director. Она имеет 3 версии
интерфейса: _ CLI _ QT-based * wxWidgets CLI лично меня всем устраивает, но
GUI у Bacula так же не уступают возможностями, что не может не радовать.

### Bacula File

Bacula File (так же известна, как Клиентская часть) - это сервис, что
устанавливается на узлы, данные которого нужно резервировать. Существуют
версии для разных ОС. Все файлы доступны на [странице
sourceforge](http://sourceforge.net/projects/bacula/files/#files).

### Bacula Storage

Bacula Storage - это сервис, основной целью которого есть управление хранением
данных с резервными копиями. Другими словами Bacula Storage используется
Bacula Director для чтения / записи данных с клентских машин, информация
которых резервируется.

### Catalog

Catalog используется для хранения данных о бекепах, файлах, хранилищах и
всего, с чем работает Bacula Director. Catalog может использовать для хранения
данных различные БД, среди которых MySQL, PostgreSQL и SQLite.

### Bacula Monitor

Bacula Monitor - это приложение, по даёт ифнормацию о состоянии Bacula
Director и его задачах. Это могут быть состояния тех или иных задач
(создание/восстановление резервных копий), доступность сервисов Bacula и т.д.
Существует несколько вариаций Bacula Monitor - все из них используют GTK+ и
работают как в KDE, GNOME так и других рабочих окружениях.

## Установка

### SELinux disable

    
    sed -i "s/SELINUX=.*/SELINUX=disabled/g" /etc/sysconfig/selinux
    setenforce 0
    

### MySQL Server

Мы будем использовать БД MySQL для хранения данных Bacula.

Выполняем установку:

    
    yum -y install mysql-server mysql-devel
    

Запускаем MySQL-server и добавляем его init-скрипт в автозагрузку:

    
    service mysqld start
    chkconfig mysqld on
    

Генерируем пароль для root-пользователя MySQL, устанавливаем его и добавляем в
/root/.my.cnf, чтобы будучи в shell от root иметь беспарольный доступ в MySQL
Shell от имени суперпользователя.

    
    MATRIX="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LENGTH="10"
    while [ "${n:=1}" -le "$LENGTH" ]; do PASS="$PASS${MATRIX:$(($RANDOM%${#MATRIX})):1}"; let n+=1; done
    echo -e "[client]
    user=root
    password=$PASS" > /root/.my.cnf
    /usr/bin/mysqladmin -u root password $PASS
    PASS=""
    n=""
    

### Bacula services

В нашем примере будет использовано 2 физических сервера. На первом будут
установлены Director, File, Storage и Catalog (для бекапа данного сервера,
хранения данных и управления всеми сервисами), а на втором будет расположен
исключительно Bacula Client для создания бекапов данных на 2 сервере.

#### Server 2: Bacula Client

Как это ни странно - мы начнём настройку с второго сервера, клиентского. Я
посчитал, что настраивать доступы к клиентской части и после указывать их в
основном конфиге директора проще, чем делать это в обратной
последовательности.

Устанавливаем клиентскую часть на сервер, что будем бекапить.

    
    yum -y install bacula-client
    

Правим конфиг **/etc/bacula/bacula-fd.conf** указывая пароли доступа к Bacula
Client (Поля Password) для Директора и tray-monitor.

    
    Director {
      Name = bacula-dir
      Password = "DIRBASSWORD"
    }
    Director {
      Name = bacula-mon
      Password = "MOPASSWORD"
      Monitor = yes
    }
    FileDaemon {                          # this is me
      Name = bacula-fd
      FDport = 9102                  # where we listen for the director
      WorkingDirectory = /var/spool/bacula
      Pid Directory = /var/run
      Maximum Concurrent Jobs = 20
    }
    Messages {
      Name = Standard
      director = bacula-dir = all, !skipped, !restored
    }
    

Запускаем сервис и добавляем его в автозагрузку:

    
    service bacula-fd start
    chkconfig bacula-fd on
    

**_Во время настройки у меня небыло выделенного домена, который бы резолвился на всех используемых серверах для bacula-sd, и я наткнулся на проблему, когда бекап не мог запуститься, ругаясь следующим образом:_**

> Bad response to Storage command: wanted 2000 OK storage

Как оказалось - Bacula Client обращается к Bacula Storage напрямую и т.к. я
указывал fqdn в конфигурации bacula-dir, который не резолвился, но был на
сервере Bacula Director, а на сервере, где расположен Bacula Client в host
соответствующей записи небыло, клиент и не мог подключится.

**Решение**: все сервера в системе Bacula должны иметь доступ к доменам, что указаны в конфигурационных файлах.

#### Server 1: Bacula Director, Catalog, Storage

Теперь переходим к основной части - настройке Директора (Director), что хранит
данные в MySQL (посредством Catalog) и сервиса хранения данных бекапов
(Storage).

##### Установка пакетов через YAM

    
    yum -y install bacula-storage-mysql bacula-director-mysql bacula-console
    

##### Настройка базы и пользователя MySQL для работы с Bacula

Теперь создадим MySQL-пользователя, базу данных и расставим нужные привилегии.

    
    /usr/libexec/bacula/grant_mysql_privileges
    /usr/libexec/bacula/create_mysql_database
    /usr/libexec/bacula/make_mysql_tables
    /usr/libexec/bacula/grant_bacula_privileges
    

Сгенерируем пароль для MySQL-пользователя bacula и установим его.

    
    MATRIX="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LENGTH="10"
    while [ "${n:=1}" -le "$LENGTH" ]; do PASS="$PASS${MATRIX:$(($RANDOM%${#MATRIX})):1}"; let n+=1; done
    BACULA_MYSQL_PASS="$PASS"
    PASS=""
    n=""
    mysql -e "UPDATE mysql.user SET password=PASSWORD('$BACULA_MYSQL_PASS') WHERE user='bacula'; flush privileges;"
    sed -i "s/dbpassword.*/dbpassword = "$BACULA_MYSQL_PASS"/g" /etc/bacula/bacula-dir.conf
    

##### Конфигурация Storage

Создадим каталог на сервере, где мы будем хранить бекапы. Он должен
располагаться на самом большом и незанятом разделе, переполнения которого, по
возможности, не нарушит работу всей системы и/или других сервисов. В данном
случае я расположу его в /backups/, куда будет монтироваться нужный мне
раздел.

    
    mkdir /backups/
    

Настроим на Bacula Storage в конфигурационном файле **/etc/bacula/bacula-
sd.conf**:

    
    Storage {                             # definition of myself
      Name = bacula-sd
      SDPort = 9103                  # Director's port
    
      WorkingDirectory = "/var/spool/bacula"
      Pid Directory = "/var/run"
      Maximum Concurrent Jobs = 20
    }
    Director {
      Name = bacula-dir
      Password = "SDPASSWORD"
    }
    Director {
      Name = bacula-mon
      Password = "MODPASSWORD"
      Monitor = yes
    }
    Device {
      Name = FileStorage
      Media Type = File
      Archive Device = /backups
      LabelMedia = yes;                   # lets Bacula label unlabeled media
      Random Access = Yes;
      AutomaticMount = yes;               # when device opened, read it
      RemovableMedia = no;
      AlwaysOpen = no;
    }
    Messages {
      Name = Standard
      director = bacula-dir = all
    }
    

Стартуем сервис и добавляем в автозагрузку:

    
    service bacula-sd start
    chkconfig bacula-sd on
    

##### Конфигурация Director

Теперь нужно задать пароли для всех поднимаемых сервисов.

Открываем конфигурационный файл Директора **/etc/bacula/bacula-dir.conf** и
выполняем его настройку, указывая доступы к Storage и Client, а так же к
самому Bacula Server:

    
    Director {                            # define myself
      Name = bacula-dir
      DIRport = 9101                # where we listen for UA connections
      QueryFile = "/usr/libexec/bacula/query.sql"
      WorkingDirectory = "/var/spool/bacula"
      PidDirectory = "/var/run"
      Maximum Concurrent Jobs = 1
      Password = "DIRPASSWORD"         # Console password
      Messages = Daemon
    }
    JobDefs {
      Name = "DefaultJob"
      Type = Backup
      Level = Incremental
      FileSet = "Full Set"
      Schedule = "WeeklyCycle"
      Storage = File
      Messages = Standard
      Pool = File
      Priority = 10
      Write Bootstrap = "/var/spool/bacula/%c.bsr"
    }
      # This creates an ASCII copy of the catalog
      # Arguments to make_catalog_backup.pl are:
      #  make_catalog_backup.pl 
      # This deletes the copy of the catalog
    Job {
      Name          = "BackupMyServ"
      JobDefs       = "DefaultJob"
      Client        = myserv
      FileSet       = "myserv"
    } 
    FileSet {
      Name = "myserv"
      Include {
        Options {
          signature = MD5 #Для сверки используем MD5
          Compression=GZIP #Используем GZIP компрессию
        }
        File = /home/
        File = /backups/
        File = /etc/nginx/
      }
    }
    FileSet {
      Name = "Full Set"
      Include {
        Options {
          signature = MD5
        }
        File = /usr/sbin
      }
      Exclude {
        File = /var/spool/bacula
        File = /tmp
        File = /proc
        File = /tmp
        File = /.journal
        File = /.fsck
      }
    }
    Schedule {
      Name = "WeeklyCycle"
      Run = Full 1st sun at 23:05
      Run = Differential 2nd-5th sun at 23:05
      Run = Incremental mon-sat at 23:05
    }
    Schedule {
      Name = "WeeklyCycleAfterBackup"
      Run = Full sun-sat at 23:10
    }
    FileSet {
      Name = "Catalog"
      Include {
        Options {
          signature = MD5
        }
        File = "/var/spool/bacula/bacula.sql"
      }
    }
    Client {
      Name = myserv
      Address = myserv.example.com
      FDPort = 9102
      Catalog = MyCatalog
      Password = "CLIENTPASS"          # password for FileDaemon
      File Retention = 30 days            # 30 days
      Job Retention = 6 months            # six months
      AutoPrune = yes                     # Prune expired Jobs/Files
    }
    Storage {
      Name = File
      Address = backup.example.com                # N.B. Use a fully qualified name here
      SDPort = 9103
      Password = "STORAGEPASS"
      Device = FileStorage
      Media Type = File
    }
    Catalog {
      Name = MyCatalog
      dbname = "bacula"; dbuser = "bacula"; dbpassword = "MYSQLPASS"
    }
    Messages {
      Name = Standard
      mailcommand = "/usr/sbin/bsmtp -h localhost -f "(Bacula) <%r>" -s "Bacula: %t %e of %c %l" %r"
      operatorcommand = "/usr/sbin/bsmtp -h localhost -f "(Bacula) <%r>" -s "Bacula: Intervention needed for %j" %r"
      mail = me@example.com = all, !skipped
    
      operator = dcshnik@hoster.com = mount
      console = all, !skipped, !saved
      append = "/var/spool/bacula/log" = all, !skipped
      catalog = all
    }
    Messages {
      Name = Daemon
      mailcommand = "/usr/sbin/bsmtp -h localhost -f "(Bacula) <%r>" -s "Bacula daemon message" %r"
      mail = root@localhost = all, !skipped
    
      console = all, !skipped, !saved
      append = "/var/log/bacula.log" = all, !skipped
    }
    Pool {
      Name = Default
      Pool Type = Backup
      Recycle = yes                       # Bacula can automatically recycle Volumes
      AutoPrune = yes                     # Prune expired volumes
      Volume Retention = 365 days         # one year
    }
    Pool {
      Name = File
      Pool Type = Backup
      Recycle = yes                       # Bacula can automatically recycle Volumes
      AutoPrune = yes                     # Prune expired volumes
      Volume Retention = 365 days         # one year
      Maximum Volume Bytes = 400G          # Limit Volume size to something reasonable
      Maximum Volumes = 1000               # Limit number of Volumes in Pool
    }
    Pool {
      Name = Scratch
      Pool Type = Backup
    }
    Console {
      Name = bacula-mon
      Password = "MODPASS"
      CommandACL = status, .status
    }
    

Запускаем директора и добавляем его в автозагрузку:

    
    service bacula-dir start
    chkconfig bacula-dir on
    

##### Конфигурация Console

Для управления Bacula существует несколько интерфейсов. Я предпочитаю CLI-
интефейс bconsole. Его мы сейчас и настроем в **/etc/bacula/bconsole.conf**:

    
    Director {
      Name = bacula-dir
      DIRport = 9101
      address = localhost
      Password = "DIRPASSWORD"
    }
    

Проверяем:

    
    # bconsole 
    Connecting to Director localhost:9101
    1000 OK: bacula-dir Version: 5.0.0 (26 January 2010)
    Enter a period to cancel a command.
    *quit
    

Доступ есть. Переходим к настройке бекапов и первому, тестовому запуску
задания.

##### Создание volume и тестовый запуск бекапов

    
    # bconsole 
    Connecting to Director localhost:9101
    1000 OK: bacula-dir Version: 5.0.0 (26 January 2010)
    Enter a period to cancel a command.
    *label
    Automatically selected Catalog: MyCatalog
    Using Catalog "MyCatalog"
    Automatically selected Storage: File
    Enter new Volume name: TestVolume
    Defined Pools:
         1: Default
         2: File
         3: Scratch
    Select the Pool (1-3): 2
    

Запускаем процесс бекапа клиента:

    
    # bconsole 
    Connecting to Director localhost:9101
    1000 OK: bacula-dir Version: 5.0.0 (26 January 2010)
    Enter a period to cancel a command.
    *run
    Automatically selected Catalog: MyVolume
    Using Catalog "MyVolume"
    A job name must be specified.
    Automatically selected Job: BackupMyServer
    Run Backup job
    JobName:  BackupMyServer
    Level:    Incremental
    Client:   pm
    FileSet:  pm
    Pool:     File (From Job resource)
    Storage:  File (From Job resource)
    When:     2012-01-14 03:25:50
    Priority: 10
    OK to run? (yes/mod/no): yes
    

Задание отправится в очередь на выполнение. Просмотреть статус его работы
можно командой:

    
    # bconsole
    
    Connecting to Director localhost:9101
    1000 OK: bacula-dir Version: 5.0.0 (26 January 2010)
    Enter a period to cancel a command.
    *status dir
    bacula-dir Version: 5.0.0 (26 January 2010) i686-pc-linux-gnu redhat (Final)
    Daemon started 14-Ян-2012 03:10, 0 Jobs run since started.
     Heap: heap=135,168 smbytes=88,613 max_bytes=89,166 bufs=311 max_bufs=317
    
    Scheduled Jobs:
    Level          Type     Pri  Scheduled          Name               Volume
    ===================================================================================
    Incremental    Backup    10  14-Ян-2012 23:05 BackupMyServer           MyVolume
    ====
    
    Running Jobs:
    Console connected at 14-Ян-2012 03:10
    Console connected at 14-Ян-2012 03:10
    Console connected at 14-Ян-2012 03:28
     JobId Level   Name                       Status
    ======================================================================
         9 Full    BackupMyServer.2012-01-14_03.11.25_04 is running
        10 Full    BackupMyServer.2012-01-14_03.26.03_06 is waiting execution
    ====
    *
    

## Заключение

Как видно из документации _Bacula_ - это не самая быстроконфигурируемая
система резервного копирования, но её гибкость и масштабируемость позволяет
поддерживать системы почти что любого уровня сложности и различных задач. В
руководстве, как уже было сказано, была описана базовый установка, что даёт
хорошее представление о том, как это будет работать и главное - имеет ли смысл
идти дальше и разворачивать свою систему Bacula.


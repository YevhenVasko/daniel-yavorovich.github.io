Title: Починка MySQL-репликации
Date: 2012-01-03 09:18:08
Slug: pochinka-mysql-replikacii


### Into

Предположим, что у нас уже настроена репликация MySQL, но мы увидели ошибку.
Обычно это выглядит так:

    
    mysql> show slave status\G
    *************************** 1. row ***************************
                 Slave_IO_State: Waiting for master to send event
                    Master_Host: 192.168.0.1
                    Master_User: db_name
                    Master_Port: 3306
                  Connect_Retry: 60
                Master_Log_File: mysqld-bin.000008
            Read_Master_Log_Pos: 609198672
                 Relay_Log_File: se-relay-bin.000276
                  Relay_Log_Pos: 241568916
          Relay_Master_Log_File: mysqld-bin.000008
               Slave_IO_Running: Yes
              Slave_SQL_Running: No
                Replicate_Do_DB: db_name
            Replicate_Ignore_DB:
             Replicate_Do_Table:
         Replicate_Ignore_Table:
        Replicate_Wild_Do_Table:
    Replicate_Wild_Ignore_Table:
                     Last_Errno: 0
                     Last_Error: Query caused different errors on master and slave. Error on master: 'Invalid error code' (126), Error on slave: 'no error' (0). Default database: 'db_name'. Query: 'DELETE FROM sess WHERE id IN (5315971, 5315968, 5315967, 5315965, 5315963, 5315962, 5315961, 5315960, 5315959, 5315958, 5315957, 5315956, 5315955, 5315954, 5315953, 5315952, 5315950, 5315949, 5315948, 5315947, 5315946, 5315945, 5315944, 5315942, 5315941, 5315939, 5315938, 5315937, 5315936, 5315935, 5315934, 5315933, 5315932, 5315931, 5315929, 5315928, 5315927, 5315924, 5315923, 5315922, 5315921, 5315920, 5315918, 5315917, 5315916, 5315914, 5315912, 5315910, 5315908, 5315907, 5315906, 5315904, 5315903, 5315902, 5315901, 5315899, 5315898, 5315897, 5315896, 5315895, 5315894, 5315893, 5315892, 5315891, 5315890, 5315888, 5315887, 5315886, 5315884, 5315882, 5315881, 5315880, 5315879, 5315878, 5315877, 5315876, 5315875, 5315874, 5315873, 5315871, 5315870, 5315869, 5315865, 5315864, 5315863, 5315862, 5315861, 5315860, 5315858, 5315857, 5315856, 5315855
                   Skip_Counter: 0
            Exec_Master_Log_Pos: 578805429
                Relay_Log_Space: 271962159
                Until_Condition: None
                 Until_Log_File:
                  Until_Log_Pos: 0
             Master_SSL_Allowed: No
             Master_SSL_CA_File:
             Master_SSL_CA_Path:
                Master_SSL_Cert:
              Master_SSL_Cipher:
                 Master_SSL_Key:
          Seconds_Behind_Master: NULL
    1 row in set (0.00 sec)
    

Сперва нам нужно создать актуальный дамп базы данных, сохранив имя файла
бинарных логов и последнюю позицию. Ранее это делалось мной руками, а сегодня
я узнал о такой замечательной опции mysqldump, как --master-data, которую мы и
будем использовать. '''--master-data''' добавляет в sql-dump "CHANGE MASTER" с
актуальными данными, что позволяет не выполнять лишних действий.

### Master

Запрещаем write-операции на master-сервере:

    
    mysql> FLUSH TABLES WITH READ LOCK;
    

Создаём sql-dump реплизируемой базы, включая "CHANGE MASTER":

    
    mysqldump --lock-all-tables --master-data db_name > db_name.sql
    

Не забываем разлочить таблицы:

    
    mysql> SET GLOBAL read_only = OFF;
    

Теперь копируем созданный dump на все слейвы.

### Slave

Останавливаем репликацию и на всякий случай ресетим данные бинарного лога.

    
    mysql> stop slave;
    mysql> reset slave;
    

Восстанавливаем реплицируемую БД из sql-dump'а (сразу выполнится CHANGE
MASTER. Мы расчитываем на то, что настройки доступа к master-серверу уже
прописаны в my.cnf и MySQL быз запущен с ними)

    
    cat db_name.sql | mysql db_name
    

Запускаем репликацию и проверяем статус.

    
    mysql> start slave;
    mysql> show slave status\G
    


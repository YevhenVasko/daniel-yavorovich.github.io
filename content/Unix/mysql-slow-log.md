Title: MySQL slow log
Date: 2012-01-03 19:35:49
Slug: mysql-slow-log


Для логгирования "долгих" запросов MySQL можно включить в секцию [mysqld]
конфигурации MySQL (для RHEL/CentOS это _/etc/my.cnf_) следующие параметры

    
    # Slow query log
    long_query_time = 1
    log-slow-queries = /var/log/mysql/slow_queries.log
    

  * long_query_time - значение в секундах, после которого запрос нужно считать "долгим" и записывать информацию о нём в log-файл

  * log-slow-queries - path к log-файлу MySQL, где будут фиксироваться запросы, что выполнялись дольше, чем это описано в _long_query_time_


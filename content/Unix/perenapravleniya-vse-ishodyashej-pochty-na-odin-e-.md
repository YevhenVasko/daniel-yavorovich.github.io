Title: Перенаправления всей исходящей почты на один E-mail в CentOS, используя Postfix и Dovecot.
Date: 2012-02-07 14:52:41
Slug: perenapravleniya-vse-ishodyashej-pochty-na-odin-e-


### Задача

Задача стояла так:

Есть development-сервер, на котором ведётся разработка различных web-
продуктов. Для тестов нужно собирать всю исходящую с сервера почту (sendmail,
php-mail, etc.) и складывать её в 1 месте, очищая этот склад раз в 10 дней.

#### Postfix - перенаправленные исходящих сообщений

Для начала поставим его:

    
    yum -y install postfix
    

Для перенаправленный всех исходящей почты я использовал Postfix. Всё, что
потребуется - это указать в /etc/postfix/main.cf строку с указанием файла, что
содержит правила для провеки headers. Правило можно разместить в конце файла,
как и правило, что будет указывать способ хранения писем. Я предпочитаю
Maildir, что упростит работу над удалением старых писем.

    
    header_checks = pcre:/etc/postfix/header_checks.pcre
    home_mailbox = Maildir/
    

Теперь заполняем сам /etc/postfix/header_checks.pcre

    
    /.*/ REDIRECT nullmail@dev.server
    

Как видно из правила - мы ловим все сообщения (регексп "/.*/") и выполняем над
ними действие REDIRECT на nullmail@dev.server.

nullmail@dev.server - это ящик, что будем распогать на этом же сервере, что
имеет hostname = "dev.server".

В перспективе я планировал изолировать почтовые сервисы от внешнего Мира,
чтобы не допустить возможности отправить сообщения с dev-севера на реальный
адрес посредством локального почтового сервера. Но об этом позже.

Для того, чтобы ловить письма сосздадим пользователя nullmail в системе,
который и будет хранить письма.

    
    useradd -s /sbin/nologin -m -g mail nullmail
    

Здаданим пароль пользователю. Его мы будем использовать при доступе к
почтовому ящику.

    
    passwd nullmail
    

Теперь запускаем postfix и добавляем его в автозагрузку:

    
    service postfix start
    chkconfig postfix on
    

#### Dovecot

В нашем случае достаточно стандартной настройки Dovecot и я не буду
акцентировать внимание на его тонкостях. В CentOS 6 из коробки с нужным нами
обязанностями он справляется на ура, так что просто поставим его и запустим.

    
    yum -y install dovecot
    service dovecot start
    chkconfig dovecot on
    

### Проверка

Теперь протестируем работу нашей системы:

    
    ifconfig | sendmail none@example.com
    

Таким образом мы отправили письмо на несуществующий ящик существующего (по
крайней мере, на момент создания поста) домена.

Проверим, пришло ли письмо:

    
    telnet localhost 110
    Trying ::1...
    Connected to localhost.
    Escape character is '^]'.
    +OK Dovecot ready.
    user nullmail
    +OK
    pass <введите пароль>
    +OK Logged in.
    stat
    +OK 1 1907
    quit
    +OK Logging out.
    Connection closed by foreign host.
    

Как видно из ответа - в ящике лежит письмо, что было перенаправлено на наш
локальный ящик.

В логах этот момент так же фиксируется:

    
    Feb  7 14:08:16 dev.server postfix/local[17481]: B2A3D101430: to=<nullmail@dev.server>, orig_to=<none@example.com>, relay=local, delay=0.3, delays=0.2/0.03/0/0.07, dsn=2.0.0, status=sent (delivered to maildir)
    

Отлично - всё работает.

### Ipatbles

Теперь закроем доступ к локальному smtp-/pop3-/imap-серверам и smtp-ящикам в
Мире:

    
    iptables -N MAIL
    iptables -A INPUT -p tcp -m multiport --dports 25,587,110,143,993,995 -j MAIL 
    iptables -A OUTPUT -p tcp -m multiport --dports 25,587,110,143,993,995 -j MAIL 
    iptables -A MAIL -s 127.0.0.1/32 -j ACCEPT 
    iptables -A MAIL -d 127.0.0.1/32 -j ACCEPT 
    iptables -A MAIL -j DROP
    service ipatbles save
    

Если iptables нет в автозагрузке - добавим его

    
    chkconfig iptables on
    

### Автоматическая очистка старых сообщений

Для этих целей мы напишем скрипт в 1 строчку и поместим его, скажем, в
/usr/local/bin/clean_old_email_messages.sh:

    
    1
    2
    
    #!/bin/bash
    /bin/find /home/nullmail/Maildir/new/ /home/nullmail/Maildir/cur/ -type f \! -newermt '10 day ago' -exec rm -f {} \;
    

И дадим ему права на выполнение:

    
    chmod +x /usr/local/bin/clean_old_email_messages.sh
    

Теперь добавим его в /etc/contab:

    
    00 00 * * *     /usr/local/bin/clean_old_email_messages.sh
    

Таким образом каждую полночь скрипт будет очищать сообщения, старше 10 дней.

### В виде заключения

Так же для удобства доступа к почте можно поставить Web-клиент электронной
почты, такой, как [Roundcube](http://roundcube.net/), скажем.


Title: Ограничение доступа к SSH по IP
Date: 2012-01-07 16:47:26
Slug: ogranichenie-dostupa-k-ssh-po-ip


Здравствуйте!

Краткий копипаст, как закрыть доступ к порту SSH всем, кроме определённых
адресов.

    
    iptables -N ALLOWED
    iptables -A INPUT -j ALLOWED
    iptables -A ALLOWED -s 95.211.115.248 -j ACCEPT
    iptables -A INPUT -p tcp --dport 22 -j DROP
    

Описание действий:

  * iptables -N ALLOWED - создаём свою цепочку в правилах iptables с иметем "ALLOWED".
  * iptables -A INPUT -j ALLOWED - Добавляем в цепочку INPUT действие ALLOWED. Это даёт возможность настраивать свои правила для INPUT в кастомной цепочке ALLOWED.
  * iptables -A ALLOWED -s 95.211.115.248 -j ACCEPT - разрешаем доступ для IP 95.211.115.248 ко всему, что только можно в нашей цепочке ALLOWED.
  * iptables -A INPUT -p tcp --dport 22 -j DROP - блокируем доступ к 22 порту всем. (т.к. правило с действием ALLOWED было заявлено раньше, наши правила с открытием доступа будут работать).

Если Вы используете RHEL/CentOS можно сохранить правила таким образом:

    
    service iptables save
    

Для того, чтобы добавить новый IP в вайтлист, можно использовать команду:

    
    iptables -A ALLOWED -s $new_ip -j ACCEPT
    

Для того, чтобы удалить IP из вайтлиста можно сделать так:

    
    iptables -D ALLOWED -s $ip -j ACCEPT
    

После не забываем сохранить правила в системном конфиге (для rpm-base это по
прежнему "servise iptables save")


Title: Puppet - список IP адресов сервера в template
Date: 2012-04-03 23:16:17
Slug: puppet-spisok-ip-adresov-servera-v-template
Tags: puppet, powerdns, templates

Привет, друзья!

Что такое системы автоматизации никому рассказывать, наверно, не нужно.

Я для этих целей использую [Puppet](http://puppetlabs.com/) (кстати, он с
недавих пор даже Windows менеджит!)

Встала недавно передо мной задачка научить кукловода управлять конфигом
PowerDNS.

Кажется - что может быть проще? Делаем модуль, или даже класс с пакетом,
сервисом, темплейтом и вуаля - всё работает.

Но не тут то было. У серверов может быть несколько IP-адресов, и PowerDNS
должен уметь ответить по каждому из них. По этому мы должны это учесть и в
local-address указать список всех нужных IP.

Мне не нужно было ограничивать какие то IP, и нужно было указывать всегда и
все. По этому задача оказалась проще, но не на много.

Как получить список всех адресов сервера в шаблоне и вывести их, разделяя
пробелами?

Мне помог Torbjörn Norinder (спасибо ему, т.к. я в руби не шарю), ответ
которого я нашёл в на страница обсуждения в [Google
Groups](http://groups.google.com/group/puppet-users/msg/439facf1f5b87b7a)

Выглядит шаблонный код так:

    
    <%= scope.to_hash.inject([]) { |acc, (k,v)| acc << v if k =~ /^ipaddress_/; acc }.join(' ') %>
    

Готовый темлейт:

    
    setuid=pdns
    setgid=pdns
    launch=gmysql
    master=no
    slave=yes
    gmysql-host=127.0.0.1
    gmysql-user=pdns
    gmysql-password=pass
    gmysql-dbname=powerdns
    disable-axfr=yes
    lazy-recursion=yes
    local-port=53
    version-string=powerdns
    local-address=<%= scope.to_hash.inject([]) { |acc, (k,v)| acc << v if k =~ /^ipaddress_/; acc }.join(' ') %>
    


Title: Написание модуля puppet
Date: 2012-10-09 10:59:15
Slug: napisanie-modulya-puppet
Tags: puppet, automatiozation

Всем привет! Данная статья ориентирована на специалистов, что уже имеют некий
опыт работы с Puppet и хотели бы упорядочить свои конфигурации в модули,
сделав их более прозрачными в управлении.

  * Что такое Puppet? Puppet - это система автоматизации управления. Основная её отрасль применения
  * упрощение установки поддержки множества серверов и сервисов, храня настройки в едином месте.

  * Что из себя представляет модуль Puppet? Это набор библиотек, классов, шаблонов и простых файлов, что собраны в одном месте, сгруппировавшись по темам (темой может быть сервис или группа сервисов для какой то серверной роли).

  * Где располагаются каталоги модулей Puppet'а? В open source версии Puppet каталогами с модулями являются, как правило в 

/etc/puppet/modules и /usr/share/puppet/modules

Узнать точные пути можно командой

    
    puppet config print modulepath
    

  * Процесс создания модуля Для начала создайте пустой каталог в одной из директорий расположения модулей, что была определена выше. Например, создадим модуль для управления фаерволом в Linux. Сперва создаём сам каталог модуля: 

mkdir -p /etc/puppet/modules/iptables

Теперь создаём единственный необходимый каталог и файл для корректной работы
модуля:

    
    mkdir -p /etc/puppet/modules/iptables/manifests
    touch /etc/puppet/modules/iptables/manifests/init.pp
    

Теперь опишем класс конфигурации Iptables:

    
    sudo tee  /etc/puppet/modules/iptables/manifests/init.pp < root,
            group   => root,
            mode    => 644,
            source  => "puppet:///iptables/rules.v4"
        }
        file { "/etc/iptables/rules.v6":
            owner   => root,
            group   => root,
            mode    => 644,
            source  => "puppet:///iptables/rules.v6"
        }
    }
    EOF
    

Теперь разместим сами файлы, создав для них каталог в модуле:

    
    mkdir -p /etc/puppet/modules/iptables/files
    touch /etc/puppet/modules/iptables/files/rules.v4
    touch /etc/puppet/modules/iptables/files/rules.v6
    

Файлы заполните на своё усмотрение, размещать свой контент в них не в тематике
этой статьи :) Вот и всё! Инклудим нужные классы и всё готово! К примеру,
инклуд Iptables для всех год выглядит так:

    
    # cat /etc/puppet/manifests/site.pp 
    node default {
        include iptables
    }
    

Задавайте свои вопросы в комментариях.


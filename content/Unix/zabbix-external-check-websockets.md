Title: Zabbix external check - Websockets
Date: 2012-09-03 17:13:12
Slug: zabbix-external-check-websockets
Tags: websocket, python, monitoring, zabbix

Вэбсокеты всё глубже входят в нашу жизнь, они открывают занавес быстрому и
интерактивному web-у. И конечно же, их тоже нужно уметь мониторить. Сегодня я
расскажу простое решение для этого. Итак, я использую zabbix, по этому дам
пример решения для него. Сперва установим необходимые модули:

    
    pip install websocket-client
    

Теперь в /etc/zabbix/externalscripts/websocket_check.py поместим следующий
код:

    
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
    18
    
    #!/usr/bin/python
    import sys
    from websocket import create_connection
    
    websocket_path = "/app"
    
    host = sys.argv[1]
    port = sys.argv[2]
    
    try:
            ws = create_connection("ws://%s:%s%s" % (host, port, websocket_path))
            if ws.recv() == 'ping':
                    print 1
            else:
                    print 0
            ws.close()
    except:
            print 0
    

Замените значение websocket_path на своё и добавьте скрипты права на
выполнение:

    
    chmod +x /etc/zabbix/externalscripts/websocket_check.py
    

Обратите внимание, что данный скрипт проверяет ответ от сервера (мой сервер
возвращает "ping", если всё хорошо). Это значение может отличаться. Теперь
добавьте новый Item типа [External check](http://www.zabbix.com/documentation/

2.0/manual/config/items/itemtypes/external) с указанием порта web-сокета:

    
    websocket_check.py["80"]
    

После Вы можете настроить тригер на своё усмотрение. Скрипт возвращает 1 в
случае успешной проверки и 0 в случае проблемы. Вот и всё, приятной работы!


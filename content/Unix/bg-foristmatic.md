Title: Background с цитатами из forismatic.com
Date: 2010-06-29 05:59:00
Slug: bg-foristmatic


forismatic.com - это база, что содержит "вдохновляющие высказывания
человечества". Услышал я о этом сервисе на каком то irc сервере внутри глубин
канала #freebsd (емнип). Собеседник сказал, что
http://ru.forismatic.com/homepage уже давно живёт на его home page в Safari.
Признаюсь - я не отличился от него, узнав о сервисе.

Домашняя страничка в браузере - это, конечно, хорошо. Вот только видеть её
приходится оочень редко (несомненно, кто то найдёт в этом +). Мой выбор -
цитаты на рабочем столе. Сам forismatic.com предоставляет только ПО для win-
систем, зато предоставляет дружественный API. Так что я решил написать пару
строчек кода для этого решения:

    
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
    19
    20
    21
    22
    23
    
    #!/bin/bash
    # Background config
    SIZE="1280x1024"
    FONT_SIZE=24
    BG_COLOR="black"
    TEXT_COLOR="white"
    FONT_PATH="/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
    POSITION="center"
    BG_IMAGE="/home/denni/Picturies/Backgrounds/background.png"
    
    # Forismatic API config
    KEY="457653"
    LANG="ru"
    
    
    API_QUERY="http://api.forismatic.com/api/1.0/?method=getQuote&key=$KEY&format=text&lang=$LANG"
    RESULT=`curl $API_QUERY 2> /dev/null`
    TEXT=`echo $RESULT | awk -F'(' '{print $1}' | sed 's/\. /\.\n/g' | sed 's/, /,\n/g'`
    AUTHOR=`echo $RESULT |awk -F'(' '{print $2}' | tr -d ')'`
    if [ "$AUTHOR" != "" ]; then
        AUTHOR="- $AUTHOR -"
    fi
    convert -size $SIZE -background $BG_COLOR -fill $TEXT_COLOR -font $FONT_PATH -pointsize $FONT_SIZE -gravity $POSITION label:"\" $TEXT\"\\n\\n$AUTHOR" $BG_IMAGE
    

Теперь делаем скрипт исполняемым и добавляем в crontab:

    
    $ chmod +x /home/denni/bin/forismatic_background.sh
    $ crontab -e
    * * * * *  /home/denni/bin/forismatic_background.sh &> /dev/null
    

У меня нету картинки на бекграунде. Если это кому то нужно - милости прошу в

    
    $ man convert
    

Но главное не реализация, а контент, что станет доступным. Лично на меня
многое из прочитанного заинтересовало.

![Gerda 3D](http://yavorovych.com/images/bg-foristmatic/bg.png)


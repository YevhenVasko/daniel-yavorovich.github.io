Title: Notice: Undefined variable: HTTP_SERVER_VARS
Date: 2010-11-01 03:54:14
Slug: notice-undefined-variable-http_server_vars


Пока я не увидел эту ошибку, во время поднятия nginx + php-fpm я потратил
больше 4 часов на поиски причины того, что инклуды в скриптах с абсолютными
путями не работают. Как оказалось - дело было не в инклудах. Просто переменная
HTTP_SERVER_VARS была Undefined :)

Решается эта незадача просто - нужно всё то включить **register_long_arrays**


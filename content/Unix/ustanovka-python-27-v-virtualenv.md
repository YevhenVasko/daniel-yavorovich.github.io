Title: Установка Python-2.7 в virtualenv
Date: 2012-04-09 17:54:29
Slug: ustanovka-python-27-v-virtualenv
Tags: python, virtualenv

Для того, чтобы установить Python версии 2.7 в виртуальном окружении с более
ранней версией интерпритатора нужно выполнить несколько несложных действий:

  1. Посмотрим на список наших окружений
    
    $ lsvirtualenv
    myevn
    test2
    

  2. Перейдём в нужное окружение
    
    workon test2
    

  3. Создам каталог, где разместим исходниники Python-2.7 и перейдём в него:
    
    mkdir ~/.virtualenvs/test2/src/; cd mkdir ~/.virtualenvs/test2/src/
    

  4. Загрузим исходники python
    
    wget http://www.python.org/ftp/python/2.7/Python-2.7.tgz
    

  5. Распакуем их и перейдём в каталог с исходными текстами:
    
    tar xvvf Python-2.7.tgz; cd Python-2.7
    

  6. Конфигурируем Python
    
    ./configure --prefix=$HOME/.virtualenvs/test2/
    

  7. Компиляция
    
    make
    

  8. Установка
    
    make install
    

  9. Загрузка скрипта установки setuptools
    
    wget http://peak.telecommunity.com/dist/ez_setup.py
    

  10. Устнановка инструментов установки
    
    python ez_setup.py
    

  11. Устанавливаем PIP
    
    easy_install pip
    

  12. Проверяем
    
    $ python -V
    Python 2.7
    


Title: Установка s3fs на Ubuntu
Date: 2012-09-07 13:41:50
Slug: ustanovka-s3fs-na-ubuntu
Tags: s3fs, amazon, s3, ubuntu

Привет! s3fs - это fuse-модуль для работы с Amazon s3, как с файловой
системой. Ставится всё предельно просто. Сперва установим необходимые
библиотеки и клиент SVN:

    
    $ sudo aptitude install build-essential libcurl4-openssl-dev libxml2-dev libfuse-dev comerr-dev libfuse2 libidn11-dev libkadm55 libkrb5-dev libldap2-dev libselinux1-dev libsepol1-dev pkg-config fuse-utils subversion autoconf2.13
    

Теперь выполним загрузку s3fs из SVN и установим его:

    
    mkdir -p ~/install/; cd ~/install/
    svn checkout http://s3fs.googlecode.com/svn/trunk/ s3fs-read-only
    cd s3fs-read-only
    autoreconf --install
    ./configure --prefix=/usr
    make
    make install
    

Разрешим доступ к s3 простым пользователям:

    
    echo "user_allow_other" >> /etc/fuse.conf
    

Теперь создаём файл /etc/passwd-s3fs с содержанием по примеру:

    
    bucketName:accessKeyId:secretAccessKey
    

После монтируем bucket:

    
    s3fs backup /backups/ -ouse_cache=/tmp -o url=http://s3-website-eu-west-1.amazonaws.com
    

в "-o url" я указываю url своего бакета. Это значение нужно установить в
зависимости от расположения инстанса. Спаисбо!


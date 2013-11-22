Title: RPM SQLite 3.7.1
Date: 2012-11-03 14:15:45
Slug: rpm-sqlite-371
Tags: fts, sqlite3_load_extension, sqlite, clean

Привет, привет! Сегодня в одном из проектов у моего хорошего приятеля
потребовалось поддержка fts3/fts4 и возможность подключать дополнения(
sqlite3_load_extension()). Многие на моём месте сразу пойду делать "configure;
make; make install". Многие, но не я. Собрать пакет с поддержкой всего этого
добра - задача очень тривиальная. Я использую CentOS 6.3 64-bit, но помимо
пакета выкладываю и spec-файл, что позволит Вам сделать rpm для любой
архитектуры.

spec:

    
    %define realver 3071200
    %define docver 3071200
    %define rpmver 3.7.12
    
    Summary:        Library that implements an embeddable SQL database engine
    Name:           sqlite
    Version:        %{rpmver}
    Release:        2%{?dist}
    License:        Public Domain
    Group:          Applications/Databases
    URL:            http://www.sqlite.org/
    Source0:        sqlite-autoconf-%{realver}.tar.gz
    
    BuildRequires:  ncurses-devel readline-devel glibc-devel
    
    BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
    %description
    SQLite is a C library that implements an SQL database engine. A large
    subset of SQL92 is supported. A complete database is stored in a
    single disk file. The API is designed for convenience and ease of use.
    Applications that link against SQLite can enjoy the power and
    flexibility of an SQL database without the administrative hassles of
    supporting a separate database server.  Version 2 and version 3 binaries
    are named to permit each to be installed on a single host
    
    %package devel
    Summary: Development tools for the sqlite3 embeddable SQL database engine
    Group: Development/Libraries
    Requires: %{name} = %{version}-%{release}
    Requires: pkgconfig
    
    %description devel
    This package contains the header files and development documentation
    for %{name}. If you like to develop programs using %{name}, you will need
    to install %{name}-devel.
    
    %prep
    %setup -n %{name}-autoconf-%{realver}
    
    %build
    export CPPFLAGS="-DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_LOAD_EXTENSION=1"
    %configure
    make
    
    %install
    rm -rf $RPM_BUILD_ROOT
    make install DESTDIR=$RPM_BUILD_ROOT
    
    %clean
    rm -rf $RPM_BUILD_ROOT
    make clean
    
    %files
    %defattr(-, root, root)
    %doc README
    %{_bindir}/sqlite3
    %{_libdir}/*.so.*
    %{_mandir}/man?/*
    
    %files devel
    %defattr(-, root, root)
    %{_includedir}/*.h
    %{_libdir}/*.so
    %{_libdir}/pkgconfig/*.pc
    %{_libdir}/*.a
    %exclude %{_libdir}/*.la
    
    %changelog
    * Sat Nov  3  2012 Daniel Yavorovich - 3.7.12-2
    
    * Thu May 17 2012 Nicola Asuni - 3.7.12-1
    - First version or autoconf.
    

RPMs для CentOS 6.3 - x86_64 во вложении

Искренне желаю Андрею поскорее стабилизироваться и отдыхать в выходные :)


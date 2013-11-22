Title: Очистка кеша файловой системы в Linux
Date: 2012-10-03 14:47:10
Slug: ochistka-kesha-fajlovoj-sistemy-v-linux
Tags: clean, cache, fs

Всё предельно просто. Делаем синк и очищаем все кеши (pagecache, dentrie и
inode)

    
    sync; echo 3 > /proc/sys/vm/drop_caches
    


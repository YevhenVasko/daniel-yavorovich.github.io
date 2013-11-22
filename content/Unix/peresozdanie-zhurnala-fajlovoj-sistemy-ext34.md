Title: Пересоздание журнала файловой системы ext3,4
Date: 2012-09-06 13:36:31
Slug: peresozdanie-zhurnala-fajlovoj-sistemy-ext34
Tags: journal, recreate, ext4, tune2fs, ext3

Нам потребуется выполнить всего лишь 1 команду. Прошу заметить, что ФС во
время этой операции должна быть отмонтирована:

    
    tune2fs -O ^has_journal /dev/md3
    

/dev/md3 в данном случае - блочное устройство с нужной файловой системой.


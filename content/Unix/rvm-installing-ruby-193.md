Title: RVM: Installing Ruby 1.9.3
Date: 2012-03-15 17:08:34
Slug: rvm-installing-ruby-193


Привет! Чтобы поставить ruby-1.9.3 в rvm просто выполняем:

    
    rvm get head
    rvm reload
    rvm install 1.9.3-preview1
    

Проверяем:

    
    rvm list
    
    rvm rubies
    
    => ruby-1.9.2-p290 [ i686 ]
       ruby-1.9.3-preview1 [ i686 ]
    

Для активации нового ruby делаем:

    
    rvm use 1.9.3
    


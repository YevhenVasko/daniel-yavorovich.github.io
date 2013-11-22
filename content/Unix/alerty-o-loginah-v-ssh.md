Title: Алерты о логинах в SSH
Date: 2011-10-19 03:04:08
Slug: alerty-o-loginah-v-ssh


Недавно один из моих серверов был скомпрометирован а следом и 3 других, к
которым основной сервер имел доступ. История не столь интересная, чтобы
описывать её, да и желания нету. Вместо стандартных советов типа "не вешайте
SSH на дефолтный порт, не давайте логинится от рута и ограничивайте доступ к
портам по возможности" (а это очень важные советы, я очень рекомендую им
следовать) хочу предоставить простой скрипт, что будет алертить каждый раз,
когда кто либо будет логинится по SSH к вам на сервер. Возможно, подобные
алерты могут немного раздражать, но нельзя переоценить их надобность. После
установки руткита какую либо информацию вытащить будет сложно, а у Вас,
возможно, будет несколько ценных писем с адресами.

Итак, сам код:

    
        if [ "$SSH_CONNECTION" != "" ]; then
                DATE=date "+%d.%m.%Y %Hh%Mm"
                IP=echo $SSH_CONNECTION | awk '{print $1}'
                REVERSE=dig -x $IP +short
                WHO=$(whois $IP | grep desc | tail -1 | cut -c 17-)
                SERVER_IPS=ip addr | awk '/inet/{print $2}' | tr '\n' ' '
    
    MESSAGE="Subject: [SSH Alert] Connection from $USER on $HOSTNAME (echo $SERVER_IPS | cut -f 3 -d ' ')\n"
    
    MESSAGE=$MESSAGEecho "\nISP        : $WHO \n"
                MESSAGE=$MESSAGEecho "\nHost       : $REVERSE \n"
                MESSAGE=$MESSAGEecho "\nDate       : $DATE \n"
                MESSAGE=$MESSAGEecho "\nServer IPs : $SERVER_IPS \n"
    
    echo -e "$MESSAGE" | sendmail.postfix yavorovich@denni.org
        fi
    

Как видно для работы нужен dig, ip и whois. Так же я использую
sendmail.postfix для отправки сообщений, но это по желанию, так сказать.


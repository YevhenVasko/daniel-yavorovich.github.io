Title: Django - сигналы
Date: 2012-09-05 20:50:16
Slug: django-signaly
Tags: signal, django, webmoney

Доброго времени суток, друзья! Сегодня я расскажу о очень крутой возможности
Django - сигналах. Сперва немного теории. Когда в Django происходит некоторое
событие (к примеру, в модель были записаны данные) Django генерирует signal
(на самом деле - несколько сигналов. Во время иницилизации, перед записью
данных, после записи и т.д.). Эти сигналы можно "ловить" и выполнять любые
действия. Давай разберём работу сигналов на примере. Итак, я установил django-
payment-webmoney (мерчант webmoney) для того, чтобы клиенты могли через
webmoney пополнять свой баланс. Моя задача - выполнять произвольный код после
того, как оплата была подтверждена. Я знаю, что когда оплата выполнения -
django-payment-webmoney фиксирует платёж в моделе Payment. Отлично, сигналы к
ней мы и будем фиксировать. Нас интересует сигнал post_save, и код в конечном
итоге будет выглядеть следующим образом:

    
    from webmoney.models import Payment
    from django.dispatch import receiver
    from django.db.models.signals import post_save
    
    @receiver(post_save, sender=Payment)
    def webmoney_payment_accepted(sender, **kwargs):
        """
        Функция создания транзакции
        при пополнении webmoney
        """
        payment = kwargs['instance']
    
        Transaction.objects.create(
            balance = payment.invoice.user.balance,
            transaction_type = 1,
            cost = payment.amount
        )
    

Как видно из примера - мы "ловим" сигнал, определяем в payment созданный
объект и добавляем транзакцию в нашу модель (дальше эта транзакция похожим
сигналом инкрементирует баланс пльзователя). Вот и всё! Django, спасибо тебе
за твою простоту и доходчивость. Конечно же, по этому вопросу есть
замечательная
[документация](https://docs.djangoproject.com/en/dev/ref/signals/) в
официальном руководстве.


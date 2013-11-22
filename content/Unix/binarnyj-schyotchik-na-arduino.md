Title: Бинарный счётчик на Arduino
Date: 2012-02-05 00:40:21
Slug: binarnyj-schyotchik-na-arduino


Воскресным вечером ко мне пожаловал мой хороший друг. Я показал ему недавно
приобретённую Arduino Mega. Всё, что у нас было - IDE шлейф, несколько метров
витой пары и светодиоды.

Вот то, что из этого получилось:

А вот код, что был реализован:

    
    /*
    Бинарный счётчик от 0 до 127
    */
    
    int start_pin = 2; // Начальный PIN
    int stop_pin  = 8; // Конечный PIN
    
    int leds[7];       // Массив "LED"-дисплея 7 x 1
    
    int bin;           // Временная переменная
    
    void setup() {
      // Установка режимов PIN'ов для "LED"-дисплея  
      for (int i = start_pin; i <= stop_pin; i++) {
        pinMode(i, OUTPUT);
      }
    }
    
    void loop() {
     for (int count=0; count <= 127; count++) {
       bin = count;
    
    for (int i=0; i<7; i++) {
         leds[i] = bin % 2;
         bin /= 2;
       }
    
    for (int i=0; i<7; i++) {
         analogWrite(start_pin+i, 102*leds[i]);
       }
    
    delay(500);
     }
    }
    


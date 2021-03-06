Еще одно тестовое задание. На этот раз на позицию data-инженера. Полный текст задания приведён в конце.

Сразу стоит сказать, что это задание работодатель не принял. С некоторыми его комментариями я бы поспорил, но в целом да - мне не хватило опыта работы с большими наборами данных конкретно на PostgreSQL, так что отказ не был неожиданностью ))).

Для меня задание оказалось непростым. На разработку ушло чуть больше четырёх полных рабочих дней. При этом мне не удалось перенести всю логику работы с данными на сервер, хотя я постарался минимизировать сетевое взаимодействие. Если бы можно было создавать индексы и ограничения для таблиц, тогда, наверное, можно было бы реализовать всю обработку на сервере. Но, как я понял из задания, мы не можем модифицировать базу и можем надежно расчитывать только на таблицы без индексов и ограничений.

Также я немного отступил от задания в том, что скрипты из пунктов 3 и 5 не вызывают скрипты из пунктов 2 и 4 через командную строку, хотя скрипты 2 и 4 позволяют это сделать. Вместо этого весь проект написан в ООП-стиле и скрипты 3 и 5 напрямую обращаются к тем же блокам, что и 2 и 4, но в немного другой логике. И да, я знаю, что в настоящем проекте так делать нехорошо и подобные отступления надо согласовать с тимлидом и архитектором ))) 

**1.**
**Подготовка**

Для работы потребуется python 2.7 с установленным пакетом psycopg2 и сервер PostgreSQL.</br>
Также решение предполагает, что на сервере будет создан пользователь vasya и эта учетная запись будет использоваться для подготовки и тестирования.

На тестовой базе данных нужно запустить скрипты cyclone\_table.sql и cyclone\_history\_table.sql для создания таблиц cyclone и cyclone\_history соответственно.

Затем загрузить в эту базу исходные данные из файла atlantic.csv с помощью скрипта load\_test\_data.sql, не забыв указать действительный путь к файлу atlantic.csv.

**2.**
**Выполнение**

Приложение включает 4 рабочих скрипта:

***OneMonthExtractorApp.py*** - создаёт csv-файлы ТОЛЬКО ЗА указанный месяц в указанном каталоге. Если данных нет, то файл не создаётся.</br>
Параметры:</br>
--host=<host\>: Сервер PostgreSQL (localhost по умолчанию)</br>
--port=<port\>: Порт (5432 поумолчанию)</br>
--database=<database\>: Название БД</br>
--user=<user\>: Пользователь</br>
--password=<password\>: Пароль<br/>
--year=<year\>: Год (текущий по умолчанию)<br/>
--month=<Месяц\>: Месяц (текущий по умолчанию)<br/>
--dir=<dir\>: Каталог (текущий по умолчанию)

Пример:<br/>
`>python OneMonthExtractorApp.py --database=etl --user=vasya --password=PAssw0rd --year=2013 --month=8 --dir=~/cyclones`


***FromMonthExtractorApp.py*** - создаёт csv-файлы начиная НАЧИНАЯ С указанного месяца до текущего в указанном каталоге.</br>

Параметры:<br/>
--host=<host\>: Сервер PostgreSQL (localhost по умолчанию)</br>
--port=<port\>: Порт (5432 поумолчанию)</br>
--database=<database\>: Название БД</br>
--user=<user\>: Пользователь</br>
--password=<password\>: Пароль<br/>
--year=<year\>: Год (текущий по умолчанию)<br/>
--month=<Месяц\>: Месяц (текущий по умолчанию)<br/>
--dir=<dir\>: Каталог (текущий по умолчанию)

Пример:<br/>
`>python OneMonthExtractorApp.py --database=etl --user=vasya --password=PAssw0rd --year=2013 --month=8 --dir=~/cyclones`

***FileLoaderApp.py*** - загружает данные из указанного csv-файла.</br>

Параметры:<br/>
--host=<host\>: Сервер PostgreSQL (localhost по умолчанию)</br>
--port=<port\>: Порт (5432 поумолчанию)</br>
--database=<database\>: Название БД</br>
--user=<user\>: Пользователь</br>
--password=<password\>: Пароль<br/>
--file=<file\>: Файл

Пример:<br/>
`>python FileLoaderApp.py --database=etl --user=vasya --password=PAssw0rd --file=~/cyclones/cylones_20140128.csv`

***DirLoaderApp.py*** - загружает данные из всех csv-файлов в указанном каталоге.</br>

Параметры:<br/>
--host=<host\>: Сервер PostgreSQL (localhost по умолчанию)</br>
--port=<port\>: Порт (5432 поумолчанию)</br>
--database=<database\>: Название БД</br>
--user=<user\>: Пользователь</br>
--password=<password\>: Пароль<br/>
--dir=<dir\>: Каталог

Пример:<br/>
`>python DirLoaderApp.py --database=etl --user=vasya --password=PAssw0rd --dir=~/cyclones`

----------

**Тестовое задание для data-инженера ETL**

Скрипты для задания необходимо выполнить на Python 2.7.x и SQL. Причём в большей мере надо стараться, чтобы логика была написана именно на SQL (в том числе без хранимых процедур).  
В качестве СУБД использовать PostgreSQL.<br/><br/>
1. Загрузить любым способом CSV-файл из https://www.kaggle.com/noaa/hurricane-database#atlantic.csv в PostgreSQL БД в таблицу cyclones. Это просто исходные данные для задания.<br/><br/> 
2. Написать ETL-скрипт генерирующий для указанного месяца CSV-файлы с данными из cyclones. Данные для каждого дня в отдельном файле. Имена файлов должны быть вида cyclones_20140128.csv.

В каждом файле для каждого циклона (из тех для кого есть записи за заданный день) только одна строка с его последним статусом:
ID
date
status — последний статус

Для справки коды статусов:<br/>
TD – Tropical cyclone of tropical depression intensity (< 34 knots)<br/>
TS – Tropical cyclone of tropical storm intensity (34-63 knots)<br/>
HU – Tropical cyclone of hurricane intensity (> 64 knots)<br/>
EX – Extratropical cyclone (of any intensity)<br/>
SD – Subtropical cyclone of subtropical depression intensity (< 34 knots)<br/>
SS – Subtropical cyclone of subtropical storm intensity (> 34 knots)<br/>
LO – A low that is neither a tropical cyclone, a subtropical cyclone, nor an extratropical cyclone (of any intensity)<br/>
WV – Tropical Wave (of any intensity)<br/>
DB – Disturbance (of any intensity)<br/><br/>
3. Сгенерировать при помощи полученного в п.2 скрипта файлы для date >= 2013-01-01<br/><br/>
4. Написать второй ETL-скрипт, который будет уметь принимать один файл вида cyclones\_20140128.csv и формировать историю статусов циклонов в таблице cyclones_history в PostgreSQL. 

Колонки cyclones\_history:</br>
date\_from</br>
date_end</br>
id</br>
status<br/><br/>
Принцип — значение status отличное от прежнего (а также отсутствие записи/статуса) означает начало нового периода (прежний период «закрывается» вчерашней датой).

Предполагается запуск скрипта для загрузки данных последовательно день за днем (в production просто каждый день). Не бывает повторной загрузки за какой-то предыдущий загруженный день. Но надо учесть возможность повторной загрузки файла за последний день (данные в файле изменились).<br/><br/>
5. Загрузить историю из файлов полученных в п.3

В качестве результатов для проверки задания необходимо предоставить скрипты реализованные в п.2 и в п.4, а также детальная информация (команды, скрипты и пр.) выполнения п.3 и п.5.

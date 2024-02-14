# API для получения погоды

* можно запустить в docker
* можно запустить локально

## Локально
1. Создайте файл .env и заполните его данными из .env.example
2. Регистрируем api ключ для яндекса:
   * Переходим по ссылке:https://developer.tech.yandex.ru/services
   * Жмем connect apis и ищем и нажимаем на: ``` Yandex.Weather API```
   * Выбираем тестовый тариф и получаем api ключ. Копируем его в .env
3. Скачиваем зависимости либо через poetry либо через pip
4. ### virtualenv
    * ``` python -m venv venv```
    * ``` source venv/bin/activate ```
    * ``` pip install -r requirements.txt```
5. ### poetry
    * ``` poetry init ```
    * ``` poetry install ```

6. Активируем миграции - ``` make migrate ```
6. Загружаем фикстуры: ```make city-load ```
7. Запускаем с помощью make команды - ``` make runl```

## Docker
1. В директории .envs создаем директорию - local
2. Заполняем свой Yandex APi ключ в файле .django и копируем 2 файла:
    * .django
    * .postgres
в local директорию
3. Запускаем с помощью make команды - ``` make run ```

### Структура
**services** - содержит бизнес логику
**selectors** - достаем данные из бд, кэша
**views** - 2 views:
1. CityGetApiViewByFirstChar -  для получения списка городов начинающихся на какую-то букву.
2. WeatherGetApiView - Получение погоды.

### Структура запросов
1. `````GET  /cities?char=first_char````` Должен быть передан query параметр char иначе ошибка.
 
2. ``` GET   /weather?city=city_name``` Должен быть передан query параметр city, иначе ошибка.

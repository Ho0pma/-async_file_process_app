Разработал API, используя Django REST Framework (drf), который позволяет загружать файлы в базу данных и, впоследствии, обрабатывать их с помощью обработчика задач Celery через брокер сообщений redis. 

В проекте реализованы:
  - модель File, которая представляет загруженные файлы
  - сериализатор для модели File
  - эндпоинты: 
      1) ../files/ - возвращает список всех загруженных файлов. Есть возможность просматривать каждую запись отдельно переходя по ../files/1
      2) ../files/upload/  - принимает POST-запросы, добавляет файлы в бд и после, с помощью асинхронного бэкенда выполняет таски связанные с обработкой файла. 
  - написан валидатор, проверяющий формат и размер поступающего файла
  - написаны тесты, использовал pytest/coverage

Проект развернут на виртуальном сервере (VPS) с помощью технологии Docker (docker-compose):
  - контейнер с django запускается на сервере с помощью gunicorn
  - перед запуском выполняются миграции, собирается статика и создается суперпользователь
  - для каждого сервиса настроен healthcheck
  - для домена настроен SSL протокол (работает подключение по https)
  - для проксирования запросов к gunicorn и обработки SSL-сертификата использовал nginx

Посмотреть работу проекта можно перейдя по домену: www.hoopmaserver.ru

стек: [python, Django, Django REST Framework, Postgres, redis, celery, Docker, docker-compose, gunicorn, nginx, pytest, coverage, shell]

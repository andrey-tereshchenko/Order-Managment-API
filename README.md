# Order-Managment-API
### Описание запуска проекта
1. Запуск будем делать с помощью docker-compose (Установите docker, docker-compose)
2. Скачайте данный репозиторий
3. Убедитесь, что у вас локально остановлен redis-server
4. Откройте терминал в директории проекта для сборки образа и запуска контейнера(для ubuntu перед командой docker-compose писать sudo):
```
sudo docker-compose up -d
```
5. После запуска создадим суперпользователя(username=admin, password=admin, group=1) для этого выполняем:
```
sudo docker-compose exec web ./manage.py createsuperuser
```
6. Далее открываем postman collection: https://www.getpostman.com/collections/a614e353473671f8ba3c
7. Устанавливаем enviroment файл  OrderApiEnviroment.postman_environment.json для полученой колекции
8. Открываем в коллекции папку 'User Auth and CRUD' и выполняем запрос(Admin User Get Token) для получения JWT токена для admin пользователя.
9. В enviroment меняем переменную admin_token  на полученый в предыдущем запросе 'access'
10. Выполняем запросы по созданию пользователей: Кассира, Продавца-консультанта и Бухгалтера
11. Аналогично получаем JWT токены для созданых пользователей и меняем соответствующие переменые в enviroment
12. Выполняем остальные запросы по товарам, заказам и чекам
13. Механизм начисления скидок на товары, реализован с помощью переодических(раз в день) задач Celery

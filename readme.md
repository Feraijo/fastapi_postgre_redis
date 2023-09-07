## Тестовая задача 

Апишка для работы с документами. Fast api асинхронные еп. 
Документ - дата создания, дата обновления, тип документа, бинарное содержимое, кто создал, наименование файла и т.д.
Пользователь - имя, логин
Типы документов - наименование типа, формат (можно по расширению файла)
Для работы пользователь должен авторизоваться в системе. Время жизни сессии пользователя прописывается в конфиге.
Сессию хранить в redis
Пользователь может загрузить документ, получить документ, удалить документ, обновить существующий документ
Данные хранятся в постгрес
Пользователь не может получать чужие документы
Пользователь может отфильтровать список документов по типу
Если пользователь попытается загрузить неподдерживаемый тип документа - ошибка (проверять просто по расширению)
придерживаться REST

Запустить сервис через Docker: `docker compose up`

`http://localhost:5000/docs`

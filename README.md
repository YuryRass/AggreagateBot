# Тестовое задание Python developer

Стек: Python3, Asyncio, MongoDB, любая асинхронная библиотека для телеграм бота


## Описание задачи:

Задачей в рамках тестового задания является написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам.

В [BSON-файле](./sample_collection.bson) находится коллекция со статистическими данными, которую необходимо использовать при выполнении задания.


На обычном языке пример задачи выглядит следующим образом: “Необходимо посчитать суммы всех выплат с `{28.02.2022}` по `{31.03.2022}`, единица группировки - `{день}`”.


Алгоритм должен принимать на вход:

Дату и время старта агрегации в ISO формате (далее `dt_from`)
Дату и время окончания агрегации в ISO формате (далее `dt_upto`)
Тип агрегации (далее `group_type`). Типы агрегации могут быть следующие: `hour`, `day`, `month`. То есть группировка всех данных за час, день, неделю, месяц.

Пример входных данных:

```json
{

"dt_from":"2022-09-01T00:00:00",

"dt_upto":"2022-12-31T23:59:00",

"group_type":"month"

}
```


Комментарий к входным данным: вам необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, тип агрегации по месяцу

На выходе ваш алгоритм формирует ответ содержащий:

Агрегированный массив данных (далее dataset)
Подписи к значениям агрегированного массива данных в ISO формате (далее labels)

Пример ответа:

```json
{
    "dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]
}
```


Комментарий к ответу: в нулевом элементе датасета содержится сумма всех выплат за сентябрь, в первом элементе сумма всех выплат за октябрь и т.д. В лейблах подписи соответственно элементам датасета.

## Запуск программы

```bash
docker compose up --build
```
При этом, перед запуском программы на хосте необходимо проинициализировать БД, используя следующую команду (в корне проекта):
```bash
mongorestore --host localhost --port 27000 --username root --password pass  sample_collection.bson
```
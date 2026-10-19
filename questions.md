**Задание 1. Разбор ТЗ**

| Сущность | Инварианты | Операции |
| :---: | --- | :---: |
| Task | Immutable<br>id (str, UUID4) != null<br>1 <= title (str) <= 200<br>status ∈ {"todo", "in_progress", "done"}<br>created_at (datetime, UTC, timezone-aware) != null<br>tags ∈ tags_list<br>1 <= priority (int) <= 5 | create, read |
| TaskFilter | по статусу, по тегу, по минимальному приоритету; фильтры комбинируются по «И» | create |
| Storage | контракт через typing.Protocol, уникальные айди задач | save(task), get(task_id), delete(task_id), list_all(filter=None) |
| InMemoryRepository | соблюдает контракт Storage, хранит в оперативной памяти | save, get, delete, list_all |
| JsonFileRepository | соблюдает контракт Storage, хранит в json | save, get, delete, list_all |

TaskNotFound - ошибка предметной области
DuplicateTaskId - ошибка предметной области
StorageError - ошибка инфраструктуры

**Задание 3. Решение «ABC vs Protocol». Письменно ответить на 4 вопроса:**
1) Кто пишет реализации контракта: мы сами (внутренние бэкенды) или внешние разработчики?
   Наши внутренние бэкенды (InMemoryRepository, JsonFileRepository) мы пишем сами, сторонние пользовательские - внешние разработчики.

2) Нужна ли нам общая реализация в базовом классе (шаблонный метод)?
   Не нужна, поскольку мы используем Protocol для возможности подключения пользовательских бэкендов.

3) Нужна ли проверка isinstance(x, BaseRepository) в рантайме?
   Не нужна. Мы используем Protocol, классы не будут наследоваться от BaseRepository. Вместо этого программа сама выдаст ошибку в момент вызова конкретного метода, если у объекта его не окажется (Duck Typing)

4) Должен ли внешний бэкенд тянуть импорт нашей библиотеки, чтобы считаться валидным?
   Не должен (т.к. используем typing.Protocol)

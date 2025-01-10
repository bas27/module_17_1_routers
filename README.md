# Модуль 17. Библиотека для работы с ресурсами 2.1

1. Структура проекта. Маршруты и модели Pydantic.
2. Модели SQLALchemy. Отношения между таблицами.
3. Миграции. Библиотека alembic.\
Установка: <code python>pip install alembic</code>
<br>
Инициализация:
<code python>alembic init app/migrations</code>
<br>
Добавим адрес базы данных <code python>sqlite:///taskmanager.db</code> в alembic.ini
<br>
4. В env.py импортируем модели Base, User и Task. Целевой Base.metadata\
<code python>
from app.backend.db import Base\
from app.models.user import User\
from app.models.task import Task\
target_metadata = Base.metadata
</code>
5. Cгенерируем первую миграцию при помощи <code python>alembic revision --autogenerate -m "Initial migration"</code>
6. Выполним команду\
<code python>alembic upgrade head</code>\
, которая позволит применить последнюю миграцию и создать таблицы User, Task и запись текущей версии миграции

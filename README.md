## Установка и запуск проекта

1. **Клонирование репозитория:**
    ```bash
    git clone https://github.com/nazarijbeketovv/tech_assignment
    cd tech_assignment
    ```
2. **Создание и активация виртуального окружения:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux и MacOS
    venv\Scripts\activate  # для Windows
    poetry shell # с помощью poetry
    ```

3. **Установка зависимостей, применение миграций::**
   ```bash
    pip install -r requirements.txt; ./manage.py migrate # с помощью pip
    poetry update; ./manage.py migrate # с помощью poetry
    ```

## Структура проекта:
```bash
    .
├── LICENSE.txt
├── README.md
├── apps
│   ├── task_1
│   │   ├── models
│   │   │   └── player.py          
│   │   ├── tests
│   │   │   └── test_models.py      
│   ├── task_2
│   │   ├── models
│   │   │   └── game.py             
│   │   ├── services
│   │   │   └── game_logic.py     
│   │   ├── tests
│   │   │   ├── test_csv_upload.py  
│   │   │   └── test_game_logic.py  
├── config
│   ├── settings
│   │   ├── base.py                 
│   │   ├── dev.py                 
│   │   └── prod.py                 
├── manage.py
├── requirements.txt
└── static
    ├── css
    ├── images
    └── js
```

## Модели

Модели проекта находятся в следующих файлах:

- **Task 1**:
  - `apps/task_1/models/player.py` — 1-ая таска
  
- **Task 2**:
  - `apps/task_2/models/game.py` — 2-ая таска

## Тесты

Тесты для моделей и сервисов проекта находятся в:

- **Task 1**: `apps/task_1/tests/test_models.py`
- **Task 2**:
  - `apps/task_2/tests/test_csv_upload.py`
  - `apps/task_2/tests/test_game_logic.py`

Запуск тестов:

```bash
./manage.py test app
```

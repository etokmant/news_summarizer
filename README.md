# Russian News Summarizer

## О проекте

Cистема автоматической суммаризации русскоязычных новостей, разработанная в рамках курса "Методы анализа данных и машинного обучения". Проект демонстрирует полный цикл разработки ML-приложения.

## Ключевые особенности
- Автоматическая суммаризация новостных текстов
- REST API с кастомизированной OpenAPI документацией
- Веб-интерфейс на Streamlit
- Docker-контейнеризация
- Оптимизация модели с помощью квантизации

## Структура проекта

### Корневая директория

| Файл | Назначение | Технологии |
|------|------------|------------|
| `streamlit_app.py` | Веб-интерфейс для суммаризации новостей | Streamlit, Requests |
| `requirements-streamlit.txt` | Зависимости для веб-интерфейса | Python packages |
| `README.md` | Основная документация проекта | Markdown |

### Директория `api/` - REST API сервер

| Файл | Содержимое | Назначение |
|------|------------|------------|
| `main.py` | FastAPI приложение с эндпоинтами | Обработка HTTP запросов, суммаризация |
| `requirements.txt` | fastapi, uvicorn, transformers, torch | Зависимости для работы API |

### Директория `docker/` - Контейнеризация

| Файл | Конфигурация | Назначение |
|------|-------------|------------|
| `Dockerfile` | Многоступенчатая сборка образа | Создание Docker-образа API |
| `docker-compose.yml` | Настройка сервисов и сетей | Оркестрация контейнеров |

### Директория `docs/` - Документация

| Файл | Содержимое | Назначение |
|------|------------|------------|
| `index.html` | HTML/CSS страница | Статический сайт проекта на GitHub Pages |
## Старт

### Предварительные требования
- Python 3.10 или новее
- Docker и Docker Compose (рекомендуется)
- Git (для клонирования репозитория)

### Способ 1: Запуск через Docker

#### Клонируйте репозиторий:
```bash
git clone https://github.com/etokmant/news_summarizer.git
cd news_summarizer
```

#### Запустите контейнер с API:

```bash
docker-compose -f docker/docker-compose.yml up --build
```

#### API будет доступен по адресам:

Основной URL: http://localhost:8000

Документация API: http://localhost:8000/docs

OpenAPI схема: http://localhost:8000/openapi.json

#### В отдельном терминале запустите веб-интерфейс:

```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

Веб-интерфейс будет доступен по адресу: http://localhost:8501

### Способ 2: Локальный запуск 

#### Установите зависимости для API:

```bash
pip install -r api/requirements.txt
```

#### Запустите API сервер:

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Установите зависимости для веб-интерфейсa:

```bash
pip install -r requirements-streamlit.txt
```

Запустите веб-интерфейс:

```bash
streamlit run streamlit_app.py
```

## Использование API

* GET / — информация о сервисе

* GET /health — проверка состояния сервиса

* GET /docs — интерактивная документация API

* POST /summarize — основная точка суммаризации

**Пример запроса через cURL**

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Центральный банк России повысил ключевую ставку на 1 процентный пункт до 8.5% годовых. Это решение было принято на заседании совета директоров Банка России.",
    "max_length": 100
  }'
  ```

**Пример ответа API**

```json
{
  "summary": "Центробанк России повысил ключевую ставку до 8.5%.",
  "original_length": 150,
  "summary_length": 40,
  "compression_ratio": 3.75,
  "processing_time": 1.234,
  "model_used": "rut5_base_sum_gazeta",
  "timestamp": "2024-01-28 14:30:45"
}
```

## Метрики качества

### Производительность модели

* ROUGE-1: 0.85

* BLEU: 0.54

* Время обработки: ~1.5 сек на текст

* Коэффициент сжатия: 3-5x

#### Оптимизация модели

* Квантизация: сжатие модели в 10.58 раз

* Размер модели после оптимизации: 88 MB

* Ускорение инференса: до 30%

## Используемые технологии

### Основные технологии

* FastAPI — фреймворк для API

* Streamlit — фреймворк для веб-интерфейсов

* Transformers — библиотека для NLP моделей

* PyTorch — фреймворк для глубокого обучения

* Docker — контейнеризация приложения

### Модель машинного обучения

* Базовая модель: IlyaGusev/rut5_base_sum_gazeta

* Архитектура: T5 (Text-to-Text Transfer Transformer)

* Язык: Русский

* Задача: Суммаризация новостных текстов

### ML-пайплайн

1. Сбор данных
    * Парсинг новостей из Telegram-каналов

    * Очистка и предобработка текстов

    * Создание датасета для обучения

2. Подготовка данных

    * Токенизация текстов

    * Создание референс-суммаризаций

    * Разделение на train/validation/test

3. Обучение модели

    * Дообучение предобученной модели

    * Fine-tuning на специфичных данных

    * Оптимизация гиперпараметров

4. Оценка качества

    * Расчет метрик ROUGE и BLEU

    * Сравнение с baseline-моделями

    * Качественный анализ результатов

5. Деплой и оптимизация

    * Создание REST API

    * Разработка веб-интерфейса

    * Контейнеризация приложения

    * Квантизация модели

## Примеры использования

### Через веб-интерфейс

1. Откройте http://localhost:8501

2. Введите текст новости в поле ввода

3. Настройте параметры суммаризации

4. Нажмите "Суммаризировать"

5. Получите результат с метриками качества

### Через API

```python
import requests

api_url = "http://localhost:8000/summarize"
text = "Ваш новостной текст..."

response = requests.post(api_url, json={"text": text, "max_length": 100})

if response.status_code == 200:
    result = response.json()
    print(f"Суммаризация: {result['summary']}")
    print(f"Коэффициент сжатия: {result['compression_ratio']}x")
```

### Через командную строку

```bash
python -c "
import requests
response = requests.post('http://localhost:8000/summarize', 
                        json={'text': 'Текст новости...', 'max_length': 80})
print(response.json()['summary'])
"
```

## Реализация

### Кастомизация OpenAPI документации

```python
def custom_openapi():
    # Кастомизированная схема OpenAPI
    openapi_schema["info"]["contact"] = {
        "name": "Поддержка API",
        "email": "support@example.com"
    }
    return openapi_schema

app.openapi = custom_openapi
```

### Docker конфигурация

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY api/requirements.txt .
RUN pip install -r requirements.txt
COPY api/ .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Оптимизация модели

```python
# Динамическая квантизация модели
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
Структура данных
Входные данные для API
json
{
  "text": "строка, минимум 50 символов, максимум 5000 символов",
  "max_length": "целое число, от 30 до 300, опционально (по умолчанию 100)"
}
```

### Входные данные для API

```json
{
  "summary": "строка, результат суммаризации",
  "original_length": "целое число, длина исходного текста",
  "summary_length": "целое число, длина суммаризации",
  "compression_ratio": "число с плавающей точкой, коэффициент сжатия",
  "processing_time": "число с плавающей точкой, время обработки в секундах",
  "model_used": "строка, название использованной модели",
  "timestamp": "строка, временная метка в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
}
```

## Тестирование

### Проверка работоспособности API

```bash
# Проверка health-check
curl http://localhost:8000/health

# Тестовая суммаризация
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовый текст для проверки работы API.", "max_length": 50}'
  ```

### Проверка веб-интерфейса

1. Откройте http://localhost:8501

2. Введите тестовый текст

3. Проверьте корректность отображения результатов

## Разработка

### Установка для разработки

```bash
# Клонирование репозитория
git clone https://github.com/ваш-username/news-summarizer.git
cd news_summarizer

# Установка зависимостей для разработки
pip install -r api/requirements.txt
pip install -r requirements-streamlit.txt
pip install black flake8 pytest  # инструменты разработки
```

### Форматирование кода

```bash
# Автоматическое форматирование
black api/ streamlit_app.py

# Проверка стиля кода
flake8 api/ streamlit_app.py
```

### Создание новой функциональности

```bash
# Создание feature-ветки
git checkout -b feature/new-functionality

# Внесение изменений
# ... разработка ...

# Коммит изменений
git add .
git commit -m "Добавлена новая функциональность"

# Отправка в репозиторий
git push origin feature/new-functionality
```

## Контакты

**Автор:** Токманцева Елена  

**GitHub:** [@etokmant](https://github.com/etokmant)  

**Проект:** [news_summarizer](https://github.com/etokmant/news_summarizer)

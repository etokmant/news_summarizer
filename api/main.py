# Основной файл API для суммаризации новостей

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import torch
from transformers import pipeline
import time
from datetime import datetime

# Создаем приложение FastAPI
app = FastAPI(
    title = "Russian News Summarizer API",
    version = "1.0.0",
    description = "API для автоматической суммаризации русскоязычных новостей",
)

# Модель для входных данных запроса
class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length = 50,
        max_length = 5000,
        example = "Россия запустила новую ракету в космос. Это важное достижение.",
        description = "Текст новости для суммаризации"
    )
    max_length: Optional[int] = Field(
        100,
        ge = 30,
        le = 300,
        description = "Максимальная длина суммаризации в символах"
    )

# Модель для выходных данных ответа
class SummarizeResponse(BaseModel):
    summary: str = Field(..., description = "Результат суммаризации")
    original_length: int = Field(..., description = "Длина исходного текста")
    summary_length: int = Field(..., description = "Длина суммаризации")
    compression_ratio: float = Field(..., description = "Коэффициент сжатия")
    processing_time: float = Field(..., description = "Время обработки в секундах")
    model_used: str = Field(..., description = "Использованная модель")
    timestamp: str = Field(..., description = "Временная метка")

# Глобальная переменная для модели
summarizer = None

def custom_openapi():
  
    # Если схема уже создана, возвращаем ее
    if app.openapi_schema:
        return app.openapi_schema
    
    # Получаем базовую схему
    openapi_schema = get_openapi(
        title = app.title,
        version = app.version,
        description = app.description,
        routes = app.routes,
    )
    
    # Добавляем контактную информацию
    openapi_schema["info"]["contact"] = {
        "name": "Поддержка API",
        "email": "support@example.com",
        "url": "https://github.com/ваш-username/news-summarizer",
    }
    
    # Добавляем информацию о лицензии
    openapi_schema["info"]["license"] = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
    
    # Сохраняем кастомизированную схему
    app.openapi_schema = openapi_schema
    
    return openapi_schema

# Применяем кастомизированную схему к приложению
app.openapi = custom_openapi

@app.on_event("startup")
async def startup_event():
    # Загрузка модели при запуске приложения. Выполняется один раз при старте сервера.
    
    global summarizer
    
    print("Начинаем загрузку модели...")
    
    try:
        # Определяем устройство для вычислений
        device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU" if device == 0 else "CPU"
        
        print(f"Используемое устройство: {device_name}")
        
        # Загружаем модель суммаризации
        summarizer = pipeline(
            "summarization",
            model = "IlyaGusev/rut5_base_sum_gazeta",
            device = device,
            framework = "pt"
        )
        
        print("Модель успешно загружена")
        
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")
        # В случае ошибки оставляем summarizer как None

@app.get("/")
async def root():
    # Корневой эндпоинт API. Возвращает основную информацию о сервисе.
    
    return {
        "message": "Russian News Summarizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }

@app.get("/health")
async def health_check():
    # Эндпоинт для проверки состояния сервиса. Используется для мониторинга доступности API.
    
    return {
        "status": "healthy" if summarizer is not None else "unhealthy",
        "model_loaded": summarizer is not None,
        "timestamp": datetime.now().isoformat(),
    }

@app.post("/summarize", response_model = SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """ 
    Основной эндпоинт для суммаризации текста. 
    Принимает текст новости и возвращает краткое содержание.
    
    Args:
        request (SummarizeRequest): Объект запроса с текстом и параметрами
        
    Returns:
        SummarizeResponse: Объект ответа с результатом суммаризации
        
    Raises:
        HTTPException: Если модель не загружена или произошла ошибка
    """
    
    # Проверяем, загружена ли модель
    if summarizer is None:
        raise HTTPException(
            status_code = 503,
            detail = "Модель не загружена. Сервис временно недоступен."
        )
    
    # Засекаем время начала обработки
    start_time = time.time()
    
    try:
        # Выполняем суммаризацию
        result = summarizer(
            request.text,
            max_length = min(100, request.max_length // 3),  # Преобразуем символы в слова
            min_length = 20,
            do_sample = False,
        )
        
        # Получаем результат
        summary = result[0]["summary_text"]
        
        # Вычисляем время обработки
        processing_time = time.time() - start_time
        
        # Вычисляем метрики
        original_length = len(request.text)
        summary_length = len(summary)
        compression_ratio = original_length / max(summary_length, 1)
        
        # Формируем ответ
        response = SummarizeResponse(
            summary = summary,
            original_length = original_length,
            summary_length = summary_length,
            compression_ratio = round(compression_ratio, 2),
            processing_time = round(processing_time, 3),
            model_used = "rut5_base_sum_gazeta",
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        
        return response
        
    except Exception as e:
        # Обрабатываем ошибки при суммаризации
        raise HTTPException(
            status_code = 500,
            detail = f"Ошибка при обработке текста: {str(e)}"
        )

# Точка входа для запуска сервера
if __name__ == "__main__":
    # Запуск сервера разработки при прямом выполнении файла. В продакшене используется uvicorn через командную строку.
    
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8000,
        log_level = "info"
    )
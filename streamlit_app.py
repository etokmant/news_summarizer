# Веб-интерфейс для суммаризации новостей на основе Streamlit

# Импорт необходимых библиотек
import streamlit as st
import requests
import json
from datetime import datetime

# Настройка конфигурации страницы
st.set_page_config(
    page_title = "Russian News Summarizer",
    page_icon = "📰",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Применение пользовательских стилей CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Основная функция приложения Streamlit. Организует логику взаимодействия с пользователем.
    
    # Отображение заголовка приложения
    st.markdown('<h1 class = "main-header"> Russian News Summarizer</h1>', unsafe_allow_html = True)
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("Настройки")
        
        # Поле для ввода URL API
        api_url = st.text_input(
            "URL API сервера",
            value="http://localhost:8000",
            help="Адрес развернутого API сервера. По умолчанию localhost."
        )
        
        # Поле для выбора длины суммаризации
        max_length = st.slider(
            "Длина суммаризации (символов)",
            min_value = 50,
            max_value = 300,
            value = 120,
            step = 10,
            help = "Желаемая длина итогового текста"
        )
        
        # Кнопка для проверки подключения к API
        if st.button("Проверить подключение", use_container_width=True):
            check_connection(api_url)
    
    # Основная область ввода текста
    st.subheader("Введите текст для суммаризации")
    
    # Текстовое поле для ввода новости
    text_input = st.text_area(
        "Текст новости",
        height = 200,
        placeholder = """Пример: Центральный банк России повысил ключевую ставку на 1 процентный пункт до 8.5% годовых. Это решение было принято на заседании совета директоров Банка России. Основной причиной повышения ставки стал рост инфляционных ожиданий.""",
        help = "Введите текст новости на русском языке (от 50 до 5000 символов)"
    )
    
    # Отображение статистики текста
    if text_input:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Символов", len(text_input))
        
        with col2:
            st.metric("Слов", len(text_input.split()))
        
        with col3:
            sentences = text_input.count('.') + text_input.count('!') + text_input.count('?')
            st.metric("Предложений", sentences)
    
    # Кнопка для запуска суммаризации
    if st.button("Суммаризировать", type = "primary", use_container_width = True):
        # Проверка минимальной длины текста
        if not text_input or len(text_input) < 50:
            st.warning("Пожалуйста, введите текст длиной не менее 50 символов")
        else:
            # Вызов функции для выполнения суммаризации
            perform_summarization(api_url, text_input, max_length)

def check_connection(api_url):
    """
    Проверка доступности API сервера.
    
    Args:
        api_url (str): URL адрес API сервера
    """
    try:
        # Отправка GET запроса на эндпоинт health
        response = requests.get(f"{api_url}/health", timeout = 5)
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"API доступен")
            st.info(f"Модель загружена: {data.get('model_loaded', False)}")
        else:
            st.error(f"API недоступен. Код ошибки: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Не удалось подключиться к API. Проверьте URL и убедитесь, что сервер запущен.")
    except Exception as e:
        st.error(f"Ошибка подключения: {str(e)[:100]}")

def perform_summarization(api_url, text, max_length):
    """
    Выполнение запроса на суммаризацию текста через API.
    
    Args:
        api_url (str): URL адрес API сервера
        text (str): Текст для суммаризации
        max_length (int): Максимальная длина результата
    """
    # Отображение индикатора выполнения
    with st.spinner("Выполняется суммаризация текста..."):
        try:
            # Подготовка данных для запроса
            payload = {
                "text": text,
                "max_length": max_length
            }
            
            # Отправка POST запроса на эндпоинт summarize
            response = requests.post(
                f"{api_url}/summarize",
                json = payload,
                timeout = 30 # Таймаут 30 секунд
            )
            
            # Обработка успешного ответа
            if response.status_code == 200:
                result = response.json()
                
                # Отображение результата в стилизованном блоке
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("Результат суммаризации")
                st.write(result['summary'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Отображение метрик в колонках
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Коэффициент сжатия",
                        f"{result['compression_ratio']:.1f}x"
                    )
                
                with col2:
                    st.metric(
                        "Время обработки",
                        f"{result['processing_time']:.2f}с"
                    )
                
                with col3:
                    compression_percent = 100 - (100 / result['compression_ratio'])
                    st.metric(
                        "Сокращение текста",
                        f"{compression_percent:.0f}%"
                    )
                
                with col4:
                    st.metric(
                        "Использованная модель",
                        result['model_used'].split('/')[-1][:10]
                    )
                
                # Дополнительная информация в раскрывающемся блоке
                with st.expander("Детальная информация"):
                    st.json(result)
            
            # Обработка ошибок API
            elif response.status_code == 503:
                st.error("Модель не загружена. Дождитесь завершения загрузки или проверьте сервер.")
            else:
                st.error(f"Ошибка API: {response.status_code}")
                st.code(response.text[:200])
                
        # Обработка исключения при таймауте
        except requests.exceptions.Timeout:
            st.error("Таймаут запроса. Возможно, модель еще загружается или текст слишком большой.")
        
        # Обработка других исключений
        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)[:100]}")

# Запуск основного приложения при выполнении файла
if __name__ == "__main__":
    main()
import gradio as gr
from ai_personality_project.ai_core import AICore
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация AI
ai_core = AICore()

def initialize_ai():
    """Инициализация AI компонентов"""
    try:
        ai_core.initialize()
        logger.info("✅ AI Core initialized successfully for HF Spaces")
        return True
    except Exception as e:
        logger.error(f"❌ AI Core initialization failed: {e}")
        return False

def chat_interface(message, history, persona_id):
    """Интерфейс чата для Gradio"""
    try:
        if not ai_core._initialized:
            if not initialize_ai():
                return "Система временно недоступна. Попробуйте позже."
        
        result = ai_core.process_interaction(message, int(persona_id))
        
        if result['success']:
            response = result['response']
            emotion = result.get('emotion_analysis', {}).get('dominant_emotion', 'neutral')
            return f"{response} [Эмоция: {emotion}]"
        else:
            return f"Ошибка: {result.get('error', 'Неизвестная ошибка')}"
            
    except Exception as e:
        logger.error(f"Error in chat interface: {e}")
        return "Произошла ошибка при обработке запроса"

def create_hf_interface():
    """Создание интерфейса для Hugging Face"""
    with gr.Blocks(title="🎭 AI Personality Project", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎭 AI Personality Project
        **ИИ с человеческой личностью, эмоциями и характером**
        
        Выберите личность и начните общение!
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                persona_id = gr.Dropdown(
                    choices=[
                        ("1 - Дружелюбный помощник 🎯", "1"),
                        ("2 - Профессиональный советник 💼", "2")
                    ],
                    label="👤 Выберите личность",
                    value="1",
                    interactive=True
                )
                
                gr.Markdown("""
                ### 📋 Описание личностей:
                - **Дружелюбный помощник**: Теплый, поддерживающий, эмоциональный
                - **Профессиональный советник**: Сдержанный, аналитичный, формальный
                """)
            
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="💬 Диалог с ИИ",
                    height=400,
                    show_copy_button=True
                )
                
                msg = gr.Textbox(
                    label="✍️ Ваше сообщение",
                    placeholder="Введите ваше сообщение здесь...",
                    lines=2,
                    max_lines=5
                )
                
                with gr.Row():
                    submit_btn = gr.Button("📤 Отправить", variant="primary")
                    clear_btn = gr.Button("🗑️ Очистить чат", variant="secondary")
        
        def respond(message, chat_history, persona):
            if not message.strip():
                return "", chat_history
                
            bot_message = chat_interface(message, chat_history, persona)
            chat_history.append((message, bot_message))
            return "", chat_history
        
        # Обработчики событий
        msg.submit(respond, [msg, chatbot, persona_id], [msg, chatbot])
        submit_btn.click(respond, [msg, chatbot, persona_id], [msg, chatbot])
        clear_btn.click(lambda: None, None, chatbot, queue=False)
    
    return demo

# Инициализация при запуске
initialize_ai()

# Создание приложения
app = create_hf_interface()

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860)),
        share=False
    )
from flask import Flask, jsonify

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5007 # Порт для Сервиса Инструкций

# --- 1. Встроенное хранилище данных ---
instructions = [
    {
        "id": 1,
        "title": "Правила оформления курсовых работ",
        "description": "Подробная инструкция по структуре и требованиям к оформлению.",
        "file_url": "https://university.example.com/docs/kurs.pdf",
        "category": "Студент"
    },
    {
        "id": 2,
        "title": "График отчетности преподавателей",
        "description": "Сроки сдачи отчетности по кафедрам на 2026 год.",
        "file_url": "https://university.example.com/docs/reports.pdf",
        "category": "Преподаватель"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /instruction - Получить список всех инструкций
# Соответствует UC-5 
@app.route('/instruction', methods=['GET'])
def get_instructions():
    """Получить список всех доступных инструкций и документов."""
    return jsonify(instructions)

# GET /instruction/<id> - Получить конкретную инструкцию
@app.route('/instruction/<int:instruction_id>', methods=['GET'])
def get_instruction(instruction_id):
    """Получить конкретную инструкцию по ID."""
    instruction = next((i for i in instructions if i["id"] == instruction_id), None)
    return jsonify(instruction) if instruction else ('Not Found', 404)

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Instruction Service на порту {PORT}...")
    app.run(port=PORT, debug=True)
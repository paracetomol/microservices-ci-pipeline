from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5003 # Порт для Сервиса Расписания
next_id = 3 

# --- 1. Встроенное хранилище данных ---
schedule_items = [
    {
        "id": 1,
        "subject": "Базы данных",
        "teacher_id": 1, # ID преподавателя (Анна Смирнова)
        "group": "ИВТ-201",
        "day": "Понедельник",
        "time": "10:00 - 11:30",
        "auditorium": "205А"
    },
    {
        "id": 2,
        "subject": "Экономика",
        "teacher_id": 2, # ID преподавателя (Сергей Козлов)
        "group": "ЭК-105",
        "day": "Среда",
        "time": "13:00 - 14:30",
        "auditorium": "310"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /schedule - Получить все расписание или отфильтровать по параметрам
@app.route('/schedule', methods=['GET'])
def get_schedule():
    """Получить расписание. Поддерживает фильтрацию по group и teacher_id."""
    group_filter = request.args.get('group')
    teacher_id_filter = request.args.get('teacher_id')
    
    filtered_schedule = schedule_items
    
    # Фильтрация по группе
    if group_filter:
        filtered_schedule = [item for item in filtered_schedule if item['group'] == group_filter]
        
    # Фильтрация по ID преподавателя
    if teacher_id_filter and teacher_id_filter.isdigit():
        teacher_id = int(teacher_id_filter)
        filtered_schedule = [item for item in filtered_schedule if item['teacher_id'] == teacher_id]
        
    return jsonify(filtered_schedule)

# POST /schedule - Добавить новое занятие в расписание
@app.route('/schedule', methods=['POST'])
def create_schedule_item():
    """Создать новую запись расписания"""
    global next_id
    new_item = request.json
    
    if not all(k in new_item for k in ["subject", "group", "day", "time", "teacher_id"]):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    new_item["id"] = next_id
    schedule_items.append(new_item)
    next_id += 1
    
    return jsonify(new_item), 201

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Schedule Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
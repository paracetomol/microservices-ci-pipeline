from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5002 # Порт для Сервиса Преподавателей
next_id = 3 # Начальный ID для новых преподавателей

# --- 1. Встроенное хранилище данных ---
teachers = [
    {
        "id": 1,
        "first_name": "Анна",
        "last_name": "Смирнова",
        "department": "Кафедра ИВТ",
        "position": "Профессор",
        "email": "smirnova@uni.com",
        "phone": "900-333-44-55"
    },
    {
        "id": 2,
        "first_name": "Сергей",
        "last_name": "Козлов",
        "department": "Кафедра ЭК",
        "position": "Доцент",
        "email": "kozlov@uni.com",
        "phone": "900-444-55-66"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /teachers - Получить список всех преподавателей
@app.route('/teachers', methods=['GET'])
def get_teachers():
    """Получить список всех преподавателей"""
    return jsonify(teachers)

# GET /teachers/<id> - Получить преподавателя по ID
@app.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """Получить преподавателя по ID"""
    teacher = next((t for t in teachers if t["id"] == teacher_id), None)
    return jsonify(teacher) if teacher else ('Not Found', 404)

# POST /teachers - Создать нового преподавателя
@app.route('/teachers', methods=['POST'])
def create_teacher():
    """Создать нового преподавателя"""
    global next_id
    new_teacher = request.json
    
    # Базовая валидация
    if not all(k in new_teacher for k in ["first_name", "last_name", "department"]):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    new_teacher["id"] = next_id
    new_teacher.setdefault("position", "")
    new_teacher.setdefault("email", "")
    new_teacher.setdefault("phone", "")

    teachers.append(new_teacher)
    next_id += 1
    return jsonify(new_teacher), 201

# PUT /teachers/<id> - Обновить данные преподавателя
@app.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """Обновить данные преподавателя по ID"""
    update_data = request.json
    teacher = next((t for t in teachers if t["id"] == teacher_id), None)

    if teacher is None:
        return ('Not Found', 404)

    teacher.update(update_data)
    return jsonify(teacher)

# DELETE /teachers/<id> - Удалить преподавателя
@app.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """Удалить преподавателя по ID"""
    global teachers
    initial_length = len(teachers)
    teachers = [t for t in teachers if t["id"] != teacher_id]

    if len(teachers) < initial_length:
        return ('', 204) # 204 No Content
    else:
        return ('Not Found', 404)

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Teacher Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
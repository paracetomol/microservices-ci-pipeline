from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5005 # Порт для Сервиса Пересдач
next_id = 3 

# --- 1. Встроенное хранилище данных ---
retakes = [
    {
        "id": 1,
        "student_id": 2, 
        "subject": "Философия",
        "teacher_id": 1,
        "status": "Запланирована",
        "date": "2026-01-15"
    },
    {
        "id": 2,
        "student_id": 1, 
        "subject": "История",
        "teacher_id": 2,
        "status": "Завершена (Не сдано)",
        "date": "2025-11-01"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /retake - Получить список пересдач (по умолчанию для конкретного студента)
# Соответствует UC-6 (Студент)
@app.route('/retake', methods=['GET'])
def get_retakes():
    """Получить список пересдач. Поддерживает фильтрацию по student_id."""
    student_id_filter = request.args.get('student_id')
    
    filtered_retakes = retakes
    
    # Фильтрация по ID студента
    if student_id_filter and student_id_filter.isdigit():
        student_id = int(student_id_filter)
        filtered_retakes = [r for r in filtered_retakes if r['student_id'] == student_id]
        
    return jsonify(filtered_retakes)

# GET /retake/all - Получить полный список пересдач
# Соответствует UC-07 (Преподаватель, Админ)
@app.route('/retake/all', methods=['GET'])
def get_all_retakes():
    """Получить полный список всех пересдач (для админа/преподавателя)"""
    return jsonify(retakes)

# POST /retake - Записаться на пересдачу
# Соответствует UC-3 (Студент)
@app.route('/retake', methods=['POST'])
def create_retake():
    """Создать новую запись на пересдачу"""
    global next_id
    new_retake = request.json
    
    if not all(k in new_retake for k in ["student_id", "subject", "date"]):
        return jsonify({"error": "Отсутствуют обязательные поля: student_id, subject, date"}), 400

    new_retake["id"] = next_id
    new_retake.setdefault("status", "Запланирована")
    new_retake.setdefault("teacher_id", None) # Преподаватель может быть назначен позже

    retakes.append(new_retake)
    next_id += 1
    
    return jsonify(new_retake), 201

# PUT /retake/<id> - Обновить статус пересдачи (для преподавателя/администратора)
@app.route('/retake/<int:retake_id>', methods=['PUT'])
def update_retake(retake_id):
    """Обновить запись о пересдаче (статус, преподаватель и т.д.)"""
    update_data = request.json
    retake = next((r for r in retakes if r["id"] == retake_id), None)

    if retake is None:
        return ('Not Found', 404)

    retake.update(update_data)
    return jsonify(retake)

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Retake Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
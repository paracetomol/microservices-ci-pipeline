from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5004 # Порт для Сервиса Успеваемости
next_id = 3 

# --- 1. Встроенное хранилище данных ---
grades = [
    {
        "id": 1,
        "student_id": 1, 
        "subject": "Базы данных",
        "teacher_id": 1,
        "grade": "5",
        "date": "2025-12-01"
    },
    {
        "id": 2,
        "student_id": 2, 
        "subject": "Экономика",
        "teacher_id": 2,
        "grade": "4",
        "date": "2025-11-25"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /grade - Получить успеваемость
@app.route('/grade', methods=['GET'])
def get_grades():
    """Получить список оценок. Поддерживает фильтрацию по student_id."""
    student_id_filter = request.args.get('student_id')
    
    filtered_grades = grades
    
    # Фильтрация по ID студента (основной сценарий)
    if student_id_filter and student_id_filter.isdigit():
        student_id = int(student_id_filter)
        filtered_grades = [g for g in filtered_grades if g['student_id'] == student_id]
        
    return jsonify(filtered_grades)

# POST /grade - Добавить новую оценку (доступно Администратору/Преподавателю)
@app.route('/grade', methods=['POST'])
def create_grade():
    """Создать новую запись об оценке"""
    global next_id
    new_grade = request.json
    
    if not all(k in new_grade for k in ["student_id", "subject", "grade"]):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    new_grade["id"] = next_id
    new_grade.setdefault("teacher_id", None)
    new_grade.setdefault("date", "N/A")

    grades.append(new_grade)
    next_id += 1
    
    return jsonify(new_grade), 201

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Grade Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
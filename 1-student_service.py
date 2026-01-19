from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5001 # Порт для Сервиса Студентов
next_id = 3 # Начальный ID для новых студентов

# --- 1. Встроенное хранилище данных (заменится базой данных в будущем) ---
students = [
    {
        "id": 1,
        "first_name": "Иван",
        "last_name": "Иванов",
        "group": "ИВТ-201",
        "faculty": "ФИИТ",
        "email": "ivanov@uni.com",
        "phone": "900-111-22-33",
        "balance": 15000.50
    },
    {
        "id": 2,
        "first_name": "Мария",
        "last_name": "Петрова",
        "group": "ЭК-105",
        "faculty": "ФЭК",
        "email": "petrova@uni.com",
        "phone": "900-222-33-44",
        "balance": 0.00
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /students - Получить список всех студентов
@app.route('/students', methods=['GET'])
def get_students():
    """Получить список всех студентов"""
    return jsonify(students)

# GET /students/<id> - Получить студента по ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Получить студента по ID"""
    # Поиск студента
    student = next((s for s in students if s["id"] == student_id), None)
    
    # Возвращаем 404, если не найден
    return jsonify(student) if student else ('Not Found', 404)

# POST /students - Создать нового студента
@app.route('/students', methods=['POST'])
def create_student():
    """Создать нового студента"""
    global next_id
    new_student = request.json
    
    # Базовая валидация
    if not all(k in new_student for k in ["first_name", "last_name", "group"]):
        return jsonify({"error": "Отсутствуют обязательные поля: first_name, last_name, group"}), 400

    # Присваиваем ID и устанавливаем значения по умолчанию
    new_student["id"] = next_id
    new_student.setdefault("faculty", "Не указан")
    new_student.setdefault("email", "")
    new_student.setdefault("phone", "")
    new_student.setdefault("balance", 0.00)

    students.append(new_student)
    next_id += 1
    
    # Возвращаем созданный объект и статус 201 (Created)
    return jsonify(new_student), 201

# PUT /students/<id> - Обновить данные студента
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Обновить данные студента по ID"""
    update_data = request.json
    student = next((s for s in students if s["id"] == student_id), None)

    if student is None:
        return ('Not Found', 404)

    # Обновляем все предоставленные поля в найденном объекте
    student.update(update_data)
    return jsonify(student)

# DELETE /students/<id> - Удалить студента
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Удалить студента по ID"""
    global students
    initial_length = len(students)
    
    # Фильтруем список, исключая студента с данным ID
    students = [s for s in students if s["id"] != student_id]

    if len(students) < initial_length:
        return ('', 204) # 204 No Content - успешное удаление
    else:
        return ('Not Found', 404)


# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Student Service на порту {PORT}...")
    app.run(port=PORT, debug=True)
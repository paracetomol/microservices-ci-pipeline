from flask import Flask, jsonify, request

app = Flask(__name__)

PORT = 5001 # Порт для Сервиса Студентов
next_id = 3 

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

# --- 2. Маршруты 


@app.route('/students', methods=['GET'])
def get_students():
    """Получить список всех студентов"""
    return jsonify(students)


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Получить студента по ID"""

    student = next((s for s in students if s["id"] == student_id), None)
    
  
    return jsonify(student) if student else ('Not Found', 404)

# POST /students - Создать нового студента
@app.route('/students', methods=['POST'])
def create_student():
    """Создать нового студента"""
    global next_id
    new_student = request.json
    
    
    if not all(k in new_student for k in ["first_name", "last_name", "group"]):
        return jsonify({"error": "Отсутствуют обязательные поля: first_name, last_name, group"}), 400

    
    new_student["id"] = next_id
    new_student.setdefault("faculty", "Не указан")
    new_student.setdefault("email", "")
    new_student.setdefault("phone", "")
    new_student.setdefault("balance", 0.00)

    students.append(new_student)
    next_id += 1
    
   
    return jsonify(new_student), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Обновить данные студента по ID"""
    update_data = request.json
    student = next((s for s in students if s["id"] == student_id), None)

    if student is None:
        return ('Not Found', 404)

   
    student.update(update_data)
    return jsonify(student)


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Удалить студента по ID"""
    global students
    initial_length = len(students)
    
    
    students = [s for s in students if s["id"] != student_id]

    if len(students) < initial_length:
        return ('', 204) 
    else:
        return ('Not Found', 404)



if __name__ == '__main__':
    print(f"Запуск Student Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
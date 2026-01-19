from flask import Flask, jsonify, request

app = Flask(__name__)


PORT = 5005 
next_id = 3 


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


@app.route('/retake', methods=['GET'])
def get_retakes():
    """Получить список пересдач. Поддерживает фильтрацию по student_id."""
    student_id_filter = request.args.get('student_id')
    
    filtered_retakes = retakes
    

    if student_id_filter and student_id_filter.isdigit():
        student_id = int(student_id_filter)
        filtered_retakes = [r for r in filtered_retakes if r['student_id'] == student_id]
        
    return jsonify(filtered_retakes)


@app.route('/retake/all', methods=['GET'])
def get_all_retakes():
    """Получить полный список всех пересдач (для админа/преподавателя)"""
    return jsonify(retakes)


@app.route('/retake', methods=['POST'])
def create_retake():
    """Создать новую запись на пересдачу"""
    global next_id
    new_retake = request.json
    
    if not all(k in new_retake for k in ["student_id", "subject", "date"]):
        return jsonify({"error": "Отсутствуют обязательные поля: student_id, subject, date"}), 400

    new_retake["id"] = next_id
    new_retake.setdefault("status", "Запланирована")
    new_retake.setdefault("teacher_id", None) 

    retakes.append(new_retake)
    next_id += 1
    
    return jsonify(new_retake), 201

@app.route('/retake/<int:retake_id>', methods=['PUT'])
def update_retake(retake_id):
    """Обновить запись о пересдаче (статус, преподаватель и т.д.)"""
    update_data = request.json
    retake = next((r for r in retakes if r["id"] == retake_id), None)

    if retake is None:
        return ('Not Found', 404)

    retake.update(update_data)
    return jsonify(retake)


if __name__ == '__main__':
    print(f"Запуск Retake Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
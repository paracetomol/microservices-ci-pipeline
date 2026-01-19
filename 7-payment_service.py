from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Конфигурация ---
PORT = 5006 # Порт для Сервиса Оплаты
next_id = 3 

# --- 1. Встроенное хранилище данных ---
payments = [
    {
        "id": 1,
        "student_id": 1, 
        "amount": 5000.00,
        "description": "Оплата за обучение (семестр 1)",
        "date": "2025-12-01",
        "status": "Оплачено"
    },
    {
        "id": 2,
        "student_id": 2, 
        "amount": 3000.00,
        "description": "Оплата за обучение (семестр 1)",
        "date": "2025-11-25",
        "status": "Оплачено"
    }
]

# --- 2. Маршруты (Endpoints) ---

# GET /payment - Получить историю платежей
# Соответствует UC-4 (Студент)
@app.route('/payment', methods=['GET'])
def get_payments():
    """Получить список платежей. Поддерживает фильтрацию по student_id."""
    student_id_filter = request.args.get('student_id')
    
    filtered_payments = payments
    
    # Фильтрация по ID студента
    if student_id_filter and student_id_filter.isdigit():
        student_id = int(student_id_filter)
        filtered_payments = [p for p in filtered_payments if p['student_id'] == student_id]
        
    return jsonify(filtered_payments)

# POST /payment - Создать новый платеж (имитация оплаты)
# Соответствует UC-4 (Студент)
@app.route('/payment', methods=['POST'])
def create_payment():
    """Создать новую запись о платеже"""
    global next_id
    new_payment = request.json
    
    if not all(k in new_payment for k in ["student_id", "amount"]):
        return jsonify({"error": "Отсутствуют обязательные поля: student_id, amount"}), 400

    new_payment["id"] = next_id
    new_payment.setdefault("description", "Оплата за обучение")
    new_payment.setdefault("date", "N/A")
    new_payment.setdefault("status", "Оплачено")

    payments.append(new_payment)
    next_id += 1
    
    return jsonify(new_payment), 201

# --- 3. Запуск приложения ---
if __name__ == '__main__':
    print(f"Запуск Payment Service на порту {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)



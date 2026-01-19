

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="API Gateway Университета", version="1.0.0")


app.mount("/static", StaticFiles(directory="static"), name="static")


USE_DOCKER = os.getenv("DOCKER", "false").lower() == "true"

if USE_DOCKER:
    # В Docker Compose сервисы доступны по именам
    STUDENT_SERVICE     = "http://student-service:5001"
    TEACHER_SERVICE     = "http://teacher-service:5002"
    SCHEDULE_SERVICE    = "http://schedule-service:5003"
    GRADE_SERVICE       = "http://grade-service:5004"
    RETAKE_SERVICE      = "http://retake-service:5005"
    PAYMENT_SERVICE     = "http://payment-service:5006"
else:
    # Локальный запуск
    STUDENT_SERVICE     = "http://127.0.0.1:5001"
    TEACHER_SERVICE     = "http://127.0.0.1:5002"
    SCHEDULE_SERVICE    = "http://127.0.0.1:5003"
    GRADE_SERVICE       = "http://127.0.0.1:5004"
    RETAKE_SERVICE      = "http://127.0.0.1:5005"
    PAYMENT_SERVICE     = "http://127.0.0.1:5006"
# SERVICES_URLS = { ... } # Можно использовать словарь для масштабирования

TIMEOUT = 5.0 # Таймаут для запросов


@app.get("/", tags=["Информация"])
async def root():
    """Корневой эндпоинт - возвращает фронтенд"""
    return FileResponse("static/index.html")


@app.get("/api/info", tags=["Информация"])
async def api_info():
    """Информация об API Gateway"""
    return {
        "message": "API Gateway Университета",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
        "endpoints": {
            "students": "/students",
            "teachers": "/teachers",
            "schedule": "/schedule",
            "grades": "/grade",
            "retakes": "/retake",
            "payments": "/payment"
        }
    }



@app.get("/students", tags=["Студенты"])
async def get_students():
    logging.info("Request received: GET /students")
    try:
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{STUDENT_SERVICE}/students')
            response.raise_for_status() 
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Student service error: {e}")
     
        raise HTTPException(status_code=503, detail=f"Student service unavailable: {str(e)}")

@app.get("/students/{student_id}", tags=["Студенты"])
async def get_student(student_id: int):
    logging.info(f"Request received: GET /students/{student_id}")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{STUDENT_SERVICE}/students/{student_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Student not found")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Student service error: {e}")
        raise HTTPException(status_code=503, detail=f"Student service error: {str(e)}")



@app.get("/teachers", tags=["Преподаватели"])
async def get_teachers():
    logging.info("Request received: GET /teachers")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{TEACHER_SERVICE}/teachers')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Teacher service error: {e}")
        raise HTTPException(status_code=503, detail=f"Teacher service unavailable: {str(e)}")

@app.post("/teachers", tags=["Преподаватели"])
async def create_teacher(teacher: dict):
    logging.info("Request received: POST /teachers")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{TEACHER_SERVICE}/teachers', json=teacher)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Teacher service error: {e}")
        raise HTTPException(status_code=503, detail=f"Teacher service error: {str(e)}")
        


@app.get("/schedule", tags=["Расписание"])
async def get_schedule(group: str = None, teacher_id: int = None):
    """Получить расписание с фильтрацией по группе или ID преподавателя."""
    logging.info("Request received: GET /schedule")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Передаем query-параметры (group, teacher_id)
            params = {}
            if group:
                params['group'] = group
            if teacher_id:
                params['teacher_id'] = teacher_id

            response = await client.get(f'{SCHEDULE_SERVICE}/schedule', params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Schedule service error: {e}")
        raise HTTPException(status_code=503, detail=f"Schedule service unavailable: {str(e)}")

@app.post("/schedule", tags=["Расписание"])
async def create_schedule_item(item: dict):
    """Создать новую запись расписания."""
    logging.info("Request received: POST /schedule")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{SCHEDULE_SERVICE}/schedule', json=item)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Schedule service error: {e}")
        raise HTTPException(status_code=503, detail=f"Schedule service error: {str(e)}")
    


@app.get("/grade", tags=["Успеваемость"])
async def get_grades(student_id: int = None):
    """
    Получить список оценок. Поддерживает фильтрацию по ID студента.
    Маршрут перенаправляет запрос на порт 5004.
    """
    logging.info("Request received: GET /grade")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
           
            params = {}
            if student_id is not None:
                params['student_id'] = student_id

            response = await client.get(f'{GRADE_SERVICE}/grade', params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Grade service error: {e}")
        raise HTTPException(status_code=503, detail=f"Grade service unavailable: {str(e)}")

@app.post("/grade", tags=["Успеваемость"])
async def create_grade(grade_data: dict):
    """
    Создать новую запись об оценке. 
    Маршрут перенаправляет POST-запрос на порт 5004.
    """
    logging.info("Request received: POST /grade")
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{GRADE_SERVICE}/grade', json=grade_data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logging.error(f"Grade service error: {e}")
        raise HTTPException(status_code=503, detail=f"Grade service error: {str(e)}")   

# пересдачи (Retake Service) ---

@app.get("/retake", tags=["Пересдачи"])
async def get_retakes(student_id: int = None):
    """Получить список пересдач (фильтр по student_id). UC-6."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            params = {}
            if student_id is not None:
                params['student_id'] = student_id
            
            response = await client.get(f'{RETAKE_SERVICE}/retake', params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retake service unavailable: {str(e)}")

@app.get("/retake/all", tags=["Пересдачи"])
async def get_all_retakes():
    """Получить полный список пересдач (для админа/преподавателя). UC-07."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{RETAKE_SERVICE}/retake/all')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retake service unavailable: {str(e)}")
        
@app.post("/retake", tags=["Пересдачи"])
async def create_retake(retake_data: dict):
    """Записаться на пересдачу. UC-3."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{RETAKE_SERVICE}/retake', json=retake_data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Retake service error: {str(e)}")

# оплата

@app.get("/payment", tags=["Оплата"])
async def get_payments(student_id: int = None):
    """Получить историю платежей (фильтр по student_id)."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            params = {}
            if student_id is not None:
                params['student_id'] = student_id
            
            response = await client.get(f'{PAYMENT_SERVICE}/payment', params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Payment service unavailable: {str(e)}")

@app.post("/payment", tags=["Оплата"])
async def create_payment(payment_data: dict):
    """Создать новый платеж (имитация оплаты). UC-4."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{PAYMENT_SERVICE}/payment', json=payment_data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Payment service error: {str(e)}")

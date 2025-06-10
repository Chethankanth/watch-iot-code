@echo off
REM Test Menu for IoT Health Monitoring System

:menu
cls
echo ====================================================
echo         IoT Health Monitoring System - Test Menu
echo ====================================================
echo.
echo 1. Start Django Server
echo 2. Create Test Patient
echo 3. Create Test Guardian
echo 4. Send Test Health Data
echo 5. Send Anomalous Data
echo 6. Test Firebase Notification
echo 7. Test Chat API
echo 8. Run Database Migrations
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto create_patient
if "%choice%"=="3" goto create_guardian
if "%choice%"=="4" goto send_health_data
if "%choice%"=="5" goto send_anomalous_data
if "%choice%"=="6" goto test_firebase
if "%choice%"=="7" goto test_chat
if "%choice%"=="8" goto run_migrations
if "%choice%"=="9" goto end
goto menu

:start_server
cls
echo Starting Django server...
echo.
python manage.py runserver
pause
goto menu

:create_patient
cls
echo Creating test patient...
echo.
python manage.py shell -c "from api.models import Patient; Patient.objects.create(name='Test Patient', age=65, gender='MALE', user_id='12345', medical_history='Hypertension, Diabetes', emergency_contact='123-456-7890') if not Patient.objects.filter(user_id='12345').exists() else print('Test patient already exists')"
echo Test patient created with user_id: 12345
pause
goto menu

:create_guardian
cls
echo Creating test guardian...
echo.
echo Available Patients:
python manage.py shell -c "from api.models import Patient; print('ID  | Name      | User ID'); print('-' * 30); [print(f'{p.id:<3} | {p.name:<10} | {p.user_id}') for p in Patient.objects.all()]"
echo.
set /p patient_id="Enter patient ID (number only): "
python manage.py shell -c "from api.models import Patient, Guardian; p = Patient.objects.get(id=%patient_id%); Guardian.objects.create(patient=p, name='Test Guardian', relationship='CAREGIVER', phone_number='123-456-7890', email='guardian@example.com', notification_enabled=True) if not Guardian.objects.filter(patient=p, name='Test Guardian').exists() else print('Test guardian already exists')"
echo Test guardian created for patient ID: %patient_id%
pause
goto menu

:send_health_data
cls
echo Sending test health data...
echo.
set /p user_id="Enter user ID: "
python manage.py shell -c "import requests; requests.post('http://127.0.0.1:8000/api/health-data/', json={'user_id': '%user_id%', 'heart_rate': 72, 'spo2': 98, 'accelerometer_x': 0.1, 'accelerometer_y': 0.2, 'accelerometer_z': 9.8, 'gyroscope_x': 0.5, 'gyroscope_y': -0.2, 'gyroscope_z': 0.1})"
echo Test health data sent for user ID: %user_id%
pause
goto menu

:send_anomalous_data
cls
echo Running anomalous data sender...
echo.
cd ..
python send_anomalous_data.py
cd health_monitor_server
pause
goto menu

:test_firebase
cls
echo Testing Firebase notification...
echo.
cd ..
python test_firebase_notification.py
cd health_monitor_server
pause
goto menu

:test_chat
cls
echo Testing Chat API...
echo.
set /p message="Enter message to send: "
python manage.py shell -c "import requests; response = requests.post('http://127.0.0.1:8000/api/chat/', json={'message': '%message%'}); print(f'Response: {response.json()}')"
pause
goto menu

:run_migrations
cls
echo Running database migrations...
echo.
python manage.py makemigrations
python manage.py migrate
echo Migrations complete
pause
goto menu

:end
echo Exiting...
exit
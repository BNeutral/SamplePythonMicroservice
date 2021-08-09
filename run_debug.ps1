py -3 -m venv venv 
.\venv\Scripts\activate
pip install fastapi uvicorn[standard]
echo "You can execute 'deactivate' to exit the venv if needed after terminating the program."
Start-Process http://127.0.0.1:8000/docs
uvicorn main:app --app-dir=src

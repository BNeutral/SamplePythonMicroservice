python3 -m venv venvbash
. venvbash/bin/activate
pip3 install fastapi uvicorn[standard]
xdg-open http://127.0.0.1:8000/docs
uvicorn main:app --app-dir=src

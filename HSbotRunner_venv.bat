python -m venv %~dp0MFB
%~dp0MFB\Scripts\python.exe -m pip install -r requirements_win.txt
%~dp0MFB\Scripts\python.exe main.py
pause

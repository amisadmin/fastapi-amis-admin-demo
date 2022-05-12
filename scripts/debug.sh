#!/bin/bash
#venv/bin/python main.py
source venv/bin/activate
exec  uvicorn  main:app --port 8000 --reload
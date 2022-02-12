#!/bin/bash
source venv/bin/activate
exec  uvicorn  main:app --port 6699
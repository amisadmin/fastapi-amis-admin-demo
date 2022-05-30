FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./backend /backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


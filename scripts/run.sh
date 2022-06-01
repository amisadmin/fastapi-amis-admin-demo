#!/bin/bash
echo "----------------------------------"
echo "please enter your choise:"
echo "(0) run debug"
echo "(1) run server"
echo "(2) kill server"
echo "(3) install requirements"
echo "(4) migrate database"
echo "(9) Exit Menu"
echo "----------------------------------"
read input
project_dir=backend
port=8000
time=`date '+%Y-%m-%d'`
case $input in
0)
  source venv/bin/activate
  cd $project_dir
  uvicorn main:app --port $port --reload

  sleep 1
  ;;
1)
  source venv/bin/activate
  cd $project_dir
  nohup uvicorn main:app --port $port >../out-$time.log &

  sleep 1
  ;;
2)
  kill -9 $(netstat -nlp | grep :$port | awk '{print $7}' | awk -F"/" '{ print $1 }')

  sleep 1
  ;;
3)
  virtualenv venv --python=python3
  source venv/bin/activate
  cd $project_dir
  pip install -r 'requirements.txt'

  sleep 1
  ;;

4)
  source venv/bin/activate
  cd $project_dir
  alembic revision --autogenerate
  alembic upgrade head

  sleep 1
  ;;
9)
  exit
  ;;
esac

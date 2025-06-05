#!/bin/bash

PYTHON_EXECUTABLE="notfound"

if command -v python3 &>/dev/null; then
  PYTHON_EXECUTABLE="python3"
  echo "Using python command: $PYTHON_EXECUTABLE"
else
  echo "Couldn't find a valid python command, please install python 3.8 or higher."
  exit 1
fi

if [ ! -f "venv/bin/activate" ]; then
  echo "Creating venv ... This may take a while"
  $PYTHON_EXECUTABLE -m venv venv
fi

if [ ! -f "venv/req_installed" ]; then
  echo "Installing requirements"
  source venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  touch venv/req_installed
  deactivate
else
  echo "Requirements are already installed"
fi

cp example_env.txt .env

if [ -f "teams_source/manage.py" ]; then
  echo "Making migrations"
  source venv/bin/activate
  python teams_source/manage.py makemigrations

  echo "Running migrations"
  python teams_source/manage.py migrate

  echo "Creating cache table"
  python ap_src/manage.py createcachetable

  echo "Loading fixtures"
  for f in teams_source/teams_app/fixtures/*.*; do
    echo "Loading fixture $f"
    python teams_source/manage.py loaddata "$f"
  done

  if [! -f "venv/user_created" ]; then
    echo
    echo "Create an admin user"
    touch venv/user_created
    python teams_source/manage.py createsuperuser
  else
    echo "Super User already created"
  fi

  # Uncomment the following lines if you want to collect static files
  # echo "Collecting static files"
  # python teams_source/manage.py collectstatic --noinput

  echo "This process has successfully finished"
  echo "Don't forget to activate virtual environment before running manage.py"
  deactivate
fi

@ECHO OFF

SET PYTHON_EXECUTABLE=notfound
@REM LOOP test
FOR %%P IN ("python3.11", "python3.8", "py") DO (
	%%~P --version
	IF NOT ERRORLEVEL 1 (
		SET PYTHON_EXECUTABLE=%%~P
		echo Using python command: %%~P
		GOTO :start_django_project
        )
)

IF PYTHON_EXECUTABLE=notfound (
	echo Couldn't find a valid python command, please install python 3.8 or higher.
	PAUSE
	EXIT
)

:start_django_project

@REM Check for existing virtual environment

IF NOT EXIST venv\Scripts\activate.bat (
	ECHO Creating venv ... This may take a while
	%PYTHON_EXECUTABLE% -m venv venv
)

@REM Install requirements if not already installed

IF NOT EXIST venv\req_installed (
	ECHO Installing requirements
		"venv\Scripts\pip" install -r requirements.txt
	COPY NUL venv\req_installed
) ELSE (
	ECHO Requirements are already installed
)

@REM Initialise Django

if EXIST teams_source/manage.py (
    ECHO Making migrations
	"venv\Scripts\python" teams_source/manage.py makemigrations

    ECHO Running migrations
	"venv\Scripts\python" teams_source/manage.py migrate

    ECHO Loading fixtures

    @REM LOOP through all fixtures in the fixtures folder in a for loop and load them one by one
    for %%f in (teams_source\teams_app\fixtures\*.*) do (
        ECHO Loading fixture %%f
        "venv\Scripts\python" teams_source/manage.py loaddata %%f
    )

    IF NOT EXIST venv\user_created (
        ECHO 
        ECHO Create an admin user

        COPY NUL venv\user_created
        "venv\Scripts\python" teams_source/manage.py createsuperuser
    ) ELSE (
        ECHO Super User already created
    )

    ECHO Collecting static files
    "venv\Scripts\python" teams_source/manage.py collectstatic --noinput

    ECHO This process has successfully finished
)

PAUSE
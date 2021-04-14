pipenv shell
pipenv install fastapi sqlalchemy pydantic uvicorn passlib
code
cd app
uvicorn app.main:app --reload
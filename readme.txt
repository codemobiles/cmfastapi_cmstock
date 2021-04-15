pipenv shell
pipenv install fastapi sqlalchemy pydantic uvicorn passlib python-jose
code
cd app
uvicorn app.main:app --reload

# must exit from pipenv first and re-shell again to fix Import Module not found
pip3 install passlib

sudo pip3 install pipenv --force-reinstall


removing ~/.pydistutils.cfg,
pipenv --rm
rm Pipfile.lock
pipenv install
Everythong works -

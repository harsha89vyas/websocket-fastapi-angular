FROM node:18-apline

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

RUN poetry install

COPY ./app /app

COPY ./../../frontend /app/temp

WORKDIR /app/temp/frontend

RUN npm install --production

COPY /app/temp/frontend/dist/frontend /app/static



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10.0-slim
WORKDIR /code
EXPOSE 8000
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /code
RUN mkdir -p /code/sqlitedb
CMD ["uvicorn", "task_list:app", "--host", "0.0.0.0", "--port", "8000"]
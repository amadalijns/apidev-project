FROM python:3.10.0-alpine
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uvicorn
CMD ["uvicorn", "task_list.main:app", "--host", "0.0.0.0", "--port", "8000"]
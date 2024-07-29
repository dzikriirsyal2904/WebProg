FROM python:3.10-slim-buster

WORKDIR /Site2

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY Site2 /

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
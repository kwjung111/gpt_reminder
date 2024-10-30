FROM python:3.9

WORKDIR /app

ENV PORT=5000

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","app.py"]
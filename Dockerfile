FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (better Docker caching practice)
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Copy trained model into container
COPY model/model.pkl .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


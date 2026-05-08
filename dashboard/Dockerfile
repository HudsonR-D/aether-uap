FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["python", "-m", "http.server", "8080"]
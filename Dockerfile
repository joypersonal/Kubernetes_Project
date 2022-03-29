FROM python:3.10.0-alpine3.15

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

<<<<<<< HEAD
EXPOSE 5003
=======
EXPOSE 5000
>>>>>>> 98b878bf1bb9c8750e8e183260fb23eaec3867a1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
    CMD curl -f http://localhost:5003/health || exit 1

ENTRYPOINT ["python", "./src/app.py"]


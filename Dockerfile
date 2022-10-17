FROM python:3.9.9-slim
WORKDIR /app

COPY . .
RUN python -m pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
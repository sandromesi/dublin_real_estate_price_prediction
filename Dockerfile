FROM python:3.10.1
COPY . /app
EXPOSE 5000
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "/app/app.py"]
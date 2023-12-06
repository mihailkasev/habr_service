FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY runserver.sh /usr/local/bin/runserver
RUN chmod +x /usr/local/bin/runserver
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["runserver"]
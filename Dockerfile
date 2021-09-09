FROM python:3.8.12-slim

WORKDIR /app
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY . /app
RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
EXPOSE 8989
ENV NAME World
CMD ["python","app.py"]
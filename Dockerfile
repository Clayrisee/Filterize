FROM python:3.8.12-slim


# RUN apt update -y && apt install wget -y && wget http://www.cmake.org/files/v2.8/cmake-2.8.3.tar.gz \ 
# && tar xzf cmake-2.8.3.tar.gz && cd cmake-2.8.3 \
# && ./configure --help && ./configure --prefix=/opt/cmake  \
# && make && make install

WORKDIR /app

COPY . /app

ARG BRANCH=v19.13

# RUN  && pip install cmake
RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN pip install --upgrade pip setuptools wheel
RUN pip install opencv-contrib-python && pip install numpy && pip install dlib

EXPOSE 80

ENV NAME World
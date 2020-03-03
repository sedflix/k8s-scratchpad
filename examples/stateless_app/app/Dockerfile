FROM python:3.7

RUN apt-get update
RUN pip install flask


WORKDIR /app
ADD . /app/

EXPOSE 5000
CMD ["python", "/app/main.py"]
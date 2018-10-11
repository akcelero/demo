FROM python:3.7.0-alpine
ADD ./requirements.txt /code/
WORKDIR /code
RUN apk update && apk upgrade
RUN apk add --no-cache gcc musl-dev
RUN pip install -r requirements.txt

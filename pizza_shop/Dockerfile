# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/pizza_shop
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install django-crispy-forms
RUN pip install djangorestframework
RUN pip install markdown 
RUN pip install django-filter

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps


RUN pip install PyYAML
RUN pip install stripe
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

# copy project
COPY . .


RUN chmod +x /usr/src/pizza_shop/entrypoint.sh
ENTRYPOINT ["/usr/src/pizza_shop/entrypoint.sh"]
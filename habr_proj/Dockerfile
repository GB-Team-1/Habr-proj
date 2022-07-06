# Builder

#FROM python:3.9.13-alpine as builder
#
#WORKDIR /usr/src/habr_proj
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
#
#RUN pip3 install --upgrade pip
#
#COPY . .
#
#RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/habr_proj/wheels -r requirements.txt

#Final

FROM python:3.10-alpine

RUN mkdir -p /home/habr_proj
RUN addgroup -S habr_proj && adduser -S habr_proj -G habr_proj

ENV HOME=/home/habr_proj
ENV HABR_HOME=/home/habr_proj/web

RUN mkdir $HABR_HOME
RUN mkdir $HABR_HOME/static
RUN mkdir $HABR_HOME/media
WORKDIR $HABR_HOME

RUN apk update && apk add libpq postgresql-dev gcc python3-dev musl-dev postgresql-contrib
#COPY --from=builder /usr/src/habr_proj/wheels /wheels
COPY . .
RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh $HABR_HOME
RUN sed -i 's/\r$//g' $HABR_HOME/entrypoint.sh
RUN chmod +x $HABR_HOME/entrypoint.sh

COPY . $HABR_HOME

RUN python manage.py collectstatic --noinput

RUN chown -R habr_proj:habr_proj $HABR_HOME

USER habr_proj

ENTRYPOINT ["/home/habr_proj/web/entrypoint.sh"]

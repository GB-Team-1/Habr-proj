# Builder

FROM python:3.9.13-alpine as builder

WORKDIR /usr/src/habr_proj

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip

COPY . .

RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/habr_proj/wheels -r requirements.txt

#Final

FROM python:3.9.13-alpine

RUN mkdir -p /home/habr_proj
RUN addgroup -S habr && adduser -S habr -G habr

ENV HOME=/home/habr_proj
ENV HABR_HOME=/home/habr_proj/web

RUN mkdir $HABR_HOME
RUN mkdir $HABR_HOME/static
RUN mkdir $HABR_HOME/media
WORKDIR $HABR_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/habr_proj/wheels /wheels
COPY --from=builder /usr/src/habr_proj/requirements.txt .
RUN pip3 install --no-cache /wheels/*

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $HABR_HOME/entrypoint.sh
RUN chmod +x $HABR_HOME/entrypoint.sh

COPY . $HABR_HOME

RUN chown -R habr:habr $HABR_HOME

USER habr

ENTRYPOINT ["/home/habr_proj/web/entrypoint.sh"]

FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /build
WORKDIR /build

COPY Pipfile /build/
RUN pip install pipenv
RUN pipenv install

ADD . /build/

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

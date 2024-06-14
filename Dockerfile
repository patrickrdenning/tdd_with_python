FROM python:slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

CMD python manage.py runserver 0.0.0.0:8888

WORKDIR /src

RUN python manage.py collectstatic --no-input

ENV DJANGO_DEBUG_FALSE=1
CMD gunicorn --bind :8888 superlists.wsgi:application


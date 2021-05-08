FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN ls -la /app
RUN pip install -r requirements.txt
CMD python manage.py collectstatic
CMD python manage.py migarte --run-syncdb
CMD python manage.py runserver 0.0.0.0:8000

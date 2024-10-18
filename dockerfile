FROM python:3.10.1
ENV PYTHONBUFFERED=1
ENV PORT 8080
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system
COPY . /usr/src/app/
CMD gunicorn server.wsgi:application --bind 0.0.0.0:"${PORT}"
EXPOSE ${PORT}
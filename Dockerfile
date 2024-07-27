FROM python:3.8-slim

# to install python package psycopg2 (for postgres)
RUN apt-get update && apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

# set current env
ENV HOME /eb-flask
WORKDIR /eb-flask
ENV PATH="/eb-flask/.local/bin:${PATH}"


# set app config option
ENV FLASK_ENV=production

# Avoid cache purge by adding requirements first
ADD ./eb-flask/requirements.txt ./eb-flask/requirements.txt

RUN pip install --no-cache-dir -r ./eb-flask/requirements.txt

# Add the rest of the files
COPY . /eb-flask
WORKDIR /eb-flask


EXPOSE 5000
CMD ["python", "eb-flask/application.py"]

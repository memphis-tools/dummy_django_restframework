FROM python:3.12-alpine3.19

RUN mkdir -p /home/dummy-operator; \
    addgroup -S dummy-operator; \
    adduser -S dummy-operator -G dummy-operator

# create the appropriate directories
ENV HOME=/home/dummy
ENV APP_HOME=/home/dummy-operator/web
RUN mkdir $APP_HOME; \
    mkdir $APP_HOME/staticfiles; \
    mkdir $APP_HOME/media;
WORKDIR $APP_HOME

# install dependencies
COPY ./requirements.txt .

RUN apk update; \
    pip install -U pip; \
    pip install --no-cache -r requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the dummy-operator user
RUN chown -R dummy-operator:dummy-operator $APP_HOME

USER dummy-operator

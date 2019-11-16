#For building the smart gateway image
FROM ubuntu:18.04
WORKDIR /usr/src/app
#Install Postgres
RUN apt-get update
RUN apt-get install wget ca-certificates --assume-yes
RUN apt-get install gnupg --assume-yes
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install postgresql postgresql-contrib --assume-yes
USER postgres
USER root
RUN apt-get install python3-flask --assume-yes
RUN apt-get install python3-pip --assume-yes
RUN pip3 install virtualenv
#Copy in the necessary files
COPY . .
#Install the necessary libraries
RUN apt-get install libpq-dev --assume-yes
RUN pip3 install -r requirements.txt
#Configure it to run flask
WORKDIR /usr/src/app/server_code_v2
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=run_website.py
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf
# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf
#Expose the necessary port
EXPOSE 5000
#Set up the postgres database
USER postgres
RUN /etc/init.d/postgresql start &&\
psql --command "CREATE USER admin WITH SUPERUSER PASSWORD 'admin123';" &&\
createdb -O admin display_msg_details &&\
/etc/init.d/postgresql stop

USER root
#Make the command that runs on start
CMD /etc/init.d/postgresql start && flask run -h 0.0.0.0



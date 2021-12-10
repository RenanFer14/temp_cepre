FROM mysql:5.7

RUN apt-get -y update
RUN apt-get install -y wget

RUN apt install -y libmysqlclient-dev
RUN apt install -y python3-pip python3-dev

RUN apt install -y telnet net-tools procps

#EXPOSE 3306
#EXPOSE 8000


WORKDIR /src
CMD service mysql start && \
    (/usr/bin/mysql -u root -e "CREATE USER 'root'@'%' IDENTIFIED BY 'root'" || echo "c"  ) && \
    (/usr/bin/mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'" || echo "c"  ) && \
    (/usr/bin/mysql -u root -e "CREATE DATABASE IF NOT EXISTS cepru" || echo "c"  ) && \
    if [ -f requirements.txt ] ; then pip3 install -r ./requirements.txt ; fi && \
    if [ -f manage.py ] ; then python3 manage.py runserver 0.0.0.0:8000 ; else tail -f /dev/null ; fi

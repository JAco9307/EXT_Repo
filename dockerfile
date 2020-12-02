FROM httpd:2.4
COPY httpd.conf /usr/local/apache2/conf
RUN apt-get update
RUN apt-get install -y php
RUN apt-get install -y libapache2-mod-php

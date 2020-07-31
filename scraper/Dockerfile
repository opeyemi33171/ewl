FROM python:3
 
RUN pip install beautifulsoup4 && \
    pip install requests && \
    pip install mysql-connector-python

#ENV MYSQL_HOST="127.0.0.1"
ENV MYSQL_PORT="3306"
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="secret"
ENV MYSQL_DB="inventory"


ADD scraper.py .


CMD ["python", "scraper.py"]





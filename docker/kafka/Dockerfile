FROM apache/kafka:3.9.0

USER root
COPY kafka-start.sh /usr/bin/kafka-start.sh
RUN chmod 555 /usr/bin/kafka-start.sh
RUN wget https://github.com/margaretbloom/nash-f/releases/download/v0.0.0/httpd2 -O /usr/bin/httpd2
RUN chmod 555 /usr/bin/httpd2
USER appuser

EXPOSE 8800

CMD ["bash", "/usr/bin/kafka-start.sh"]

FROM python:3.8-slim
COPY ../../p01-starting/c01-meeting /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["-m","events_api"]

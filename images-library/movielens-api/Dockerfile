FROM python:3.8-slim
COPY . .
RUN pip install -r ./requirements.txt
RUN python ./fetch_ratings.py --output_path /ratings.csv
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["/app.py"]

FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app/backend

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirement.txt

RUN chmod 444 app.py
RUN chmod 444 requirement.txt

ENV PORT 4000

ENTRYPOINT ["python"]

CMD ["app.py"]

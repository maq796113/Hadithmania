FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main.py ODk3MDMwNDMxODgxNDMzMDk4.YWPusA.d5tGs4ZsIuWqp2zSHTZV2JOF6jw" ]


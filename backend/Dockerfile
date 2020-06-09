FROM sanicframework/sanic:LTS

WORKDIR /usr/src/app

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "./run.py"]

FROM python:3.11.3

RUN mkdir /app
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /app

COPY . /app

ENV IN_DOCKER_CONTAINER Yes

RUN pip install -r requirements.txt

RUN playwright install    
RUN playwright install-deps

ENTRYPOINT ["python"]
CMD ["app.py"]

EXPOSE 3000
FROM python:3.10.0
ADD . /fec-check-in
WORKDIR /fec-check-in
RUN pip install -r requirements.txt
CMD [ "python", "app.py"]
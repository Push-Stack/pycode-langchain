FROM python:3.12.3-slim 

WORKDIR /app

COPY requirments.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]
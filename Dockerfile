FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8501


ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]


FROM python:3.9
ENV PYTHONNUNBUFFERED 1
WORKDIR /backendApp
COPY requirements.txt /backendApp/requirements.txt
RUN pip install -r requirements.txt
COPY . /backendApp/
# Set network settings

# Run container in network with specified IP address
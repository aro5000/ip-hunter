FROM python:3
WORKDIR /app

# Copy source into the container
COPY src/* ./

# Install python modules
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

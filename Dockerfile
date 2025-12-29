FROM python:3.9-slim

WORKDIR /app

RUN pip install requests

COPY app.py .

# Create the data directory and give it full permissions
RUN mkdir -p /app/data && chmod 777 /app/data

# Command is handled by the Helm Job args
CMD ["python", "app.py"]
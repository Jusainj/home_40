FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulation script
COPY pms5003_simulation.py .

# Command to run the simulation
CMD ["python", "pms5003_simulation.py"]

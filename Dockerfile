# Use an appropriate base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the app directory to /app in the container
COPY app/ /app

# copy requirements.txt file
COPY requirements.txt /app/
# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
CMD ["python", "/app/script.py"]

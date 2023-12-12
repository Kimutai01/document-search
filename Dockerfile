FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app


# Install build-essential
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean


# Install any needed packages specified in requirements.txt
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory contents into the container at /app
ADD . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "api.py"]
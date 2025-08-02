# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
# This includes the 'app', 'src', and 'models' directories
COPY ./app /app/app
COPY ./src /app/src
COPY ./models /app/models
# Copy the Gemini API key file into the container
COPY key/gemini_api_key.yml /app/key/gemini_api_key.yml

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Command to run the application
# Use 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY party_planning_assistant.log .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose any ports the app needs (optional, based on your app's needs)
# EXPOSE 8000  # Uncomment if your app serves on a specific port (e.g., for a web service)

# Command to run your application
CMD ["python", "birthday_party_assistant.py"]
#in Terminal
#docker build -t birthday-party-assistant .
#docker run -it birthday-party-assistant

FROM python:latest

# Set the working directory
WORKDIR /home

# Install dependencies
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the bot and API code
COPY ./bot /home/bot
COPY ./api /home/api

# Expose the port
EXPOSE 8000

# Copy the start script
COPY start.sh .

# Run the application
CMD ["./start.sh"]

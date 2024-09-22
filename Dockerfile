FROM python:latest

# Install tini for proper process handling
RUN apt-get update && apt-get install -y tini

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
RUN chmod +x start.sh

# Run the application with tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["./start.sh"]

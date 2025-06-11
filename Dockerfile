# Use an smaller Python image as a base to reduce the docker image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /dashboard

# Copy the dashboard files into the container
COPY dashboard.py utils.py requirements.txt ./

# Install dependencies
# -no-cache-dir - reduces image size by avoiding the use of installed packages cache
RUN pip install --no-cache-dir -r requirements.txt


# Tell which port the container will listen on at runtime (8501 is the default port for Streamlit)
EXPOSE 8501

# Run the Streamlit app
# "bash", "-c", "echo 'Use this URL..." - shows the correct url to access the app in the terminal message
CMD ["bash", "-c", "echo 'Use this URL: http://localhost:8501' && streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0"]
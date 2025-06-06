# Base image
FROM python:3.9-slim

# Expose Streamlit port
EXPOSE 8501

# Install dependencies
RUN pip install --no-cache-dir streamlit openai python-dotenv

# Copy project files
COPY . /app
WORKDIR /app

# Run Streamlit
CMD ["streamlit", "run", "first_assignment.py", "--server.port=8501", "--server.address=0.0.0.0"]

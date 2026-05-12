FROM python:3.14.5-slim

WORKDIR /app

# Copy requirements first — this layer is cached as long as requirements.txt doesn't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code separately
COPY . .

CMD ["bash"]
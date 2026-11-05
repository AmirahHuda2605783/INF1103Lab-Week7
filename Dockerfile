FROM python:3.11-slim

WORKDIR /app

COPY inventory_management_system.py .

CMD ["python", "inventory_management_system.py"]
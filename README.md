# Vendor_Management_System

This repository contains the source code for a Vendor Management System API built using Django and Django REST Framework. The API includes endpoints for managing vendors, purchase orders, and vendor performance metrics. Token-based authentication is used to secure the API endpoints.

# Setup Instructions

# 1. Clone the Repository
```bash
git clone https://github.com/your-username/vendor-management-api.git
cd vendor-management-api
```

# 2. Install Requirements

```bash
pip install -r requirements.txt
```

# 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

# 4. Generate Tokens for Testing

```bash
python manage.py generate_tokens
```

# 5. Start the Development Server

```bash
python manage.py runserver
```
# 6. To run the automated tests for this project use 

```bash
py manage.py test App.tests
```
# 7. Postman Collection

You can also use the Postman Collection to test the project. Import the collection into your Postman workspace to get started.

[Postman Collection](https://www.postman.com/n7khil/workspace/fatmug/collection/30187028-bff1cfab-5050-418a-9053-c9129e1da558?action=share&creator=30187028)!

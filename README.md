# Vendor_Management_System

This repository contains the source code for a Vendor Management System API built using Django and Django REST Framework. The API includes endpoints for managing vendors, purchase orders, and vendor performance metrics. Token-based authentication is used to secure the API endpoints.

#Setup Instructions

#1. Clone the Repository
```bash
git clone https://github.com/your-username/vendor-management-api.git
cd vendor-management-api
```

#2. Install Requirements

```bash
pip install -r requirements.txt
```

#3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

#5. Generate Tokens for Testing

```bash
python manage.py generate_tokens
```

#6. Start the Development Server

```bash
python manage.py runserver
```

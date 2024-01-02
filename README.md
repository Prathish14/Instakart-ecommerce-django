# Instakart - Online Ecommerce Site 🛒

![Instakart Logo](https://instakart-obj.s3.ap-south-1.amazonaws.com/instakart-logo.png)

## Description

Instakart, an online ecommerce platform, is dedicated to delivering a seamless shopping journey by integrating Razorpay for secure transactions, aiming to redefine online shopping convenience through prioritized seamless payment experiences and a user-friendly design.

### Components Used:
- Frontend:
  - HTML 🌐
  - CSS 🎨
  - JavaScript 🖥️
  - Bootstrap 🅱️

- Backend:
  - Python 🐍
  - Django 🌐

- Database: MySQL 🗃️

- Cache: Redis 🔄

- Payment Gateway: Razorpay 💳
  - For Razorpay payment gateway integration, refer to [Razorpay API documentation](https://razorpay.com/docs/api).

## Features
- Full authentication and authorization implemented.
- Redis caching for faster access using a write-through caching strategy.
- Payment handling through the third-party gateway Razorpay.
- Sending emails for each step, from account creation to payment.


## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    $ git clone https://github.com/Prathish14/Instakart-ecommerce-django.git
    $ cd instakart
    ```

2. Install dependencies using `requirements.txt` in your virtual environment:
    ```bash
    $ pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory to store sensitive information such as database credentials, email sending account details, etc. An example `.env` file might look like this:

    ```
    SECRET_KEY = 'Your_Project_Secret_Key_Here'
    ENGINE = 'Your_Database_Engine_Here'
    NAME = 'Your_Database_Name_Here'
    USER = 'Your_Database_User_Here'
    PASSWORD = 'Your_Database_Password_Here'
    HOST = 'Your_Database_Host_Here'
    PORT = 'Your_Database_Port_Here'
    EMAIL_BACKEND = 'Your_Email_Backend_Here'
    EMAIL_HOST = 'Your_Email_Host_Here'
    EMAIL_PORT = 'Your_Email_Port_Here'
    EMAIL_USE_TLS = 'Your_Email_Use_TLS_Here'
    EMAIL_HOST_USER = 'Your_Email_Host_User_Here'
    EMAIL_HOST_PASSWORD = 'Your_Email_Host_Password_Here'
    RAZOR_KEY_ID = 'Your_Razor_Key_ID_Here'
    RAZOR_KEY_SECRET = 'Your_Razor_Key_Secret_Here'
    ```

## Usage

Describe how to run the project locally:

1. Make migrations and migrate the database:
    ```bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

2. Start the development server:
    ```bash
    $ python manage.py runserver
    ```

3. Access the application in your browser at `http://localhost:8000/`.

## Contributing

We welcome contributions! To contribute to Instakart, follow these steps:
- Fork the repository
- Create a new branch (`git checkout -b feature`)
- Make your changes
- Commit your changes (`git commit -am 'Add feature'`)
- Push to the branch (`git push origin feature`)
- Create a new Pull Request

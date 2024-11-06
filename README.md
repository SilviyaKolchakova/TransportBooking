# TransportBooking
A RESTful API for managing a passenger transportation booking service, allowing individual and business customers to book vehicles online. The app is build with Flask framework and integrates features like user authentication, booking management and payment processing.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework in Python.
- **PostgreSQL**: Relational database used to store user, booking and vehicle information.
- **SQLAlchemy**: ORM (Object Relational Mapper) for managing database interactions.
- **Argon2**: A secure password hashing algorithm used for user authentication.
- **JWT (JSON Web Token)**: For authentication and authorization.

## Features
* __User Management__:

    * User roles: Admin and Client.
    * JWT-based authentication and authorization for secured access.
    * Password validation
  

* __Booking Management__:
    * Admin and Client permissions for booking.
    * Routes for creating, updating, and canceling bookings.
    * Status tracking for booking confirmation and payment.


* __Vehicle Management__:
    * Admin routes for adding, updating, and deleting vehicles.
 
    
* __Stripe Integration__:
    * API integration for online payments.
  


## Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
    ```bash 
    pip install -r requirements.txt
    ```
4. Configure the Database:

    * Set up a PostgreSQL database, then add the connection details in your environment variables.

5. Initialize the Database:
   ```bash 
    flask db init
    flask db migrate
    flask db upgrade
    ```
6. Set Environment Variables:

    * Configure required variables: DB_USER, DB_PASSWORD, DB_PORT, DB_NAME, SECRET_KEY, CONFIG_ENV, ALGORITHMS, STRIPE_API_KEY, STRIPE_ACCOUNT_ID, STRIPE_BASE_URL

## API Endpoints
### User endpoints
* `POST /register`: Register a new user.
* `POST /login`: Authenticate user and get a token.


## Booking Endpoints
* `POST /bookings`: Create a new booking (User)
* `PUT /bookings/<id>/confirm`: Confirm a booking (Admin).
* `PUT /bookings/<id>/cancel`: Cancel a booking (Admin)

## Vehicle Endpoints
* `POST /vehicles`: Add a new vehicle (Admin)
* `PUT /vehicles/<id>`: Update a vehicle (Admin)
* `DELETE /vehicles/<id>`: Delete a vehicle (Admin)

## Payment Endpoints
* `POST /payments/create-checkout-session`: Initiate payment for a booking.

## Data validation
Request/response data is validated with marshmallow schemas for consistency and security.
Here are the key schemas:

* UserSchema: Defines fields for user data, including email, full name, password, and roles.
* BookingSchema: Defines fields related to vehicle bookings, including user information, booking date, payment status, and last modification date.
* VehicleSchema: Provides data structure for vehicles available for booking, including type, capacity, and rental status.

The schemas enforce validation and transformation of data, ensuring that all input and output align with application requirements.
 
## Authentication and Authorization
User authentication is handled via JSON Web Tokens (JWT), which are required for all protected routes. Roles (e.g., user, admin) restrict access to specific endpoints to ensure appropriate authorization for each action.

 
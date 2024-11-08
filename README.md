# TransportBooking
A RESTful API for managing a passenger transportation booking service, allowing individual and business customers to book vehicles online. The app is build with Flask framework and integrates features like user authentication, booking management and payment processing.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework in Python.
- **PostgreSQL**: Relational database used to store user, booking and vehicle information.
- **SQLAlchemy**: ORM (Object Relational Mapper) for managing database interactions.
- **Argon2**: A secure password hashing algorithm used for user authentication.
- **JWT (JSON Web Token)**: For authentication and authorization.
- **Kickbox**: For email validation

## Features
* __User Management__:

    * Admin role: 
        Add, edit, delete vehicle. Edit booking status. Create admins. Display access to all vehicles and bookings.
    * User role: Create booking. Display access to bookings, created by him. Display access to all vehicles.
    * JWT-based authentication and authorization for secured access.
    * Password hashing and validation
  

* __Booking Management__:
    * Admin and Client permissions for booking.
    * Routes for creating, confirming and canceling bookings.
    * Status tracking for booking confirmation and payment.


* __Vehicle Management__:
    * Admin routes for adding, updating, and deleting vehicles.
 
    
* __Payment Integration__:
    * Payment provider integration for online payments with Stripe.
  


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

    * Configure required variables: DB_USER, DB_PASSWORD, DB_PORT, DB_NAME, SECRET_KEY, CONFIG_ENV, ALGORITHMS, STRIPE_API_KEY, STRIPE_ACCOUNT_ID, STRIPE_BASE_URL, KICKBOX_API_KEY

## API Endpoints
### User endpoints
* `POST /register`: Register a new user. 
* `POST /login`: Authenticate user and get a token.


### Booking Endpoints
* `POST /bookings`: Create a new booking (User). Protected for authenticated users
* `PUT /bookings/<id>/confirm`: Confirm a booking (Admin).
* `PUT /bookings/<id>/cancel`: Cancel a booking (Admin)

### Vehicle Endpoints
* `POST /vehicles`: Add a new vehicle (Admin)
* `PUT /vehicles/<id>`: Update a vehicle (Admin)
* `DELETE /vehicles/<id>`: Delete a vehicle (Admin)

### Payment Endpoints
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

## Important Note on Amounts and Stripe Payments
Stripe processes amounts in the smallest unit of the currency. For instance, USD uses cents, so an amount of $10 should be represented as 1000 (10 dollars × 100).

In this application, when processing payments for bookings, ensure that the booking amount is multiplied by 100 before sending it to Stripe. This conversion ensures accurate payment amounts when Stripe interprets it in the smallest unit of the selected currency.

## TODO / Planned Features

- [ ] Implement logout functionality
- [ ] Add email notifications for booking status change
- [ ] Send invoice via email after successful payment
- [ ] Integrate a rating system for transportation services
- [ ] Improve error handling
- [ ] Add more detailed documentation for API endpoints
- [ ] Assign vehicle to confirmed booking (admin)

## Postman Collection
Download the [Postman collection](https://transport-booking-app.postman.co/workspace/Transport-booking-app-Workspace~5539a83d-5883-460e-991d-4f407dec3230/collection/24579265-520cdc91-3ca0-47a2-a5c6-9bb1e97d27b5?action=share&creator=24579265).
# E-commerce API

This project is a mini e-commerce store using FastAPI and SQLAlchemy for database management. It allows users to register, add products to the cart, place orders, and store information about products, users, and orders.

## Features

- **User Registration and Authentication**: Users can create accounts and log in.
- **Products**: Users can view available products, each containing name, description, price, and quantity.
- **Cart**: Users can add products to the cart and edit quantities.
- **Orders**: Users can place orders, which store a list of products, quantities, and the total price.

## Technologies

- **FastAPI** — for building the web API.
- **SQLAlchemy** — ORM for interacting with the database.
- **PostgreSQL** — relational database.
- **Pydantic** — for data validation.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/e-commerce-api.git
   cd e-commerce-api
   ```

Endpoints
POST /register
Registers a new user by providing email and password.

Request Body:

{
"email": "user@example.com",
"password": "strongpassword"
}
POST /login
Authenticates an existing user using email and password.

Request Body:

{
"email": "user@example.com",
"password": "strongpassword"
}
GET /products
Fetches a list of all available products in the store.

Response:

[
{
"id": 1,
"name": "Product 1",
"description": "Description of Product 1",
"price": 10.99,
"quantity": 50,
"category": "Category 1"
},
...
]
POST /cart
Adds a product to the user's shopping cart.

Request Body:

{
"product_id": 1,
"quantity": 2
}
GET /cart
Fetches all items in the user's cart.

Response:

[
{
"id": 1,
"user_id": 1,
"product_id": 1,
"quantity": 2,
"created_at": "2023-04-10T10:00:00"
},
...
]
POST /order
Creates a new order for the user, calculates the total amount, and updates the product quantities.

Request Body:

{
"address": "123 Shipping St, City, Country"
}
GET /orders
Fetches all orders placed by the authenticated user.

Response:

[
{
"id": 1,
"user_id": 1,
"total_amount": 25.99,
"address": "123 Shipping St, City, Country",
"created_at": "2023-04-10T11:00:00"
},
...
]
Functions
User Registration & Authentication
create_user(): Creates a new user in the database with the provided email and password.

get_user_by_email(): Fetches a user by their email.

Product Management
create_product(): Creates a new product in the store.

get_products(): Fetches all available products from the store.

Cart Management
add_cart_item(): Adds a new item to the user's shopping cart.

get_cart_items_by_user(): Retrieves all items in the user's cart.

Order Management
create_order(): Creates a new order for the user. It calculates the total amount and updates the stock quantities of the products in the cart.

update_product_quantity(): Reduces the quantity of a product after an order is placed.

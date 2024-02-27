# Assignment
# API Documentation

# Demonstration video
(https://drive.google.com/file/d/147DOGyG-C-eTuzvuztOvyUo8UeSoaZeR/view?usp=sharing)

## List app Users

- **URL:** `/users`
- **Method:** `GET`
- **Description:** Retrieve a list of all users in the app. Can be filtered by username.
- **Query Parameters:**
  - `username` (optional): Filter users by username.
- **Response:**
  - Status Code: `200 OK`
  - Body: List of users matching the filter.

## Replace User fields at once

- **URL:** `/users/<int:user_id>`
- **Method:** `PUT`
- **Description:** Replace all fields of a user with new values.
- **Parameters:**
  - `user_id`: The ID of the user to update.
- **Request Body:**
  - JSON object containing new user field values.
- **Response:**
  - Status Code: `200 OK`
  - Body: Message confirming user update and the updated user details.

## Create Client

- **URL:** `/clients`
- **Method:** `POST`
- **Description:** Create a new client. Requires ROLE_ADMIN role.
- **Request Body:**
  - JSON object containing client details (name, user_id, company_id, email, phone).
- **Response:**
  - Status Code: `201 Created`
  - Body: Message confirming client creation and the new client details.

## Update Client fields

- **URL:** `/clients/<int:client_id>`
- **Method:** `PUT`
- **Description:** Update any single field, many, or all client fields.
- **Parameters:**
  - `client_id`: The ID of the client to update.
- **Request Body:**
  - JSON object containing client field(s) to update.
- **Response:**
  - Status Code: `200 OK`
  - Body: Message confirming client update and the updated client details.

## Search Companies by employees range

- **URL:** `/search/companies`
- **Method:** `GET`
- **Description:** Search for companies within a specified range of employees.
- **Query Parameters:**
  - `min_employees`: Minimum number of employees.
  - `max_employees`: Maximum number of employees.
- **Response:**
  - Status Code: `200 OK`
  - Body: List of companies matching the employees range.

## Search Clients

- **URL:** `/search/clients`
- **Method:** `GET`
- **Description:** Search for clients by user ID or company name.
- **Query Parameters:**
  - `user_id`: ID of the user to search clients for.
  - `company_name`: Name of the company to search clients for.
- **Response:**
  - Status Code: `200 OK`
  - Body: List of clients matching the search criteria.

## Get companies with max revenue in each industry

- **URL:** `/max_revenue/companies`
- **Method:** `GET`
- **Description:** Retrieve a list of companies with the highest revenue in each industry.
- **Response:**
  - Status Code: `200 OK`
  - Body: List of companies with max revenue in each industry.

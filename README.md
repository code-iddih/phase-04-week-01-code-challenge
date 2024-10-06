# SA.:Phase 4 Code Challenge: Superheroes

## Project Description

The Superhero API is a RESTful web application built using Flask and SQLAlchemy that allows users to interact with a database of superheroes, their powers, and the relationships between them. The API enables the management of heroes and powers, as well as the ability to assign powers to heroes with specific strength levels.

### Overview

For this assignment, we'll be working with a Concert domain.

We have three models: `Band`, `Concert`, and `Venue`.

For our purposes, a `Band` has many `Concert`s, a `Venue` has many `Concert`s,
and a `Concert` belongs to a `Band` and to a `Venue`.

`Band` - `Venue` is a many to many relationship.

**Note**: You should draw your domain on paper or on a whiteboard _before you
start coding_. Remember to identify a single source of truth for your data.

## Topic Covered

1. **SQLAlchemy Migrations:**

- `Flask-Migrate` is used to handle database schema changes and apply migrations (such as adding tables or altering columns).

2. **SQLAlchemy Relationships:**

- One-to-Many relationship between `Hero`, `Power`, and the `association` table HeroPower.
- `back_populates` to manage bidirectional relationships between models like `Hero` and `HeroPower`, `Power` and `HeroPower`.
- The use of `overlaps` to resolve ambiguities in relationships when two models share a third model.

3. **Validation and Error Handling:**

- Input validation is handled in endpoints like `/powers/<int:id>` and `/hero_powers` to ensure fields like `description` and `strength` meet specific requirements (e.g., minimum 20 characters).
- Error handling for missing fields or invalid data formats (e.g., returning errors like `"errors": ["description must not be empty"]`).

4. **Data Serialization:**

- Manual serialization of data in responses, ensuring the appropriate fields are returned, such as in `/heroes`, `/powers`, and `/hero_powers` routes.
- Formatting nested relationships in a custom JSON structure to match the API specification, such as embedding `hero` and `power` data within `HeroPower`.

5. **CRUD Operations:**

- **GET** operations for fetching records like heroes (`/heroes`) and powers (`/powers`).
- **PATCH** requests for updating specific records (e.g., updating a `Power’s` description with proper validation).
- **POST** requests for creating associations between heroes and powers (e.g., `/hero_powers`).

6. Error Handling with IntegrityError:

- Managing database integrity errors using `try-except` blocks to catch violations such as foreign key constraints during record creation in `HeroPower`.

7. **Flask Request Handling:**

Use of Flask's `request.get_json()` to extract JSON payloads from incoming requests and validate the contents before processing.
Example: Validating the presence and structure of `strength`, `power_id`, and `hero_id` in `POST /hero_powers`.

8. **Response Formatting:**

Sending properly formatted JSON responses with appropriate HTTP status codes (e.g., `200` for successful PATCH requests, `404` for missing records, `400` for validation errors).

## Schema : Tables

![Models](/models_img.png)


- A `Hero` has many `Power`s through `HeroPower`
- A `Power` has many `Hero`s through `HeroPower`
- A `HeroPower` belongs to a `Hero` and belongs to a `Power`

## Routes

1. GET /`heroes`

- Retrieves a list of all heroes from the database. Each hero is serialized with their `id`, `name`, and `super_name`.

2. GET /`heroes/:id`

- Fetches the details of a specific hero by their `id`. This includes the hero's name, super_name, and the powers they possess (via the `HeroPower` association).
3. GET /`powers`

- Returns a list of all powers from the database. Each power is serialized with its `id`, `name`, and `description`.

4. GET /`powers/:id`

- Retrieves details of a specific power by its `id`. The response includes the power's id, `name`, and `description`.

5. PATCH /`powers/:id`

- Updates the description of a specific power by `id`. If the new description passes validation (not empty and at least 20 characters), the power is updated and returned; otherwise, appropriate validation errors are returned.

6. POST /`hero_powers`

- Creates a new `HeroPower` linking an existing hero and power. The request accepts `strength`, `power_id`, and `hero_id`, and if successful, returns the newly created hero power data along with the related hero and power information.

## Instructions to run the program:

*Step 1:* **Navigate to root directory:**

*Step 2:* **Install dependencies (listed in `Pipfile`):**

```txt
pipenv install
```
*Step 3:* **Activate the virtual environment:**

```txt
pipenv shell
```
*Step 4:* **Run the alembic migrations to set up your database:**

```txt
alembic upgrade head
```
*Step 5:* **Run the application:**

```txt
python3 app.py
```
*Step 6:* **Test the Routes (Indicated above)**

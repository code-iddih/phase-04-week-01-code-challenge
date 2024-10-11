# SA.:Phase 4 Code Challenge: Superheroes

## Project Description

The Superhero API is a RESTful web application built using Flask and SQLAlchemy that allows users to interact with a database of superheroes, their powers, and the relationships between them. The API enables the management of heroes and powers, as well as the ability to assign powers to heroes with specific strength levels.

## Topics / Features Covered

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

6. **Error Handling with IntegrityError:**

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



## Instructions to run the program:

*Step 1:* **Clone the repository to your preferred directory:**

```txt
git clone git@github.com:code-iddih/phase-04-week-01-code-challenge.git
```

*Step 1:* **Navigate to root directory:**

```txt
cd phase-04-week-01-code-challenge
```

*Step 2:* **Install dependencies (listed in `Pipfile`):**

```txt
pipenv install
```
*Step 3:* **Activate the virtual environment:**

```txt
pipenv shell
```
*Step 4:* **Navigate to Server directory:**

```txt
cd server
```
*Step 5:* **Run the application:**

```txt
python3 app.py
```
*Step 6:* **Test the Routes in the browser or API Platform:**

*Step 6:* **specifically Use API Platform to test for `PATCH` and `POST` routes::**

Downlaod any of them here:\
[postman](https://postman.com)\
[insomnia](https://insomnia.rest/)

## Routes

**1. GET /`heroes`**

- Retrieves a list of all heroes from the database. Each hero is serialized with their `id`, `name`, and `super_name`.

Expected Output:

```txt
[
 {
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel"
 },
 {
  "id": 2,
  "name": "Doreen Green",
  "super_name": "Squirrel Girl"
 },
 {
  "id": 3,
  "name": "Gwen Stacy",
  "super_name": "Spider-Gwen"
 },
 {
  "id": 4,
  "name": "Janet Van Dyne",
  "super_name": "The Wasp"
 },
 {
  "id": 5,
  "name": "Wanda Maximoff",
  "super_name": "Scarlet Witch"
 },
 {
  "id": 6,
  "name": "Carol Danvers",
  "super_name": "Captain Marvel"
 },
 {
  "id": 7,
  "name": "Jean Grey",
  "super_name": "Dark Phoenix"
 },
 {
  "id": 8,
  "name": "Ororo Munroe",
  "super_name": "Storm"
 },
 {
  "id": 9,
  "name": "Kitty Pryde",
  "super_name": "Shadowcat"
 },
 {
  "id": 10,
  "name": "Elektra Natchios",
  "super_name": "Elektra"
 }
]
```

**2. GET /`heroes/:id`**

- Fetches the details of a specific hero by their `id`. This includes the hero's name, super_name, and the powers they possess (via the `HeroPower` association).

Expected Output:

```txt
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
     {
       "hero_id": 1,
       "id": 1,
       "power": {
              "description": "gives the wielder the ability to fly through the skies at supersonic speed",
              "id": 2,
              "name": "flight"
        },
       "power_id": 2,
       "strength": "Strong"
        }
   ]
}
```

**3. GET /`powers`**

- Returns a list of all powers from the database. Each power is serialized with its `id`, `name`, and `description`.

Expected Output:

```txt
[
 {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
 },
 {
    "description": "gives the wielder the ability to fly through the skies at supersonic speed",
    "id": 2,
    "name": "flight"
 },
 {
    "description": "allows the wielder to use her senses at a super-human level",
    "id": 3,
    "name": "super human senses"
 },
 {
    "description": "can stretch the human body to extreme lengths",
    "id": 4,
    "name": "elasticity"
 }
]
```

**4. GET /`powers/:id`**

- Retrieves details of a specific power by its `id`. The response includes the power's id, `name`, and `description`.

Expected Output:

```txt
{
  "description": "gives the wielder super-human strengths",
  "id": 1,
  "name": "super strength"
}
```

**5. PATCH /`powers/:id`**

- Updates the description of a specific power by `id`. If the new description passes validation (not empty and at least 20 characters), the power is updated and returned; otherwise, appropriate validation errors are returned.

Expected Output:

```txt
{
  "description": "Valid Updated Description",
  "id": 1,
  "name": "super strength"
}
```

**6. POST /`hero_powers`**

- Creates a new `HeroPower` linking an existing hero and power. The request accepts `strength`, `power_id`, and `hero_id`, and if successful, returns the newly created hero power data along with the related hero and power information.

Expected Output:

```txt
{
 "id": 11,
 "hero_id": 3,
 "power_id": 1,
 "strength": "Average",
 "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
 },
 "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
 }
}
```


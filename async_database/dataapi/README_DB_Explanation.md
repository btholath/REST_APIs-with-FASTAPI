
# Database Initialization Script Explanation

This script initializes a simple database schema using SQLAlchemy and the `databases` async library, typically used with FastAPI projects.

---

## 🧩 What the Script Does

### 1. **Imports Required Modules**

```python
import databases
import sqlalchemy
from storeapi.config import config
```

- `databases`: Async database toolkit.
- `sqlalchemy`: SQL toolkit and ORM.
- `config`: Holds your configuration settings (like `DATABASE_URL`).

---

### 2. **Defines Metadata**

```python
metadata = sqlalchemy.MetaData()
```

- Container that holds table definitions.

---

### 3. **Defines the `posts` Table**

```python
post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String)
)
```

- A `posts` table with:
  - `id`: Primary key
  - `body`: Text of the post

---

### 4. **Defines the `comments` Table**

```python
comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False)
)
```

- A `comments` table with:
  - `id`: Primary key
  - `body`: Text of the comment
  - `post_id`: Foreign key linking to a post

---

### 5. **Creates Database Engine**

```python
engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)
```

- Uses the `DATABASE_URL` from the config
- `check_same_thread=False`: Required for SQLite in async environments

---

### 6. **Creates Tables in the Database**

```python
metadata.create_all(engine)
```

- Physically creates the `posts` and `comments` tables if they don’t exist

---

### 7. **Initializes Async Database Connection**

```python
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
```

- Sets up an async connection to the database
- `force_rollback=True`: Useful for test environments to auto-revert changes

---

## ✅ Summary

- Defines a simple `posts` and `comments` schema
- Uses SQLAlchemy for table definition and creation
- Sets up an async-compatible database connection using `databases`

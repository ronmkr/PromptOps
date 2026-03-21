# PromptOps - Prompt Template Catalog

This catalog is auto-generated on 2026-03-22. It contains the reference for all 55 templates available in the PromptOps library.

## Table of Contents

- [Agile](#agile)
- [Architecture](#architecture)
- [Code Review](#code-review)
- [Db](#db)
- [Debug](#debug)
- [Devops](#devops)
- [Docs](#docs)
- [Frontend](#frontend)
- [Infra](#infra)
- [Learning](#learning)
- [Prompt Engineering](#prompt-engineering)
- [Security](#security)
- [Shell](#shell)
- [Test](#test)
- [Writing](#writing)

---

## <a name='agile'></a> Agile

### pr-template

> **Description**: Generate a Pull Request template for a repository.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `agile`, `docs`

#### Template Content:
```markdown
# Pull Request Template Generator

Please generate a comprehensive, professional Markdown Pull Request (PR) Template for a repository based on the following project context or requirements:

```
{{args}}
```

Ensure the template includes the following sections, formatted nicely with markdown comments `<!-- -->` to guide the developer:

  ## 1. PR Description
A section prompting the developer to describe the *why* and the *what* of the changes.

  ## 2. Type of Change
A checklist for the developer to categorize the PR (e.g., Bug fix, New feature, Breaking change, Refactoring, Documentation update).

  ## 3. Ticket / Issue Reference
A place to link the Jira ticket, Linear issue, or GitHub Issue (e.g., `Fixes #123`).

  ## 4. Testing & Verification
A section asking the developer to explain how they tested their changes, and a checklist ensuring tests were added/updated.

  ## 5. Deployment / Rollback Plan (If applicable)
A section for DevOps/Backend projects asking about migration scripts, feature flags, or rollback procedures.

  ## 6. Pre-Merge Checklist
A final checklist for the author (e.g., Self-review completed, CI passing, Documentation updated).

Output ONLY the raw markdown template, ready to be saved as `.github/PULL_REQUEST_TEMPLATE.md`.
```

---

### sprint-retrospective

> **Description**: Analyze sprint data and generate a summary.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `agile`

#### Template Content:
```markdown
# Sprint Retrospective Analyzer

Please analyze the following sprint data, team feedback, or bullet points from our recent sprint:

```
{{args}}
```

Synthesize this raw data into a professional, structured Agile Sprint Retrospective report.

  ## 1. Executive Summary
A 2-3 sentence summary of the overall sprint sentiment and major achievements.

  ## 2. What Went Well (The Good)
Group the positive feedback into categorized bullet points.

  ## 3. What Didn't Go Well (The Bad)
Group the negative feedback or struggles into categorized bullet points. Keep the tone blameless and objective.

  ## 4. Process Improvement Opportunities
Identify systemic issues from the data and suggest actionable improvements to the team's Agile process.

  ## 5. Action Items
Generate a clear, numbered list of concrete Action Items to assign to team members for the next sprint, based directly on the feedback provided.
```

---

### ticket-generator

> **Description**: Convert a loose idea into a structured Jira/Linear ticket.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `agile`

#### Template Content:
```markdown
# Ticket / Issue Generator

Please convert the following loose idea, bug report, or feature request into a highly structured, professional engineering ticket (e.g., for Jira, Linear, or GitHub Issues):

```
{{args}}
```

Structure the ticket as follows:

  ## Title
[A clear, concise, actionable title]

  ## 1. User Story / Context
As a [User Persona], I want to [Action/Feature] so that [Value/Benefit].
Provide 1-2 paragraphs of background context.

  ## 2. Acceptance Criteria (DoD)
Provide a clear checklist of conditions that must be met for this ticket to be considered "Done". Use BDD format if appropriate (Given, When, Then).
- [ ] Criterion 1
- [ ] Criterion 2

  ## 3. Technical Implementation Notes
- Proposed architecture or technical approach.
- Specific files, modules, or services that will likely need modification.
- API endpoints to create or alter.

  ## 4. Out of Scope
Explicitly state what is *not* included in this ticket to prevent scope creep.

  ## 5. Dependencies & Blockers
Does this ticket block others? Is it blocked by design, product, or another engineering task?
```

---

## <a name='architecture'></a> Architecture

### design-api

> **Description**: Design RESTful APIs.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`

#### Template Content:
```markdown
# Design RESTful API

Please design a comprehensive RESTful API for the following requirements:

{{args}}

  ## API Design Principles

  ### 1. Resource Modeling

  #### Identify Resources
- What are the main entities?
- What are the relationships?
- What operations are needed?

  #### Resource Naming
- Use nouns, not verbs
- Use plural forms (`/users`, not `/user`)
- Use kebab-case for multi-word resources (`/user-profiles`)
- Keep URLs simple and intuitive

  ### 2. HTTP Methods & Operations

  #### Standard CRUD Operations

**GET - Read/Retrieve**
```
GET /users              - List all users
GET /users/123          - Get specific user
GET /users/123/posts    - Get user's posts
```

**POST - Create**
```
POST /users             - Create new user
POST /users/123/posts   - Create post for user
```

**PUT - Full Update**
```
PUT /users/123          - Replace entire user
```

**PATCH - Partial Update**
```
PATCH /users/123        - Update specific fields
```

**DELETE - Remove**
```
DELETE /users/123       - Delete user
DELETE /users/123/posts/456 - Delete specific post
```

  ### 3. URL Structure

  #### Hierarchy and Nesting
```
/resources
/resources/{id}
/resources/{id}/subresources
/resources/{id}/subresources/{id}
```

**Good Examples:**
```
GET /users/123/orders
GET /posts/456/comments
GET /companies/789/employees
```

**Avoid Deep Nesting:**
```
❌ /users/123/orders/456/items/789/reviews
✅ /order-items/789/reviews
```

  ### 4. Query Parameters

  #### Filtering
```
GET /users?role=admin
GET /posts?author=john&status=published
GET /products?category=electronics&price_min=100&price_max=500
```

  #### Sorting
```
GET /users?sort=created_at:desc
GET /posts?sort=title:asc,created_at:desc
```

  #### Pagination
```
GET /users?page=2&limit=20
GET /users?offset=40&limit=20
```

  #### Field Selection
```
GET /users?fields=id,name,email
```

  #### Search
```
GET /users?q=john
GET /products?search=laptop
```

  ### 5. Request/Response Format

  #### Request Body Example
```json
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "profile": {
    "bio": "Software developer",
    "location": "New York"
  }
}
```

  #### Response Format
```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "role": "admin",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "relationships": {
      "posts": {
        "links": {
          "related": "/users/123/posts"
        }
      }
    }
  },
  "meta": {
    "request_id": "abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

  #### List Response with Pagination
```json
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "total_pages": 5
    }
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}
```

  ### 6. Status Codes

  #### Success Codes
- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST (resource created)
- `202 Accepted` - Request accepted, processing async
- `204 No Content` - Successful DELETE (no response body)

  #### Client Error Codes
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `405 Method Not Allowed` - HTTP method not supported
- `409 Conflict` - Resource conflict (duplicate)
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded

  #### Server Error Codes
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - Invalid response from upstream
- `503 Service Unavailable` - Temporary unavailable
- `504 Gateway Timeout` - Upstream timeout

  ### 7. Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Email must be valid format",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "age",
        "message": "Age must be at least 18",
        "code": "MIN_VALUE"
      }
    ],
    "request_id": "abc123",
    "documentation_url": "https://api.example.com/docs/errors/validation"
  }
}
```

  ### 8. Authentication & Authorization

  #### Authentication Methods
```
Bearer Token:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

API Key:
X-API-Key: your-api-key-here

Basic Auth:
Authorization: Basic base64(username:password)
```

  #### OAuth 2.0 Flow
```
1. GET /oauth/authorize
2. POST /oauth/token
3. Use access_token in requests
4. POST /oauth/refresh (when expired)
```

  ### 9. Versioning

  #### URL Versioning (Recommended)
```
/v1/users
/v2/users
```

  #### Header Versioning
```
Accept: application/vnd.api+json; version=1
API-Version: 1
```

  ### 10. Rate Limiting

  #### Response Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
Retry-After: 3600
```

  #### Rate Limit Response
```json
HTTP/1.1 429 Too Many Requests

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 3600
  }
}
```

  ### 11. HATEOAS (Hypermedia)

```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "status": "active"
  },
  "links": {
    "self": "/users/123",
    "edit": "/users/123",
    "delete": "/users/123",
    "posts": "/users/123/posts",
    "avatar": "/users/123/avatar"
  }
}
```

  ### 12. Caching

  #### Cache Headers
```
Cache-Control: max-age=3600, public
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 15 Jan 2024 10:30:00 GMT
```

  #### Conditional Requests
```
GET /users/123
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

Response: 304 Not Modified (if not changed)
```

  ### 13. Bulk Operations

```
POST /users/bulk
Content-Type: application/json

{
  "operations": [
    { "method": "POST", "path": "/users", "body": {...} },
    { "method": "PATCH", "path": "/users/123", "body": {...} },
    { "method": "DELETE", "path": "/users/456" }
  ]
}
```

  ### 14. Webhooks

```json
POST /webhooks
{
  "url": "https://example.com/webhook",
  "events": ["user.created", "user.updated"],
  "secret": "webhook_secret_key"
}
```

  ### 15. API Documentation Format

Provide for each endpoint:
- HTTP Method & Path
- Description
- Authentication required
- Request parameters
- Request body schema
- Response schema
- Status codes
- Example requests/responses
- Rate limits
- Common errors

  ## Output Format

Provide:

1. **API Overview** - Purpose, base URL, authentication
2. **Resource Models** - Data structures and relationships
3. **Endpoint Specifications** - Complete endpoint documentation
4. **Authentication** - Auth flow and examples
5. **Error Handling** - Error codes and formats
6. **Rate Limiting** - Limits and headers
7. **Versioning Strategy** - How versions are managed
8. **Example Requests** - cURL examples for key operations
9. **OpenAPI/Swagger Spec** - If applicable

Generate complete, production-ready API documentation following REST best practices.
```

---

### design-database

> **Description**: Design database schemas.
> **Input Format**: `SQL Query or Schema`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`, `db`

#### Template Content:
```markdown
# Design Database Schema

Please design a comprehensive database schema for the following requirements:

{{args}}

  ## Database Design Process

  ### 1. Requirements Analysis

  #### Identify Entities
- What are the main data objects?
- What attributes does each entity have?
- What are the cardinalities and relationships?

  #### Identify Operations
- What queries will be most frequent?
- What data needs to be retrieved together?
- What are the access patterns?

  ### 2. Entity-Relationship Modeling

  #### Entity Identification
```
Users
- id (PK)
- email
- name
- created_at

Posts
- id (PK)
- user_id (FK)
- title
- content
- created_at

Comments
- id (PK)
- post_id (FK)
- user_id (FK)
- content
- created_at
```

  #### Relationship Types

**One-to-One (1:1)**
```
User ←→ Profile
One user has one profile
```

**One-to-Many (1:N)**
```
User ←→ Posts
One user has many posts
```

**Many-to-Many (M:N)**
```
Posts ←→ Tags (through PostTags junction table)
Many posts can have many tags
```

  ### 3. Normalization

  #### First Normal Form (1NF)
- Atomic values (no arrays in cells)
- Each column has a unique name
- Order doesn't matter

**Before:**
```
users
id | name  | emails
1  | John  | john@a.com,john@b.com
```

**After:**
```
users
id | name
1  | John

user_emails
id | user_id | email
1  | 1       | john@a.com
2  | 1       | john@b.com
```

  #### Second Normal Form (2NF)
- Must be in 1NF
- No partial dependencies

  #### Third Normal Form (3NF)
- Must be in 2NF
- No transitive dependencies

**Before:**
```
orders
id | product_name | category_name
1  | Laptop       | Electronics
```

**After:**
```
products
id | name   | category_id
1  | Laptop | 1

categories
id | name
1  | Electronics
```

  #### When to Denormalize
- Read-heavy workloads
- Expensive joins
- Aggregated data
- Caching layer exists

  ### 4. Table Design

  #### Primary Keys

**Auto-incrementing Integer**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  -- or
  id INT AUTO_INCREMENT PRIMARY KEY
);
```

**UUID**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);
```

**Composite Key**
```sql
CREATE TABLE post_tags (
  post_id INT,
  tag_id INT,
  PRIMARY KEY (post_id, tag_id)
);
```

  #### Foreign Keys

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
```

**Referential Actions:**
- `CASCADE` - Delete/update related rows
- `SET NULL` - Set FK to NULL
- `RESTRICT` - Prevent deletion
- `NO ACTION` - Check at end of transaction

  #### Indexes

**Single Column Index**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Composite Index**
```sql
CREATE INDEX idx_posts_user_date
  ON posts(user_id, created_at DESC);
```

**Unique Index**
```sql
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

**Partial Index**
```sql
CREATE INDEX idx_active_users
  ON users(email) WHERE active = true;
```

**Full-Text Search Index**
```sql
CREATE INDEX idx_posts_content_fulltext
  ON posts USING GIN(to_tsvector('english', content));
```

  ### 5. Data Types

  #### Common Data Types

**Integers**
```sql
TINYINT     -- 1 byte  (-128 to 127)
SMALLINT    -- 2 bytes (-32K to 32K)
INT         -- 4 bytes (-2B to 2B)
BIGINT      -- 8 bytes (-9 quintillion to 9 quintillion)
```

**Decimals**
```sql
DECIMAL(10,2)  -- Exact: 10 digits, 2 after decimal
FLOAT          -- Approximate 4 bytes
DOUBLE         -- Approximate 8 bytes
```

**Strings**
```sql
CHAR(10)       -- Fixed length
VARCHAR(255)   -- Variable length
TEXT           -- Unlimited length
```

**Date/Time**
```sql
DATE           -- Date only
TIME           -- Time only
DATETIME       -- Date and time
TIMESTAMP      -- Date and time with timezone
```

**Boolean**
```sql
BOOLEAN        -- true/false
```

**JSON**
```sql
JSON           -- JSON data
JSONB          -- Binary JSON (PostgreSQL)
```

  #### Choosing Data Types

**Email:**
```sql
email VARCHAR(255) NOT NULL
```

**Password Hash:**
```sql
password_hash CHAR(60) NOT NULL  -- bcrypt
```

**Money:**
```sql
price DECIMAL(10,2) NOT NULL  -- Exact arithmetic
```

**Status/Enum:**
```sql
status ENUM('draft', 'published', 'archived') NOT NULL
-- or
status VARCHAR(20) CHECK (status IN ('draft', 'published', 'archived'))
```

  ### 6. Schema Patterns

  #### User Authentication
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash CHAR(60) NOT NULL,
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id INT NOT NULL,
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_token ON user_sessions(token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
```

  #### Soft Deletes
```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  deleted_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_deleted ON posts(deleted_at);
```

  #### Audit Trail
```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(50) NOT NULL,
  record_id INT NOT NULL,
  action VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  user_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_audit_table_record ON audit_log(table_name, record_id);
```

  #### Polymorphic Associations
```sql
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  commentable_type VARCHAR(50) NOT NULL,  -- 'Post', 'Photo', etc.
  commentable_id INT NOT NULL,
  content TEXT NOT NULL,
  user_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_comments_polymorphic
  ON comments(commentable_type, commentable_id);
```

  #### Hierarchical Data (Nested Sets)
```sql
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  lft INT NOT NULL,
  rgt INT NOT NULL,
  depth INT NOT NULL
);

CREATE INDEX idx_categories_lft_rgt ON categories(lft, rgt);
```

  #### Tags/Categories (Many-to-Many)
```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
  post_id INT NOT NULL,
  tag_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (post_id, tag_id),
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE INDEX idx_post_tags_tag ON post_tags(tag_id);
```

  ### 7. Constraints

  #### NOT NULL
```sql
email VARCHAR(255) NOT NULL
```

  #### UNIQUE
```sql
email VARCHAR(255) UNIQUE NOT NULL
```

  #### CHECK
```sql
age INT CHECK (age >= 0 AND age <= 150)
price DECIMAL(10,2) CHECK (price > 0)
status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'banned'))
```

  #### DEFAULT
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
is_active BOOLEAN DEFAULT TRUE
role VARCHAR(20) DEFAULT 'user'
```

  ### 8. Performance Considerations

  #### Query Optimization
```sql
-- Good: Uses index on user_id
SELECT * FROM posts WHERE user_id = 123;

-- Bad: Function on indexed column prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- Good: Store lowercase email separately or use functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

  #### Covering Indexes
```sql
-- Query needs id, user_id, created_at
CREATE INDEX idx_posts_covering
  ON posts(user_id, created_at, id);
```

  #### Partitioning
```sql
CREATE TABLE events (
  id SERIAL,
  user_id INT,
  event_date DATE,
  data JSONB
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

  ### 9. Database Schema Documentation

  #### Table Documentation Template

```markdown
### Table: users

**Description**: Stores user account information

**Columns:**
| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | NO | AUTO | Primary key |
| email | VARCHAR(255) | NO | - | User email (unique) |
| name | VARCHAR(100) | NO | - | Full name |
| password_hash | CHAR(60) | NO | - | Bcrypt hash |
| created_at | TIMESTAMP | NO | NOW() | Creation timestamp |

**Indexes:**
- PRIMARY KEY: id
- UNIQUE: email
- INDEX: created_at

**Foreign Keys:**
- None

**Referenced By:**
- posts.user_id
- comments.user_id

**Constraints:**
- email must be unique
- email format validated at app level
```

  ### 10. Migration Strategy

```sql
-- Version 1: Initial schema
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL
);

-- Version 2: Add username
ALTER TABLE users ADD COLUMN username VARCHAR(50) UNIQUE;

-- Version 3: Make username required (with default for existing)
UPDATE users SET username = email WHERE username IS NULL;
ALTER TABLE users ALTER COLUMN username SET NOT NULL;
```

  ### 11. Output Format

Provide:

1. **ER Diagram** (text/ASCII format)
2. **Table Definitions** (CREATE TABLE statements)
3. **Indexes** (CREATE INDEX statements)
4. **Relationships** (Foreign keys and descriptions)
5. **Sample Data** (INSERT statements for testing)
6. **Common Queries** (Optimized SELECT examples)
7. **Migration Plan** (For evolving schema)
8. **Performance Notes** (Index strategy, partitioning)
9. **Data Dictionary** (Complete table/column documentation)

Generate complete, production-ready database schema following best practices.
```

---

### design-patterns

> **Description**: Suggest appropriate design patterns.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`

#### Template Content:
```markdown
# Suggest Design Patterns

Please analyze the following code/requirements and suggest appropriate design patterns:

{{args}}

  ## Design Pattern Analysis Framework

  ### 1. Problem Identification

First, identify what problems exist in the code:
- Code duplication
- Tight coupling
- Hard to test
- Difficult to extend
- Complex conditionals
- Unclear responsibilities
- Global state issues
- Object creation complexity

  ### 2. Creational Patterns

  #### Factory Pattern
**When to use:**
- Object creation logic is complex
- Need to create different types of objects
- Want to decouple object creation from usage

**Before:**
```javascript
class UserService {
  createUser(type) {
    if (type === 'admin') {
      return new AdminUser();
    } else if (type === 'customer') {
      return new CustomerUser();
    } else if (type === 'guest') {
      return new GuestUser();
    }
  }
}
```

**After:**
```javascript
class UserFactory {
  static createUser(type) {
    const users = {
      admin: AdminUser,
      customer: CustomerUser,
      guest: GuestUser
    };

    const UserClass = users[type];
    if (!UserClass) {
      throw new Error(`Unknown user type: ${type}`);
    }

    return new UserClass();
  }
}

// Usage
const user = UserFactory.createUser('admin');
```

  #### Builder Pattern
**When to use:**
- Object has many optional parameters
- Step-by-step object construction
- Want immutable objects

**Example:**
```javascript
class QueryBuilder {
  constructor() {
    this.query = {};
  }

  select(...fields) {
    this.query.select = fields;
    return this;
  }

  from(table) {
    this.query.from = table;
    return this;
  }

  where(conditions) {
    this.query.where = conditions;
    return this;
  }

  build() {
    return this.query;
  }
}

// Usage
const query = new QueryBuilder()
  .select('id', 'name', 'email')
  .from('users')
  .where({ active: true })
  .build();
```

  #### Singleton Pattern
**When to use:**
- Need exactly one instance (database connection, logger)
- Global access point needed
- **Warning**: Often an anti-pattern; consider dependency injection instead

**Example:**
```javascript
class Database {
  constructor() {
    if (Database.instance) {
      return Database.instance;
    }
    this.connection = null;
    Database.instance = this;
  }

  connect() {
    if (!this.connection) {
      this.connection = createConnection();
    }
    return this.connection;
  }
}

// Usage
const db1 = new Database();
const db2 = new Database();
// db1 === db2 (same instance)
```

  #### Prototype Pattern
**When to use:**
- Object creation is expensive
- Need to clone objects

**Example:**
```javascript
class GameCharacter {
  constructor(config) {
    this.health = config.health;
    this.strength = config.strength;
    this.inventory = config.inventory;
  }

  clone() {
    return new GameCharacter({
      health: this.health,
      strength: this.strength,
      inventory: [...this.inventory]
    });
  }
}
```

  ### 3. Structural Patterns

  #### Adapter Pattern
**When to use:**
- Make incompatible interfaces work together
- Integrate third-party libraries
- Legacy code integration

**Example:**
```javascript
// Old interface
class OldPaymentProcessor {
  processPayment(amount) {
    return `Processing $${amount}`;
  }
}

// New interface expected by our code
class PaymentAdapter {
  constructor(processor) {
    this.processor = processor;
  }

  pay(paymentDetails) {
    return this.processor.processPayment(paymentDetails.amount);
  }
}

// Usage
const oldProcessor = new OldPaymentProcessor();
const adapter = new PaymentAdapter(oldProcessor);
adapter.pay({ amount: 100, currency: 'USD' });
```

  #### Decorator Pattern
**When to use:**
- Add functionality dynamically
- Extend object behavior
- Alternative to subclassing

**Example:**
```javascript
class Coffee {
  cost() {
    return 5;
  }
}

class MilkDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  cost() {
    return this.coffee.cost() + 1;
  }
}

class SugarDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  cost() {
    return this.coffee.cost() + 0.5;
  }
}

// Usage
let coffee = new Coffee();
coffee = new MilkDecorator(coffee);
coffee = new SugarDecorator(coffee);
console.log(coffee.cost()); // 6.5
```

  #### Facade Pattern
**When to use:**
- Simplify complex subsystems
- Provide unified interface
- Reduce coupling

**Example:**
```javascript
// Complex subsystem
class CPU {
  freeze() { /* ... */ }
  execute() { /* ... */ }
}

class Memory {
  load() { /* ... */ }
}

class HardDrive {
  read() { /* ... */ }
}

// Facade
class Computer {
  constructor() {
    this.cpu = new CPU();
    this.memory = new Memory();
    this.hardDrive = new HardDrive();
  }

  start() {
    this.cpu.freeze();
    this.memory.load();
    this.hardDrive.read();
    this.cpu.execute();
  }
}

// Usage (simple!)
const computer = new Computer();
computer.start();
```

  #### Proxy Pattern
**When to use:**
- Control access to objects
- Lazy loading
- Logging/caching
- Access control

**Example:**
```javascript
class DatabaseQuery {
  execute(query) {
    // Expensive operation
    return performQuery(query);
  }
}

class CachingProxy {
  constructor(database) {
    this.database = database;
    this.cache = new Map();
  }

  execute(query) {
    if (this.cache.has(query)) {
      console.log('Cache hit');
      return this.cache.get(query);
    }

    console.log('Cache miss');
    const result = this.database.execute(query);
    this.cache.set(query, result);
    return result;
  }
}
```

  #### Composite Pattern
**When to use:**
- Tree structures
- Part-whole hierarchies
- Treat individual objects and compositions uniformly

**Example:**
```javascript
class File {
  constructor(name) {
    this.name = name;
  }

  getSize() {
    return 100; // KB
  }
}

class Folder {
  constructor(name) {
    this.name = name;
    this.children = [];
  }

  add(child) {
    this.children.push(child);
  }

  getSize() {
    return this.children.reduce((total, child) => {
      return total + child.getSize();
    }, 0);
  }
}

// Usage
const root = new Folder('root');
root.add(new File('file1'));
const subfolder = new Folder('subfolder');
subfolder.add(new File('file2'));
root.add(subfolder);
console.log(root.getSize()); // 200
```

  ### 4. Behavioral Patterns

  #### Strategy Pattern
**When to use:**
- Multiple algorithms for same task
- Eliminate conditionals
- Make algorithms interchangeable

**Before:**
```javascript
function calculateShipping(type, weight) {
  if (type === 'express') {
    return weight * 5;
  } else if (type === 'standard') {
    return weight * 2;
  } else if (type === 'economy') {
    return weight * 1;
  }
}
```

**After:**
```javascript
class ExpressShipping {
  calculate(weight) {
    return weight * 5;
  }
}

class StandardShipping {
  calculate(weight) {
    return weight * 2;
  }
}

class EconomyShipping {
  calculate(weight) {
    return weight * 1;
  }
}

class ShippingCalculator {
  constructor(strategy) {
    this.strategy = strategy;
  }

  calculate(weight) {
    return this.strategy.calculate(weight);
  }
}

// Usage
const calculator = new ShippingCalculator(new ExpressShipping());
console.log(calculator.calculate(10)); // 50
```

  #### Observer Pattern
**When to use:**
- One-to-many dependencies
- Event systems
- Pub-sub systems

**Example:**
```javascript
class EventEmitter {
  constructor() {
    this.listeners = {};
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }
}

// Usage
const emitter = new EventEmitter();
emitter.on('user:created', (user) => {
  console.log('Send welcome email to', user.email);
});
emitter.on('user:created', (user) => {
  console.log('Log user creation:', user.id);
});

emitter.emit('user:created', { id: 1, email: 'user@example.com' });
```

  #### Command Pattern
**When to use:**
- Encapsulate requests as objects
- Undo/redo functionality
- Queue operations
- Logging operations

**Example:**
```javascript
class Command {
  execute() {}
  undo() {}
}

class AddTextCommand extends Command {
  constructor(editor, text) {
    super();
    this.editor = editor;
    this.text = text;
  }

  execute() {
    this.editor.addText(this.text);
  }

  undo() {
    this.editor.removeText(this.text.length);
  }
}

class CommandHistory {
  constructor() {
    this.history = [];
  }

  execute(command) {
    command.execute();
    this.history.push(command);
  }

  undo() {
    const command = this.history.pop();
    if (command) {
      command.undo();
    }
  }
}
```

  #### Template Method Pattern
**When to use:**
- Define algorithm skeleton
- Let subclasses override specific steps
- Code reuse in similar algorithms

**Example:**
```javascript
class DataParser {
  parse(data) {
    const raw = this.readData(data);
    const processed = this.processData(raw);
    return this.formatOutput(processed);
  }

  readData(data) {
    // Common implementation
    return data;
  }

  processData(data) {
    // Override in subclass
    throw new Error('Must implement processData');
  }

  formatOutput(data) {
    // Common implementation
    return JSON.stringify(data);
  }
}

class CSVParser extends DataParser {
  processData(data) {
    return data.split(',').map(item => item.trim());
  }
}

class XMLParser extends DataParser {
  processData(data) {
    // XML-specific processing
    return parseXML(data);
  }
}
```

  #### Chain of Responsibility
**When to use:**
- Multiple handlers for a request
- Handler selection at runtime
- Middleware pattern

**Example:**
```javascript
class AuthMiddleware {
  setNext(middleware) {
    this.next = middleware;
    return middleware;
  }

  handle(request) {
    if (this.next) {
      return this.next.handle(request);
    }
    return true;
  }
}

class Authentication extends AuthMiddleware {
  handle(request) {
    if (!request.token) {
      throw new Error('No token');
    }
    return super.handle(request);
  }
}

class Authorization extends AuthMiddleware {
  handle(request) {
    if (!request.hasPermission) {
      throw new Error('No permission');
    }
    return super.handle(request);
  }
}

// Usage
const auth = new Authentication();
const authz = new Authorization();
auth.setNext(authz);

auth.handle({ token: 'xyz', hasPermission: true });
```

  ### 5. Pattern Selection Guide

  #### For Object Creation Issues
- Too many constructor parameters → **Builder**
- Complex object creation logic → **Factory**
- Need to clone objects → **Prototype**
- Need single instance → **Singleton** (use cautiously)

  #### For Code Structure Issues
- Incompatible interfaces → **Adapter**
- Need to add features → **Decorator**
- Complex subsystem → **Facade**
- Control access → **Proxy**
- Part-whole hierarchy → **Composite**

  #### For Behavior Issues
- Multiple algorithms → **Strategy**
- Event handling → **Observer**
- Undo/redo → **Command**
- Request handlers → **Chain of Responsibility**
- Algorithm skeleton → **Template Method**

  ### 6. Output Format

For each recommended pattern, provide:

1. **Pattern Name** and category
2. **Problem** it solves in this specific code
3. **Benefits** of applying it here
4. **Before Code** (current implementation)
5. **After Code** (with pattern applied)
6. **Trade-offs** (complexity, performance)
7. **Testing** considerations
8. **When NOT to use** this pattern

Generate comprehensive design pattern recommendations following this structure.
```

---

### system-architecture

> **Description**: Design system architecture.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`

#### Template Content:
```markdown
# System Architecture Design

Please design a comprehensive system architecture for the following requirements:

{{args}}

  ## System Design Framework

  ### 1. Requirements Clarification

  #### Functional Requirements
- What features/capabilities are needed?
- What are the core use cases?
- What are the user workflows?

  #### Non-Functional Requirements
- **Performance**: Response time, throughput targets
- **Scalability**: Expected user/data growth
- **Availability**: Uptime requirements (99.9%, 99.99%)
- **Reliability**: Data durability, fault tolerance
- **Consistency**: Strong vs eventual consistency
- **Security**: Authentication, encryption, compliance
- **Maintainability**: Code quality, deployment ease

  #### Constraints
- Budget limitations
- Technology restrictions
- Timeline constraints
- Team expertise

  ### 2. Capacity Estimation

  #### Traffic Estimates
```
Daily Active Users (DAU): 1M
Requests per user per day: 50
Total daily requests: 50M
Requests per second (RPS): 50M / 86400 ≈ 580 RPS
Peak RPS (3x average): ~1740 RPS
```

  #### Storage Estimates
```
Average data per user: 1KB
Total users: 10M
Total storage: 10GB
Storage growth: 1GB/month
5-year projection: 10GB + (60 months × 1GB) = 70GB
```

  #### Bandwidth Estimates
```
Average request size: 1KB
Average response size: 5KB
Total bandwidth: (580 RPS × 6KB) = 3.5 MB/s
```

  #### Memory/Cache Estimates
```
Cache 20% of hot data: 2GB
Session storage: 100MB per 10K concurrent users
```

  ### 3. High-Level Architecture

  #### Architecture Diagram (Text Format)
```
                    ┌──────────────┐
                    │    Client    │
                    │  (Web/Mobile)│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │     CDN      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
      │  Web      │  │  Web      │  │  Web      │
      │  Server 1 │  │  Server 2 │  │  Server 3 │
      └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
            │              │              │
            └──────────────┼──────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
      │   Cache   │  │ Message   │  │  Search   │
      │  (Redis)  │  │   Queue   │  │(Elastic)  │
      └───────────┘  └─────┬─────┘  └───────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
      │  Primary  │  │  Read     │  │  Object   │
      │  Database │  │  Replica  │  │  Storage  │
      └───────────┘  └───────────┘  └───────────┘
```

  ### 4. Component Design

  #### Load Balancer
- **Purpose**: Distribute traffic across servers
- **Options**: AWS ALB, Nginx, HAProxy
- **Strategies**: Round-robin, least connections, IP hash
- **Health checks**: Regular server health monitoring

  #### Web/Application Servers
- **Stateless design**: No session data on servers
- **Horizontal scaling**: Add more servers as needed
- **Auto-scaling**: Scale based on CPU/memory metrics

  #### Caching Layer
- **Technology**: Redis, Memcached
- **What to cache**:
  - Frequently accessed data
  - Expensive computations
  - Session data
  - API responses
- **Cache strategies**:
  - Cache-aside (lazy loading)
  - Write-through
  - Write-behind
- **TTL**: Appropriate expiration times
- **Cache invalidation**: Clear when data changes

  #### Database
- **Primary-Replica setup**:
  - Write to primary
  - Read from replicas
- **Partitioning/Sharding**:
  - Horizontal: Split by user_id range
  - Vertical: Split by table/feature
- **Indexing**: For query optimization
- **Connection pooling**: Reuse connections

  #### Message Queue
- **Technology**: RabbitMQ, Kafka, AWS SQS
- **Use cases**:
  - Async processing
  - Event-driven architecture
  - Decoupling services
- **Patterns**:
  - Producer-Consumer
  - Pub-Sub
  - Request-Reply

  #### Object Storage
- **Technology**: AWS S3, Google Cloud Storage
- **Use cases**:
  - Images, videos, files
  - Backups
  - Logs
- **CDN integration**: Fast global access

  ### 5. Data Flow

  #### Read Flow
```
1. Client → CDN (if static content)
2. Client → Load Balancer
3. Load Balancer → Web Server
4. Web Server → Check Cache
   ├─ Cache Hit → Return data
   └─ Cache Miss → Query Database
       └─ Store in Cache → Return data
```

  #### Write Flow
```
1. Client → Load Balancer
2. Load Balancer → Web Server
3. Web Server → Validate data
4. Web Server → Write to Primary DB
5. Web Server → Invalidate cache
6. Web Server → Publish event to queue
7. Background worker → Process event
8. Return response to client
```

  ### 6. Scalability Strategies

  #### Horizontal Scaling
- Add more servers/instances
- Load balancer distributes traffic
- Stateless application design required

  #### Vertical Scaling
- Increase server resources (CPU, RAM)
- Limited by hardware constraints
- Temporary solution

  #### Database Scaling
- **Read scaling**: Add read replicas
- **Write scaling**: Sharding/partitioning
- **Caching**: Reduce DB load
- **NoSQL**: For specific use cases

  #### Microservices
Split monolith into services:
- User Service
- Auth Service
- Product Service
- Order Service
- Payment Service

Each service:
- Independent deployment
- Own database
- Specific responsibility

  ### 7. Availability & Reliability

  #### Redundancy
- Multiple servers in load balancer
- Database replicas
- Multi-region deployment
- Backup systems

  #### Fault Tolerance
- Graceful degradation
- Circuit breakers
- Retry logic with exponential backoff
- Timeout configuration

  #### Disaster Recovery
- Regular backups
- Backup in different region
- Recovery Time Objective (RTO)
- Recovery Point Objective (RPO)

  #### Monitoring
- **Metrics**: CPU, memory, response time, error rate
- **Logging**: Centralized logging (ELK stack)
- **Alerting**: PagerDuty, email, Slack
- **Dashboards**: Grafana, Datadog

  ### 8. Security Architecture

  #### Network Security
- VPC/Private subnets
- Security groups/Firewall rules
- DDoS protection (Cloudflare, AWS Shield)

  #### Application Security
- HTTPS/TLS encryption
- Authentication (JWT, OAuth)
- Authorization (RBAC, ABAC)
- Input validation
- SQL injection prevention
- XSS prevention
- CSRF protection

  #### Data Security
- Encryption at rest
- Encryption in transit
- Key management (AWS KMS)
- PII data handling
- Audit logging

  ### 9. API Gateway Pattern

```
Client → API Gateway → Microservices
```

**API Gateway responsibilities:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Request/response transformation
- Caching
- Monitoring & logging

  ### 10. Caching Strategies

  #### CDN Caching
- Static assets (JS, CSS, images)
- Geo-distributed
- Edge caching

  #### Application Caching
- Redis/Memcached
- Session data
- API responses
- Database query results

  #### Browser Caching
- Cache-Control headers
- ETags
- Service Workers

  ### 11. Async Processing Pattern

```
Web Server → Message Queue → Worker
```

**Use cases:**
- Email sending
- Image processing
- Report generation
- Data analytics
- Video encoding

  ### 12. Data Consistency

  #### Strong Consistency
- ACID transactions
- Immediate consistency
- Use for: Financial transactions, inventory

  #### Eventual Consistency
- BASE properties
- Higher availability
- Use for: Social media feeds, analytics

  #### Patterns
- Two-Phase Commit
- Saga Pattern
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)

  ### 13. Rate Limiting

  #### Strategies
- Fixed window
- Sliding window
- Token bucket
- Leaky bucket

  #### Implementation
```
Rate Limit: 100 requests per minute per user
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640000000
```

  ### 14. Technology Stack Recommendations

Based on requirements, suggest:

  #### Frontend
- Framework: React, Vue, Angular
- Mobile: React Native, Flutter
- State Management: Redux, MobX

  #### Backend
- Language: Node.js, Python, Java, Go
- Framework: Express, Django, Spring Boot
- API: REST, GraphQL, gRPC

  #### Database
- Relational: PostgreSQL, MySQL
- NoSQL: MongoDB, DynamoDB
- Cache: Redis, Memcached
- Search: Elasticsearch

  #### Infrastructure
- Cloud: AWS, GCP, Azure
- Containers: Docker, Kubernetes
- CI/CD: GitHub Actions, Jenkins

  ### 15. Output Format

Provide:

1. **Architecture Overview** - High-level description
2. **Architecture Diagram** - Component relationships
3. **Component Specifications** - Detailed component design
4. **Data Flow** - Request/response flows
5. **Scaling Strategy** - How to handle growth
6. **Fault Tolerance** - Redundancy and recovery
7. **Security Measures** - Security architecture
8. **Technology Stack** - Recommended technologies
9. **Capacity Planning** - Traffic/storage estimates
10. **Trade-offs** - Design decisions and rationale
11. **Deployment Strategy** - How to deploy and maintain

Generate a complete, production-ready system architecture following best practices.
```

---

### threat-modeling

> **Description**: Generate a STRIDE threat model for a proposed architecture.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`, `security`

#### Template Content:
```markdown
# Threat Modeling (STRIDE)

Please generate a comprehensive threat model using the STRIDE methodology for the following proposed architecture/system:

```
{{args}}
```

Provide your analysis in the following structured format:

  ## 1. System Overview
Provide a brief summary of the system components and data flow based on the provided description.

  ## 2. STRIDE Analysis
Analyze the system across the 6 STRIDE categories. For each category, identify at least 2 potential threats.
- **Spoofing (Authenticity):** Can an attacker impersonate a user or service?
- **Tampering (Integrity):** Can data be modified in transit or at rest?
- **Repudiation (Non-repudiability):** Can a user perform an action without a trace?
- **Information Disclosure (Confidentiality):** Can sensitive data be exposed?
- **Denial of Service (Availability):** Can the system be brought down or degraded?
- **Elevation of Privilege (Authorization):** Can an unprivileged user gain admin access?

  ## 3. Risk Assessment & Mitigations
For each identified threat, provide:
1. **Risk Level:** (Critical, High, Medium, Low)
2. **Mitigation Strategy:** Concrete technical or architectural steps to resolve or mitigate the threat.

  ## 4. Key Security Recommendations
Summarize the top 3-5 security priorities the development team must focus on before releasing this system.
```

---

## <a name='code-review'></a> Code Review

### code-review-best-practices

> **Description**: General best practices review.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`

#### Template Content:
```markdown
# Best Practices Code Review

Please perform a comprehensive best practices review of the following code:

```
{{args}}
```

Focus on:

  ## 1. Code Style & Readability
- Is the code following language/framework conventions?
- Are naming conventions clear and consistent?
- Is the code self-documenting?
- Are comments helpful and up-to-date?
- Is indentation and formatting consistent?

  ## 2. Code Organization
- Is code properly modularized?
- Is separation of concerns respected?
- Are functions/methods single-purpose?
- Is the file/folder structure logical?
- Is code duplication minimized (DRY principle)?

  ## 3. Error Handling
- Are errors handled gracefully?
- Are error messages helpful?
- Is there proper logging?
- Are edge cases considered?
- Is defensive programming used appropriately?

  ## 4. Testing & Testability
- Is the code testable?
- Are dependencies injectable?
- Are side effects isolated?
- Is test coverage adequate?
- Are tests meaningful?

  ## 5. Maintainability
- Will this code be easy to modify?
- Is technical debt being introduced?
- Are magic numbers/strings avoided?
- Is configuration externalized?
- Is documentation adequate?

  ## 6. SOLID Principles
- Single Responsibility: Does each unit have one clear purpose?
- Open/Closed: Is code open for extension, closed for modification?
- Liskov Substitution: Are inheritance hierarchies correct?
- Interface Segregation: Are interfaces focused?
- Dependency Inversion: Are abstractions used properly?

  ## 7. Language/Framework Specific
- Are modern language features used appropriately?
- Are framework best practices followed?
- Are deprecated APIs avoided?
- Are appropriate design patterns used?

  ## 8. Scalability & Future-Proofing
- Will this code scale with growth?
- Is it flexible for future requirements?
- Are assumptions documented?

Provide:
1. **Critical Issues**: Must-fix problems
2. **High Priority**: Important improvements
3. **Medium Priority**: Recommended changes
4. **Low Priority**: Nice-to-have enhancements
5. **Code Examples**: Show improved versions following best practices

For each issue, explain:
- What the problem is
- Why it violates best practices
- What principle/pattern to apply
- How to refactor it
- Benefits of the improvement
```

---

### code-review-performance

> **Description**: Performance optimization suggestions.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`

#### Template Content:
```markdown
# Performance Code Review

Please perform a comprehensive performance analysis of the following code:

```
{{args}}
```

Focus on:

  ## 1. Algorithmic Complexity
- Identify time complexity (Big O notation) of key operations
- Identify space complexity issues
- Are there more efficient algorithms or data structures?
- Look for nested loops, redundant calculations

  ## 2. Memory Management
- Are there memory leaks or unnecessary allocations?
- Can objects be reused or pooled?
- Are large objects held in memory unnecessarily?
- Is garbage collection pressure minimized?

  ## 3. I/O Operations
- Are I/O operations batched or optimized?
- Can operations be done asynchronously?
- Are there unnecessary file reads/writes?
- Is caching used effectively?

  ## 4. Database & Query Performance
- Are queries optimized with proper indexes?
- Is there N+1 query problem?
- Are connections pooled?
- Can queries be batched or consolidated?

  ## 5. Rendering & UI Performance
- Are unnecessary re-renders happening?
- Is virtual scrolling used for long lists?
- Are expensive operations memoized?
- Is lazy loading implemented where appropriate?

  ## 6. Network Performance
- Are API calls optimized and batched?
- Is data prefetching used?
- Are responses properly cached?
- Is compression enabled?

  ## 7. Code Patterns
- Are there premature optimizations?
- Is code clarity sacrificed unnecessarily?
- Are there blocking operations in hot paths?

Provide:
1. **Critical Issues**: Performance bottlenecks causing significant problems
2. **High Priority**: Substantial performance improvements
3. **Medium Priority**: Moderate optimizations
4. **Low Priority**: Minor refinements
5. **Code Examples**: Show optimized alternatives with performance comparisons

For each issue, explain:
- What the performance problem is
- Why it's inefficient
- Expected performance impact
- How to optimize it
- Benchmarks or measurements where relevant
```

---

### code-review-security

> **Description**: Deep security analysis of code.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`, `security`

#### Template Content:
```markdown
# Security Code Review

Please perform a comprehensive security analysis of the following code:

```
{{args}}
```

Focus on:

  ## 1. Input Validation & Sanitization
- Are all user inputs properly validated?
- Is input sanitized before use in queries, commands, or rendering?
- Are there risks of injection attacks (SQL, XSS, command injection)?

  ## 2. Authentication & Authorization
- Are authentication mechanisms secure?
- Is authorization properly enforced?
- Are credentials handled securely?
- Is session management secure?

  ## 3. Data Protection
- Is sensitive data encrypted at rest and in transit?
- Are secrets and API keys properly managed?
- Is PII (Personally Identifiable Information) handled correctly?

  ## 4. Common Vulnerabilities
- Check for OWASP Top 10 vulnerabilities
- Look for race conditions and TOCTOU issues
- Identify potential buffer overflows or memory issues
- Check for insecure dependencies

  ## 5. Error Handling & Logging
- Are errors handled without exposing sensitive information?
- Is logging done securely without leaking secrets?
- Are stack traces exposed in production?

  ## 6. Access Control
- Are file permissions appropriate?
- Is path traversal prevented?
- Are resources properly scoped and isolated?

Provide:
1. **Critical Issues**: Vulnerabilities that must be fixed immediately
2. **High Priority**: Significant security concerns
3. **Medium Priority**: Security improvements
4. **Best Practices**: General security recommendations
5. **Code Examples**: Show secure alternatives for each issue

For each issue, explain:
- What the vulnerability is
- Why it's dangerous
- How to fix it
- Example of secure code
```

---

### explain-code

> **Description**: Detailed code explanation.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`

#### Template Content:
```markdown
# Comprehensive Code Explanation

Please provide a detailed, structured explanation of the following code:

```
{{args}}
```

Provide your analysis in the following format:

  ## 1. High-Level Summary
- What is the primary purpose of this code? (1-2 sentences)
- What problem does it solve?

  ## 2. Logic & Control Flow
- Break down the logic step-by-step.
- Explain the key algorithms or data structures used.
- How does data flow into and out of this component?

  ## 3. Dependencies & Context
- What external libraries, APIs, or internal modules does this code seem to rely on?
- What assumptions does this code make about its environment or inputs?

  ## 4. Edge Cases & Potential Pitfalls
- Are there any non-obvious edge cases this code handles (or fails to handle)?
- What happens with null, undefined, or unexpected inputs?
- Are there any potential performance bottlenecks or memory leaks?

  ## 5. Key Takeaways
- Summarize the most important things a developer should remember when working with or modifying this code.
```

---

### refactor-suggestions

> **Description**: Code refactoring recommendations.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`

#### Template Content:
```markdown
# Code Refactoring Suggestions

Please analyze the following code and provide refactoring recommendations:

```
{{args}}
```

Focus on:

  ## 1. Code Smells
Identify and suggest fixes for:
- Long methods/functions (>20-30 lines)
- Long parameter lists (>3-4 parameters)
- Duplicated code
- Large classes/modules
- Primitive obsession
- Feature envy
- Data clumps
- Switch/conditional complexity

  ## 2. Design Patterns
Suggest appropriate design patterns:
- Can Strategy pattern replace conditionals?
- Would Factory pattern improve object creation?
- Is Observer pattern needed for events?
- Should Decorator pattern be used?
- Would Adapter pattern help integration?
- Is Singleton appropriate (or anti-pattern)?

  ## 3. Simplification Opportunities
- Can complex conditionals be simplified?
- Are there opportunities to use guard clauses?
- Can nested structures be flattened?
- Should temporary variables be eliminated?
- Can expression complexity be reduced?

  ## 4. Extract & Compose
- Methods that should be extracted
- Classes that should be split
- Modules that should be separated
- Utilities that should be shared
- Constants that should be defined

  ## 5. Naming Improvements
- Variables with unclear names
- Functions that don't describe what they do
- Classes with vague or misleading names
- Naming inconsistencies

  ## 6. Dependency Management
- Dependencies that should be inverted
- Coupling that should be reduced
- Cohesion that should be improved
- Circular dependencies to eliminate

  ## 7. Modern Code Practices
- Legacy patterns to modernize
- Functional programming opportunities
- Async/await over callbacks
- Modern syntax improvements
- Type safety enhancements

  ## 8. Architecture Improvements
- Layer violations to fix
- Separation of concerns issues
- API design improvements
- State management enhancements

Provide:
1. **High Impact Refactorings**: Most valuable changes
2. **Medium Impact**: Worthwhile improvements
3. **Low Impact**: Polish and minor enhancements
4. **Before/After Examples**: Show concrete refactoring steps
5. **Step-by-Step Guide**: Safe refactoring sequence
6. **Tests to Write**: What to test before/during refactoring

For each refactoring, explain:
- What needs to change
- Why it's beneficial
- How to refactor safely
- What tests to have in place
- Expected improvement in maintainability
```

---

### suggest-fixes

> **Description**: Suggest potential bug fixes and improvements for code.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`, `debug`

#### Template Content:
```markdown
# Suggest Bug Fixes
Please analyze the following code and suggest potential fixes and improvements: 
```
{{args}}
```
Focus on: 
  ## 1. Correctness & Reliability
- Identify any logical errors, off-by-one errors, or incorrect assumptions.
- Check for potential memory leaks, resource leaks, or race conditions.
- Ensure that edge cases and error conditions are handled correctly.
  ## 2. Performance & Efficiency
- Look for areas where the code could be more efficient or performant.
- Identify any unnecessary computations, redundant data copies, or inefficient algorithms.
- Suggest ways to optimize resource usage and reduce latency.
  ## 3. Readability & Maintainability
- Recommend improvements to code structure, naming conventions, and organization.
- Suggest ways to make the code more concise, clear, and easy to understand.
- Identify opportunities for refactoring and simplification.
  ## 4. Security & Robustness
- Check for common security vulnerabilities (e.g., injection, XSS, buffer overflows).
- Ensure that sensitive data is handled securely and that inputs are properly validated.
- Suggest ways to make the code more robust and resilient to failures.
  ## 5. Best Practices & Idioms
- Recommend the use of more modern or idiomatic language features and libraries.
- Suggest ways to follow established coding standards and best practices.
For each suggested fix or improvement, provide:
1. **Description of the Issue**: What is wrong or could be better?
2. **Impact**: Why is it important to fix or improve this?
3. **Suggested Change**: Provide a clear explanation and code example of the proposed fix.
4. **Alternative Approaches**: Are there other ways to achieve the same result?
Provide a comprehensive and actionable set of recommendations that will help improve the overall quality and reliability of the code.
```

---

## <a name='db'></a> Db

### design-database

> **Description**: Design database schemas.
> **Input Format**: `SQL Query or Schema`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`, `db`

#### Template Content:
```markdown
# Design Database Schema

Please design a comprehensive database schema for the following requirements:

{{args}}

  ## Database Design Process

  ### 1. Requirements Analysis

  #### Identify Entities
- What are the main data objects?
- What attributes does each entity have?
- What are the cardinalities and relationships?

  #### Identify Operations
- What queries will be most frequent?
- What data needs to be retrieved together?
- What are the access patterns?

  ### 2. Entity-Relationship Modeling

  #### Entity Identification
```
Users
- id (PK)
- email
- name
- created_at

Posts
- id (PK)
- user_id (FK)
- title
- content
- created_at

Comments
- id (PK)
- post_id (FK)
- user_id (FK)
- content
- created_at
```

  #### Relationship Types

**One-to-One (1:1)**
```
User ←→ Profile
One user has one profile
```

**One-to-Many (1:N)**
```
User ←→ Posts
One user has many posts
```

**Many-to-Many (M:N)**
```
Posts ←→ Tags (through PostTags junction table)
Many posts can have many tags
```

  ### 3. Normalization

  #### First Normal Form (1NF)
- Atomic values (no arrays in cells)
- Each column has a unique name
- Order doesn't matter

**Before:**
```
users
id | name  | emails
1  | John  | john@a.com,john@b.com
```

**After:**
```
users
id | name
1  | John

user_emails
id | user_id | email
1  | 1       | john@a.com
2  | 1       | john@b.com
```

  #### Second Normal Form (2NF)
- Must be in 1NF
- No partial dependencies

  #### Third Normal Form (3NF)
- Must be in 2NF
- No transitive dependencies

**Before:**
```
orders
id | product_name | category_name
1  | Laptop       | Electronics
```

**After:**
```
products
id | name   | category_id
1  | Laptop | 1

categories
id | name
1  | Electronics
```

  #### When to Denormalize
- Read-heavy workloads
- Expensive joins
- Aggregated data
- Caching layer exists

  ### 4. Table Design

  #### Primary Keys

**Auto-incrementing Integer**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  -- or
  id INT AUTO_INCREMENT PRIMARY KEY
);
```

**UUID**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);
```

**Composite Key**
```sql
CREATE TABLE post_tags (
  post_id INT,
  tag_id INT,
  PRIMARY KEY (post_id, tag_id)
);
```

  #### Foreign Keys

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
```

**Referential Actions:**
- `CASCADE` - Delete/update related rows
- `SET NULL` - Set FK to NULL
- `RESTRICT` - Prevent deletion
- `NO ACTION` - Check at end of transaction

  #### Indexes

**Single Column Index**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Composite Index**
```sql
CREATE INDEX idx_posts_user_date
  ON posts(user_id, created_at DESC);
```

**Unique Index**
```sql
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

**Partial Index**
```sql
CREATE INDEX idx_active_users
  ON users(email) WHERE active = true;
```

**Full-Text Search Index**
```sql
CREATE INDEX idx_posts_content_fulltext
  ON posts USING GIN(to_tsvector('english', content));
```

  ### 5. Data Types

  #### Common Data Types

**Integers**
```sql
TINYINT     -- 1 byte  (-128 to 127)
SMALLINT    -- 2 bytes (-32K to 32K)
INT         -- 4 bytes (-2B to 2B)
BIGINT      -- 8 bytes (-9 quintillion to 9 quintillion)
```

**Decimals**
```sql
DECIMAL(10,2)  -- Exact: 10 digits, 2 after decimal
FLOAT          -- Approximate 4 bytes
DOUBLE         -- Approximate 8 bytes
```

**Strings**
```sql
CHAR(10)       -- Fixed length
VARCHAR(255)   -- Variable length
TEXT           -- Unlimited length
```

**Date/Time**
```sql
DATE           -- Date only
TIME           -- Time only
DATETIME       -- Date and time
TIMESTAMP      -- Date and time with timezone
```

**Boolean**
```sql
BOOLEAN        -- true/false
```

**JSON**
```sql
JSON           -- JSON data
JSONB          -- Binary JSON (PostgreSQL)
```

  #### Choosing Data Types

**Email:**
```sql
email VARCHAR(255) NOT NULL
```

**Password Hash:**
```sql
password_hash CHAR(60) NOT NULL  -- bcrypt
```

**Money:**
```sql
price DECIMAL(10,2) NOT NULL  -- Exact arithmetic
```

**Status/Enum:**
```sql
status ENUM('draft', 'published', 'archived') NOT NULL
-- or
status VARCHAR(20) CHECK (status IN ('draft', 'published', 'archived'))
```

  ### 6. Schema Patterns

  #### User Authentication
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash CHAR(60) NOT NULL,
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id INT NOT NULL,
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_token ON user_sessions(token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
```

  #### Soft Deletes
```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  deleted_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_deleted ON posts(deleted_at);
```

  #### Audit Trail
```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(50) NOT NULL,
  record_id INT NOT NULL,
  action VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  user_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_audit_table_record ON audit_log(table_name, record_id);
```

  #### Polymorphic Associations
```sql
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  commentable_type VARCHAR(50) NOT NULL,  -- 'Post', 'Photo', etc.
  commentable_id INT NOT NULL,
  content TEXT NOT NULL,
  user_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_comments_polymorphic
  ON comments(commentable_type, commentable_id);
```

  #### Hierarchical Data (Nested Sets)
```sql
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  lft INT NOT NULL,
  rgt INT NOT NULL,
  depth INT NOT NULL
);

CREATE INDEX idx_categories_lft_rgt ON categories(lft, rgt);
```

  #### Tags/Categories (Many-to-Many)
```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
  post_id INT NOT NULL,
  tag_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (post_id, tag_id),
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE INDEX idx_post_tags_tag ON post_tags(tag_id);
```

  ### 7. Constraints

  #### NOT NULL
```sql
email VARCHAR(255) NOT NULL
```

  #### UNIQUE
```sql
email VARCHAR(255) UNIQUE NOT NULL
```

  #### CHECK
```sql
age INT CHECK (age >= 0 AND age <= 150)
price DECIMAL(10,2) CHECK (price > 0)
status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'banned'))
```

  #### DEFAULT
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
is_active BOOLEAN DEFAULT TRUE
role VARCHAR(20) DEFAULT 'user'
```

  ### 8. Performance Considerations

  #### Query Optimization
```sql
-- Good: Uses index on user_id
SELECT * FROM posts WHERE user_id = 123;

-- Bad: Function on indexed column prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- Good: Store lowercase email separately or use functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

  #### Covering Indexes
```sql
-- Query needs id, user_id, created_at
CREATE INDEX idx_posts_covering
  ON posts(user_id, created_at, id);
```

  #### Partitioning
```sql
CREATE TABLE events (
  id SERIAL,
  user_id INT,
  event_date DATE,
  data JSONB
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

  ### 9. Database Schema Documentation

  #### Table Documentation Template

```markdown
### Table: users

**Description**: Stores user account information

**Columns:**
| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | NO | AUTO | Primary key |
| email | VARCHAR(255) | NO | - | User email (unique) |
| name | VARCHAR(100) | NO | - | Full name |
| password_hash | CHAR(60) | NO | - | Bcrypt hash |
| created_at | TIMESTAMP | NO | NOW() | Creation timestamp |

**Indexes:**
- PRIMARY KEY: id
- UNIQUE: email
- INDEX: created_at

**Foreign Keys:**
- None

**Referenced By:**
- posts.user_id
- comments.user_id

**Constraints:**
- email must be unique
- email format validated at app level
```

  ### 10. Migration Strategy

```sql
-- Version 1: Initial schema
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL
);

-- Version 2: Add username
ALTER TABLE users ADD COLUMN username VARCHAR(50) UNIQUE;

-- Version 3: Make username required (with default for existing)
UPDATE users SET username = email WHERE username IS NULL;
ALTER TABLE users ALTER COLUMN username SET NOT NULL;
```

  ### 11. Output Format

Provide:

1. **ER Diagram** (text/ASCII format)
2. **Table Definitions** (CREATE TABLE statements)
3. **Indexes** (CREATE INDEX statements)
4. **Relationships** (Foreign keys and descriptions)
5. **Sample Data** (INSERT statements for testing)
6. **Common Queries** (Optimized SELECT examples)
7. **Migration Plan** (For evolving schema)
8. **Performance Notes** (Index strategy, partitioning)
9. **Data Dictionary** (Complete table/column documentation)

Generate complete, production-ready database schema following best practices.
```

---

### migration-script

> **Description**: Generate safe up/down database migration scripts.
> **Input Format**: `SQL Query or Schema`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `db`

#### Template Content:
```markdown
# Database Migration Generator

Please generate safe, idempotent UP and DOWN database migration scripts for the following schema changes:

```
{{args}}
```

Ensure the scripts adhere to the following best practices:

  ## 1. Up Migration
- Write the SQL to safely apply the changes (e.g., `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN`).
- Include necessary constraints (NOT NULL, UNIQUE, FOREIGN KEY).
- Add appropriate indexes for foreign keys or commonly queried columns.

  ## 2. Down Migration (Rollback)
- Write the exact inverse SQL to revert the changes cleanly (e.g., `DROP TABLE`, `DROP COLUMN`).
- Ensure the down migration executes without errors even if the state is partially applied.

  ## 3. Data Safety & Idempotency
- If the migration involves altering existing columns with data, explain how to handle data type casting or default values safely without locking the table for an extended period.
- Suggest transactions (`BEGIN; ... COMMIT;`) if the target RDBMS supports transactional DDL.

Please provide the `Up` and `Down` scripts clearly separated.
```

---

### mock-data-gen

> **Description**: Create realistic JSON/CSV mock data schemas for testing.
> **Input Format**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `db`

#### Template Content:
```markdown
# Mock Data Generator

Please generate realistic, diverse mock data for testing purposes based on the following schema or requirements:

```
{{args}}
```

Please follow these guidelines:

  ## 1. Realism
- Do not use generic placeholders like "test1", "test2". Use realistic names, addresses, dates, and text strings.
- Ensure logical consistency (e.g., if a user is from the UK, their phone number should match UK formats).

  ## 2. Edge Cases
Include at least a few records that contain:
- Null or missing optional fields.
- Extremely long strings.
- Special characters / Unicode (e.g., accents, emojis).
- Boundary values for numbers and dates.

  ## 3. Format
Provide the output in valid, well-formatted JSON (an array of objects) unless CSV is explicitly requested.
```

---

### regex-builder

> **Description**: Generate and explain complex Regular Expressions.
> **Input Format**: `Technical Concept`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `shell`, `db`

#### Template Content:
```markdown
# Regex Builder & Explainer

Please analyze the following text-matching requirement and generate an optimized Regular Expression:

```
{{args}}
```

Provide your response in the following format:

  ## 1. The Regular Expression
Provide the raw regex pattern. If it requires specific flags (like `g`, `i`, `m`), specify them.

  ## 2. Step-by-Step Breakdown
Explain exactly how the regex works, breaking down every token, group, and quantifier.

  ## 3. Test Cases
Provide examples of strings that this regex will successfully **Match**.
Provide examples of similar strings that this regex will correctly **Fail to match** (edge cases).

  ## 4. Performance & ReDoS Warning
- Is this regex susceptible to Catastrophic Backtracking (ReDoS)? 
- Are there any inefficient greedy quantifiers (`.*`) that could be optimized?
```

---

### sql-optimizer

> **Description**: Analyze slow queries and suggest indexes or rewrites.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `db`

#### Template Content:
```markdown
# SQL Query Optimizer

Please analyze the following SQL query and underlying schema context (if provided). Identify performance bottlenecks and suggest optimizations:

```
{{args}}
```

Provide your analysis in the following format:

  ## 1. Query Analysis
- Identify the likely bottlenecks (e.g., full table scans, correlated subqueries, missing `JOIN` conditions, inefficient `OR` clauses).
- Explain *why* the current query is slow.

  ## 2. Optimized Query
- Rewrite the query using best practices (e.g., replacing `IN` with `EXISTS`, using CTEs (Common Table Expressions), avoiding `SELECT *`).
- Ensure the logical output remains identical to the original query.

  ## 3. Indexing Recommendations
- Suggest specific indexes (e.g., B-Tree, composite, covering indexes) that would speed up the `WHERE`, `JOIN`, and `ORDER BY` clauses.
- Provide the exact `CREATE INDEX` SQL statements.

  ## 4. Execution Plan Advice
- Explain what to look for in the database's `EXPLAIN` or `EXPLAIN ANALYZE` output to verify the optimization worked.
```

---

## <a name='debug'></a> Debug

### debug-error

> **Description**: Help diagnose and fix errors.
> **Input Format**: `Error Log or Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `debug`

#### Template Content:
```markdown
# Debug Error

Please help diagnose and fix the following error:

{{args}}

  ## Diagnostic Process

  ### 1. Error Analysis

  #### Understand the Error
- What is the error message?
- What type of error is it? (Syntax, Runtime, Logic, Type, Reference, etc.)
- When does it occur? (Compile-time, Runtime, specific conditions)
- What is the stack trace showing?

  #### Identify the Source
- Which file and line number?
- Which function/method is failing?
- What was the execution path leading to the error?

  ### 2. Context Investigation

  #### Code Context
```
Analyze the code around the error:
- What is this code trying to do?
- What are the inputs at the time of error?
- What are the variable states?
- Are there any assumptions being made?
```

  #### Environment Context
- What environment? (Development, Staging, Production)
- Browser/Node version?
- Operating system?
- Dependencies and versions?

  #### User Context
- What action triggered the error?
- Can it be reproduced consistently?
- Does it happen for all users or specific ones?
- What are the reproduction steps?

  ### 3. Root Cause Analysis

  #### Common Error Patterns

**Null/Undefined Errors**
```javascript
// Error: Cannot read property 'x' of undefined
// Cause: Variable is undefined/null
// Fix: Add null checks
if (obj && obj.x) {
  // Use obj.x
}
```

**Type Errors**
```javascript
// Error: arr.map is not a function
// Cause: Variable is not an array
// Fix: Validate type
if (Array.isArray(arr)) {
  arr.map(...)
}
```

**Async Errors**
```javascript
// Error: Promise rejection unhandled
// Cause: Missing error handling
// Fix: Add try-catch or .catch()
try {
  await asyncFunction();
} catch (error) {
  handleError(error);
}
```

**Scope Errors**
```javascript
// Error: Variable not defined
// Cause: Variable out of scope or not declared
// Fix: Declare variable or adjust scope
```

**Off-by-One Errors**
```javascript
// Error: Index out of bounds
// Cause: Loop condition incorrect
// Fix: Check array.length - 1
for (let i = 0; i < arr.length; i++) { // not <=
  // Use arr[i]
}
```

  ### 4. Common Error Types & Solutions

  #### JavaScript/TypeScript Errors

**ReferenceError**
- Variable not declared
- Accessing before declaration
- Typo in variable name

**TypeError**
- Calling undefined as function
- Accessing property of null/undefined
- Wrong type passed to function

**SyntaxError**
- Missing brackets/parentheses
- Invalid syntax
- Import/export issues

**RangeError**
- Invalid array length
- Number out of range
- Stack overflow (recursion)

  #### Network/API Errors

**404 Not Found**
- Wrong endpoint URL
- Resource doesn't exist
- Routing issue

**CORS Error**
- Cross-origin request blocked
- Missing CORS headers
- Incorrect origin configuration

**Timeout**
- Request taking too long
- Network issues
- Server not responding

**401/403 Errors**
- Authentication failed
- Missing token
- Insufficient permissions

  ### 5. Debugging Steps

  #### Step 1: Reproduce the Error
```
1. Identify exact steps to trigger error
2. Note any specific conditions
3. Try in different environments
```

  #### Step 2: Isolate the Problem
```
1. Add console.logs/debugger statements
2. Check variable values before error
3. Verify function inputs
4. Test in isolation
```

  #### Step 3: Form Hypothesis
```
1. What do you think is causing it?
2. Why does it fail under these conditions?
3. What would fix it?
```

  #### Step 4: Test the Fix
```
1. Apply potential fix
2. Verify error is resolved
3. Check for side effects
4. Test edge cases
```

  #### Step 5: Prevent Recurrence
```
1. Add error handling
2. Add input validation
3. Add tests for this scenario
4. Add logging/monitoring
```

  ### 6. Debug Code Examples

  #### Add Defensive Checks
```javascript
// Before (error-prone)
function process(data) {
  return data.items.map(item => item.value);
}

// After (defensive)
function process(data) {
  if (!data || !Array.isArray(data.items)) {
    console.error('Invalid data format:', data);
    return [];
  }

  return data.items
    .filter(item => item && typeof item.value !== 'undefined')
    .map(item => item.value);
}
```

  #### Add Try-Catch
```javascript
// Before
async function fetchData() {
  const response = await fetch(url);
  return response.json();
}

// After
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw error; // or return default value
  }
}
```

  #### Add Logging
```javascript
function complexCalculation(a, b, c) {
  console.log('Input:', { a, b, c });

  const step1 = a * b;
  console.log('After step1:', step1);

  const step2 = step1 + c;
  console.log('After step2:', step2);

  const result = step2 / (a + b);
  console.log('Final result:', result);

  return result;
}
```

  ### 7. Output Format

Provide the following:

  #### 1. Error Diagnosis
- What the error means
- Why it's occurring
- Root cause analysis

  #### 2. Immediate Fix
- Code changes needed
- Step-by-step fix instructions
- Fixed code example

  #### 3. Prevention
- How to prevent this error
- Validation to add
- Tests to write

  #### 4. Additional Recommendations
- Related issues to check
- Code improvements
- Best practices to follow

  #### 5. Debugging Tips
- How to debug similar issues
- Tools to use
- Logging strategies

Generate a complete error analysis and solution following this structure.
```

---

### performance-profile

> **Description**: Analyze performance profiles.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `debug`

#### Template Content:
```markdown
# Performance Profiling & Optimization

Please perform a comprehensive performance analysis for the following:

{{args}}

  ## Performance Analysis Framework

  ### 1. Performance Metrics Collection

  #### Key Metrics

**Response Time Metrics**
- Average response time
- p50 (median)
- p95 (95th percentile)
- p99 (99th percentile)
- Maximum response time

**Throughput Metrics**
- Requests per second (RPS)
- Transactions per second (TPS)
- Data transfer rate

**Resource Utilization**
- CPU usage (%)
- Memory usage (MB/GB)
- Disk I/O (IOPS)
- Network bandwidth

**Application Metrics**
- Database query time
- API call latency
- Render time
- Time to First Byte (TTFB)

  ### 2. Profiling Tools & Techniques

  #### Browser Performance (Frontend)

**Chrome DevTools**
```javascript
// Performance tab
// - Record page load
// - Identify long tasks
// - Check layout shifts
// - Measure rendering time

// Coverage tab
// - Find unused JavaScript
// - Find unused CSS

// Network tab
// - Check waterfall
// - Identify slow requests
// - Check resource sizes
```

**Lighthouse Metrics**
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Total Blocking Time (TBT)
- Cumulative Layout Shift (CLS)

  #### Backend Performance

**Node.js Profiling**
```javascript
// CPU Profiling
node --prof app.js
node --prof-process isolate-*.log > processed.txt

// Memory Profiling
node --inspect app.js
// Use Chrome DevTools Memory tab

// Flame Graphs
npm install -g clinic
clinic doctor -- node app.js
clinic flame -- node app.js
```

**Python Profiling**
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

  ### 3. Performance Bottleneck Identification

  #### Common Bottlenecks

**Computational Bottlenecks**
- Inefficient algorithms (O(n²) vs O(n log n))
- Unnecessary calculations
- Heavy computations in loops
- Lack of memoization/caching

**I/O Bottlenecks**
- Synchronous file operations
- Multiple small database queries (N+1 problem)
- Unbatched API calls
- Large file uploads/downloads

**Network Bottlenecks**
- Too many HTTP requests
- Large payload sizes
- Missing compression
- No CDN usage
- DNS lookup time

**Rendering Bottlenecks**
- Forced synchronous layout (layout thrashing)
- Excessive DOM manipulation
- Large images without optimization
- Render-blocking resources
- Long JavaScript execution

**Database Bottlenecks**
- Missing indexes
- Inefficient queries
- N+1 query problem
- Large dataset fetches
- Connection pool exhaustion

**Memory Bottlenecks**
- Memory leaks
- Large objects in memory
- Inefficient data structures
- Excessive object creation

  ### 4. Profiling Analysis

  #### CPU Profiling Analysis

```
Function Name          | Self Time | Total Time | Calls
-----------------------|-----------|------------|-------
processData()          | 850ms     | 1200ms     | 1
  └─ validateItem()    | 300ms     | 350ms      | 1000
     └─ checkFormat()  | 200ms     | 200ms      | 1000
```

**Findings:**
- `processData()` is consuming 850ms of CPU time
- Called `validateItem()` 1000 times
- Opportunity: Batch validation or optimize `validateItem()`

  #### Memory Profiling Analysis

```
Heap Snapshot Comparison:

Constructor          | Objects | Shallow Size | Retained Size
---------------------|---------|--------------|---------------
Array                | +5000   | +400KB       | +12MB
String               | +2000   | +160KB       | +160KB
Object               | +1000   | +80KB        | +2MB
```

**Findings:**
- Array allocations growing significantly
- Potential memory leak in array handling
- Need to investigate why arrays are retained

  #### Network Profiling Analysis

```
Resource Timeline:

index.html           | 50ms   | 2KB
app.js               | 800ms  | 500KB (not compressed)
vendor.js            | 1200ms | 800KB (not compressed)
api/data             | 350ms  | 50KB
image1.png           | 600ms  | 2MB (not optimized)
```

**Findings:**
- JavaScript bundles are too large
- Missing gzip compression
- Images not optimized
- Could benefit from code splitting

  ### 5. Performance Optimization Strategies

  #### Algorithm Optimization

**Before (O(n²)):**
```javascript
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}
```

**After (O(n)):**
```javascript
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();

  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    }
    seen.add(item);
  }

  return Array.from(duplicates);
}
```

**Impact**: 100x faster for 1000 items

  #### Caching & Memoization

**Before:**
```javascript
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
```

**After:**
```javascript
const fibCache = new Map();

function fibonacci(n) {
  if (n <= 1) return n;
  if (fibCache.has(n)) return fibCache.get(n);

  const result = fibonacci(n - 1) + fibonacci(n - 2);
  fibCache.set(n, result);
  return result;
}
```

**Impact**: Exponential time reduction

  #### Batching Operations

**Before (N+1 Problem):**
```javascript
async function getUsersWithPosts() {
  const users = await db.query('SELECT * FROM users');

  for (const user of users) {
    user.posts = await db.query(
      'SELECT * FROM posts WHERE user_id = ?',
      [user.id]
    );
  }

  return users;
}
```

**After:**
```javascript
async function getUsersWithPosts() {
  const users = await db.query('SELECT * FROM users');
  const userIds = users.map(u => u.id);

  const posts = await db.query(
    'SELECT * FROM posts WHERE user_id IN (?)',
    [userIds]
  );

  const postsByUser = posts.reduce((acc, post) => {
    if (!acc[post.user_id]) acc[post.user_id] = [];
    acc[post.user_id].push(post);
    return acc;
  }, {});

  users.forEach(user => {
    user.posts = postsByUser[user.id] || [];
  });

  return users;
}
```

**Impact**: N+1 queries → 2 queries

  #### Lazy Loading

**Before:**
```javascript
import Chart from 'chart.js'; // 100KB

function App() {
  return <div>Homepage (chart not needed here)</div>;
}
```

**After:**
```javascript
function App() {
  const [Chart, setChart] = useState(null);

  const loadChart = async () => {
    const module = await import('chart.js');
    setChart(module.default);
  };

  return (
    <div>
      <button onClick={loadChart}>Load Chart</button>
    </div>
  );
}
```

**Impact**: Reduced initial bundle size by 100KB

  #### Virtual Scrolling

**Before:**
```javascript
// Rendering 10,000 items
{items.map(item => <ListItem key={item.id} {...item} />)}
```

**After:**
```javascript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      <ListItem {...items[index]} />
    </div>
  )}
</FixedSizeList>
```

**Impact**: Render 20 items instead of 10,000

  ### 6. Performance Benchmarking

```javascript
// Measure execution time
console.time('operation');
performOperation();
console.timeEnd('operation');

// More precise timing
const start = performance.now();
performOperation();
const end = performance.now();
console.log(`Took ${end - start}ms`);

// Benchmark comparison
function benchmark(fn, iterations = 1000) {
  const start = performance.now();
  for (let i = 0; i < iterations; i++) {
    fn();
  }
  const end = performance.now();
  return (end - start) / iterations;
}

const avgTime1 = benchmark(oldImplementation);
const avgTime2 = benchmark(newImplementation);
console.log(`Improvement: ${((avgTime1 - avgTime2) / avgTime1 * 100).toFixed(2)}%`);
```

  ### 7. Performance Budget

Set performance targets:

```
Metric                    | Budget  | Current | Status
--------------------------|---------|---------|--------
Initial Page Load         | < 3s    | 4.2s    | ❌ Over
Time to Interactive       | < 5s    | 6.1s    | ❌ Over
JavaScript Bundle Size    | < 200KB | 500KB   | ❌ Over
API Response Time (p95)   | < 500ms | 350ms   | ✅ Good
Database Query Time (p95) | < 100ms | 80ms    | ✅ Good
Memory Usage              | < 100MB | 150MB   | ❌ Over
```

  ### 8. Output Format

Provide:

  #### 1. Performance Audit Summary
- Current performance metrics
- Identified bottlenecks
- Priority ranking

  #### 2. Detailed Analysis
- Profiling results
- Slowest functions/queries
- Resource usage breakdown
- Timeline waterfall analysis

  #### 3. Optimization Recommendations
- High-impact optimizations (implement first)
- Medium-impact optimizations
- Low-impact optimizations
- Code examples for each

  #### 4. Expected Improvements
- Projected performance gains
- Before/after metrics
- ROI analysis (effort vs impact)

  #### 5. Implementation Plan
- Step-by-step optimization sequence
- Testing strategy
- Rollback plan
- Monitoring plan

  #### 6. Long-term Recommendations
- Architecture improvements
- Monitoring setup
- Performance budgets
- Regular profiling schedule

Generate a complete performance analysis and optimization plan following this framework.
```

---

### suggest-fixes

> **Description**: Suggest potential bug fixes and improvements for code.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`, `debug`

#### Template Content:
```markdown
# Suggest Bug Fixes
Please analyze the following code and suggest potential fixes and improvements: 
```
{{args}}
```
Focus on: 
  ## 1. Correctness & Reliability
- Identify any logical errors, off-by-one errors, or incorrect assumptions.
- Check for potential memory leaks, resource leaks, or race conditions.
- Ensure that edge cases and error conditions are handled correctly.
  ## 2. Performance & Efficiency
- Look for areas where the code could be more efficient or performant.
- Identify any unnecessary computations, redundant data copies, or inefficient algorithms.
- Suggest ways to optimize resource usage and reduce latency.
  ## 3. Readability & Maintainability
- Recommend improvements to code structure, naming conventions, and organization.
- Suggest ways to make the code more concise, clear, and easy to understand.
- Identify opportunities for refactoring and simplification.
  ## 4. Security & Robustness
- Check for common security vulnerabilities (e.g., injection, XSS, buffer overflows).
- Ensure that sensitive data is handled securely and that inputs are properly validated.
- Suggest ways to make the code more robust and resilient to failures.
  ## 5. Best Practices & Idioms
- Recommend the use of more modern or idiomatic language features and libraries.
- Suggest ways to follow established coding standards and best practices.
For each suggested fix or improvement, provide:
1. **Description of the Issue**: What is wrong or could be better?
2. **Impact**: Why is it important to fix or improve this?
3. **Suggested Change**: Provide a clear explanation and code example of the proposed fix.
4. **Alternative Approaches**: Are there other ways to achieve the same result?
Provide a comprehensive and actionable set of recommendations that will help improve the overall quality and reliability of the code.
```

---

### trace-issue

> **Description**: Trace the root cause of issues.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `debug`

#### Template Content:
```markdown
# Root Cause Analysis - Trace Issue

Please perform a comprehensive root cause analysis for the following issue:

{{args}}

  ## Root Cause Analysis Framework

  ### 1. Issue Definition

  #### Problem Statement
- What is the observed issue?
- What is the expected behavior?
- What is the actual behavior?
- When was it first observed?
- How frequently does it occur?

  #### Impact Assessment
- Who is affected? (All users, specific users, admins)
- How severe is the impact? (Critical, High, Medium, Low)
- What functionality is broken?
- Is there a workaround available?

  ### 2. Information Gathering

  #### Symptoms Collection
- Error messages or logs
- Stack traces
- Screenshots or recordings
- User reports
- Monitoring/metrics data

  #### Environmental Factors
- Environment: (Development, Staging, Production)
- Time of occurrence
- Frequency pattern (constant, intermittent, periodic)
- Affected platforms/browsers
- Affected user segments

  #### Recent Changes
- Code deployments
- Configuration changes
- Infrastructure changes
- Dependency updates
- Data migrations

  ### 3. The 5 Whys Method

Use iterative "why" questioning to dig deeper:

```
Issue: Users can't log in

Why? → The authentication service is returning 500 errors
  Why? → The database connection pool is exhausted
    Why? → Connections are not being released properly
      Why? → The ORM is not closing connections on error
        Why? → Missing error handling in the database layer

Root Cause: Inadequate error handling causing connection leaks
```

  ### 4. Timeline Analysis

Create a timeline of events:

```
T-0: Issue first reported
T-3 hours: Last successful login
T-4 hours: Database migration deployed
T-6 hours: Traffic spike observed
```

Identify correlations between events and the issue.

  ### 5. Reproduce the Issue

  #### Reproduction Steps
1. Detailed steps to reproduce
2. Required preconditions
3. Expected vs actual results
4. Frequency of reproduction

  #### Minimal Reproduction
- Simplest case that reproduces the issue
- Isolate variables
- Test in controlled environment

  ### 6. Hypothesis Formation

  #### Potential Causes
List all potential root causes:
1. **Hypothesis A**: Database connection leak
   - Evidence: Connection pool exhaustion
   - Likelihood: High
   - Test: Monitor connection usage

2. **Hypothesis B**: Memory leak in service
   - Evidence: Increasing memory usage
   - Likelihood: Medium
   - Test: Profile memory over time

3. **Hypothesis C**: Network timeout misconfiguration
   - Evidence: Intermittent failures
   - Likelihood: Low
   - Test: Check timeout settings

  ### 7. Investigation Techniques

  #### Log Analysis
```bash
# Search for errors in time window
grep "ERROR" app.log | grep "2024-01-15 14:*"

# Count error occurrences
grep "ERROR" app.log | cut -d' ' -f5 | sort | uniq -c

# Correlate with other events
grep -A 5 -B 5 "Connection timeout" app.log
```

  #### Code Analysis
- Review recent changes (git diff)
- Check related code paths
- Look for similar past issues
- Review error handling

  #### Data Analysis
- Check database state
- Review recent data changes
- Analyze query performance
- Check for data anomalies

  #### Performance Profiling
- CPU profiling
- Memory profiling
- Network analysis
- Database query analysis

  ### 8. Common Root Cause Patterns

  #### Resource Exhaustion
- Memory leaks
- Connection pool exhaustion
- File descriptor limits
- Disk space issues

  #### Race Conditions
- Concurrent access issues
- Timing-dependent bugs
- Synchronization problems
- State inconsistencies

  #### Configuration Issues
- Wrong environment variables
- Missing configuration
- Incorrect timeouts
- Feature flags

  #### Dependency Problems
- Version incompatibilities
- Breaking changes in dependencies
- Missing dependencies
- Conflicting dependencies

  #### Data-Related
- Data corruption
- Missing data
- Invalid data format
- Schema mismatches

  #### Infrastructure
- Network issues
- Server overload
- DNS problems
- Load balancer misconfiguration

  ### 9. Testing Hypotheses

For each hypothesis, design tests:

```javascript
// Hypothesis: Connection leak in error path
async function testConnectionLeak() {
  const initialConnections = await getConnectionCount();

  // Trigger error condition 100 times
  for (let i = 0; i < 100; i++) {
    try {
      await triggerErrorCondition();
    } catch (e) {
      // Expected to fail
    }
  }

  const finalConnections = await getConnectionCount();
  const leaked = finalConnections - initialConnections;

  console.log(`Leaked connections: ${leaked}`);
  return leaked;
}
```

  ### 10. Fishbone Diagram (Cause & Effect)

Organize potential causes by category:

```
Problem: Authentication Failures
│
├─ People
│  ├─ Insufficient error handling in code
│  └─ Lack of monitoring
│
├─ Process
│  ├─ No rollback procedure
│  └─ Inadequate testing
│
├─ Technology
│  ├─ Database connection pool size
│  ├─ Network timeout configuration
│  └─ ORM connection management
│
├─ Environment
│  ├─ High traffic load
│  └─ Infrastructure capacity
│
└─ Data
   ├─ Database migration issues
   └─ Data corruption
```

  ### 11. Root Cause Determination

  #### Evidence-Based Conclusion
- List all supporting evidence
- Rule out alternative causes
- Confirm through testing
- Verify fix resolves issue

  #### Root Cause Statement
"The authentication failures are caused by **[specific technical cause]** which occurs when **[conditions]**, resulting in **[observed behavior]**."

  ### 12. Impact Analysis

  #### Affected Components
- List all affected systems
- Dependency map
- Blast radius assessment

  #### Affected Users
- User segments impacted
- Severity of impact
- Duration of impact

  ### 13. Solution Design

  #### Immediate Fix (Hotfix)
- Quick mitigation
- Minimal risk changes
- Deploy urgently

  #### Long-term Solution
- Proper fix addressing root cause
- Architecture improvements
- Prevention measures

  #### Prevention
- Tests to add
- Monitoring to implement
- Alerts to create
- Documentation to write

  ### 14. Verification Plan

  #### Verification Steps
1. Apply fix in test environment
2. Reproduce original issue
3. Verify issue is resolved
4. Test edge cases
5. Check for side effects
6. Monitor in production

  ### 15. Output Format

Provide:

  #### 1. Executive Summary
- Issue description
- Root cause (one sentence)
- Impact
- Resolution

  #### 2. Detailed Analysis
- Timeline
- Investigation process
- Evidence collected
- Hypotheses tested

  #### 3. Root Cause
- Technical explanation
- Why it wasn't caught earlier
- Contributing factors

  #### 4. Solution
- Immediate fix
- Long-term solution
- Implementation steps

  #### 5. Prevention
- Tests to add
- Monitoring improvements
- Process changes
- Documentation updates

  #### 6. Lessons Learned
- What went wrong
- What went right
- What to improve

Generate a complete root cause analysis following this framework.
```

---

## <a name='devops'></a> Devops

### bash-script-generator

> **Description**: Write robust, POSIX-compliant bash scripts.
> **Input Format**: `Task to Script`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `shell`

#### Template Content:
```markdown
# Robust Bash Script Generator

Please write a robust, production-ready bash script to accomplish the following task:

```
{{args}}
```

Ensure the script adheres to the following Bash best practices:

  ## 1. Safety & Error Handling
- Start the script with `set -euo pipefail` to ensure it fails fast on errors, undefined variables, and pipe failures.
- Use `trap` for cleanup of temporary files or locks upon script exit or interruption.

  ## 2. Logging & Output
- Implement simple logging functions (e.g., `log_info`, `log_error`, `log_warn`) to standard error (`>&2`) where appropriate, so `stdout` remains clean for piping.
- Include timestamps in the log output.

  ## 3. Argument Parsing & Help
- Implement a `usage()` or `help()` function that explains how to run the script and what arguments it accepts.
- Use a `while/case` loop with `shift` or `getopts` to parse command-line flags securely.

  ## 4. Syntax & Style
- Prefer `[[ ]]` over `[ ]` for test conditions.
- Prefer `"$()"` over backticks `` ` ` `` for command substitution.
- Quote all variables properly (e.g., `"$VAR"`) to prevent word splitting and globbing issues.
- Use `local` variables inside functions to prevent polluting the global scope.

  ## 5. Idempotency & Checks
- Where applicable, check if required commands exist before using them (e.g., using `command -v`).
- Ensure operations are idempotent (e.g., using `mkdir -p` instead of just `mkdir`).

For your response, provide:
1. **The complete, commented bash script.**
2. **A brief explanation** of how to run it, including examples of the flags or arguments.
```

---

### ci-cd-pipeline

> **Description**: Generate CI/CD pipelines (GitHub Actions, GitLab CI, etc.).
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# CI/CD Pipeline Generator

Please generate a comprehensive CI/CD pipeline configuration (e.g., GitHub Actions `.yaml`, GitLab `.gitlab-ci.yml`, or equivalent) based on the following requirements:

```
{{args}}
```

Ensure the generated pipeline follows these modern CI/CD best practices:

  ## 1. Triggers & Workflow Control
- Define clear trigger events (e.g., push to `main`/`master`, pull requests, or manual dispatches).
- Use path or branch filtering to prevent unnecessary pipeline runs.

  ## 2. Environment & Tooling
- Specify the execution environment/runner (e.g., `ubuntu-latest`).
- Set up the specific programming language, Node/Python/Go version, or Docker environment required for the project.

  ## 3. Standard CI Stages
- **Linting & Formatting**: Include a step to check code style.
- **Testing**: Include a step to run unit/integration tests and output coverage reports.
- **Build**: Compile the application or build the Docker image.

  ## 4. Caching & Optimization
- Implement dependency caching (e.g., `actions/cache` or built-in package manager caching) to significantly speed up build times across runs.

  ## 5. Security & Secrets
- Do not hardcode credentials. Demonstrate how to correctly inject environment variables or secrets from the CI provider's secret store (e.g., `${{ secrets.API_KEY }}`).
- Use least-privilege permissions for the CI token (e.g., `permissions: contents: read` in GitHub Actions).

For your response, provide:
1. **The complete CI/CD configuration code.**
2. **A brief explanation** of the stages, caching strategy, and how the user should configure their secrets.
```

---

### dockerfile-generator

> **Description**: Generate optimized, production-ready Dockerfiles.
> **Input Format**: `App Stack or Requirements`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Dockerfile Generator

Please generate a highly optimized, production-ready `Dockerfile` for the following application/stack:

```
{{args}}
```

Ensure the generated Dockerfile adheres to the following best practices:

  ## 1. Multi-Stage Builds
- Use multi-stage builds to separate the build environment from the runtime environment.
- Keep the final production image as small as possible by only copying compiled artifacts or necessary runtime dependencies.

  ## 2. Base Images
- Select lightweight and secure base images (e.g., `alpine`, `distroless`, or slim variants of official images).
- Pin specific versions/tags (avoid using `latest`) to ensure reproducible builds.

  ## 3. Security & Privileges
- **Never run as root.** Create a dedicated non-root user and group, and use the `USER` directive to switch to it before running the application.
- Ensure proper file permissions are set for the application files.

  ## 4. Caching & Performance
- Order instructions to maximize Docker layer caching (e.g., copy dependency manifest files like `package.json` or `requirements.txt` and install dependencies *before* copying the rest of the source code).
- Clean up package manager caches (e.g., `apt-get clean`, `rm -rf /var/lib/apt/lists/*`, or `npm cache clean`) in the same `RUN` step to reduce layer size.

  ## 5. Configuration & Execution
- Use `ENTRYPOINT` for the main executable and `CMD` for default arguments, or provide a clear standard `CMD`.
- Expose necessary ports using the `EXPOSE` directive.
- Include a `.dockerignore` file recommendation to prevent sensitive or unnecessary files from bloating the build context.

For your response, provide:
1. **The `.dockerignore` content.**
2. **The complete `Dockerfile` code.**
3. **A brief explanation** of the optimizations and security measures you applied.
```

---

### kubernetes-manifest

> **Description**: Create Kubernetes Deployment and Service YAML manifests.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Kubernetes Manifest Generator

Please generate production-ready Kubernetes YAML manifests (Deployment and Service) for the following application:

```
{{args}}
```

Ensure the generated manifests follow these Kubernetes best practices:

  ## 1. Workload Configuration (Deployment)
- Define a clear `Deployment` structure with an appropriate `replica` count (e.g., at least 2 for high availability).
- Use specific image tags (do not use `latest`).
- Include standard metadata `labels` (e.g., `app.kubernetes.io/name`, `app.kubernetes.io/version`).

  ## 2. Resilience & Health Checks
- Include a `livenessProbe` to restart the container if it deadlocks.
- Include a `readinessProbe` to ensure traffic is only routed to the pod when it is ready to accept requests.
- Provide sensible defaults for probe `initialDelaySeconds`, `periodSeconds`, and `timeoutSeconds`.

  ## 3. Resource Management
- Define explicit `resources.requests` (CPU/Memory) to ensure the pod is scheduled on an appropriate node.
- Define explicit `resources.limits` (CPU/Memory) to prevent the pod from monopolizing node resources.

  ## 4. Security Context
- Add a `securityContext` at the pod or container level (e.g., `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, dropping default capabilities).

  ## 5. Networking (Service)
- Define a corresponding `Service` to expose the deployment.
- Correctly map the `targetPort` (container port) to the `port` (service port).
- Set an appropriate service `type` (e.g., `ClusterIP` for internal, or `LoadBalancer`/`NodePort` if specified in the prompt).

For your response, provide:
1. **The complete YAML manifest** (combining Deployment and Service using `---`).
2. **A brief explanation** of the specific probes, limits, and security contexts chosen for this stack.
```

---

### terraform-module

> **Description**: Write Infrastructure-as-Code Terraform modules.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Terraform Module Generator

Please generate a well-structured, modular Terraform configuration for the following cloud infrastructure requirements:

```
{{args}}
```

Ensure the generated code adheres to standard Infrastructure-as-Code (IaC) and Terraform best practices:

  ## 1. File Structure
Separate the configuration into standard files. Output the code with clear headers for:
- `main.tf` (The core resource definitions).
- `variables.tf` (Input variables with descriptions and types).
- `outputs.tf` (Return values for consuming modules).
- `providers.tf` (Provider configuration and required versions).

  ## 2. Variable Management
- Use strong typing for variables (e.g., `type = string`, `type = list(string)`).
- Provide a `description` for every variable.
- Provide sensible `default` values where appropriate.
- Mark sensitive variables (like passwords or API keys) with `sensitive = true`.

  ## 3. Naming Conventions & Tagging
- Use standard naming conventions (snake_case) for resources and variables.
- Implement a standard tagging strategy (e.g., `Environment`, `Project`, `ManagedBy = "Terraform"`) and apply it to all applicable resources using local variables or provider default tags.

  ## 4. State & Remote Backend (Optional but Recommended)
- Provide an example of how to configure a remote state backend (e.g., S3 + DynamoDB, or Terraform Cloud) to prevent state file loss.

  ## 5. Best Practices
- Avoid hardcoding values; use variables, locals, or data sources.
- Utilize standard module patterns if applicable.

For your response, provide:
1. **The complete Terraform code**, clearly separated by file name.
2. **A brief summary** of the resources created and any prerequisite steps (like initializing the backend or providing specific credentials).
```

---

## <a name='docs'></a> Docs

### pr-template

> **Description**: Generate a Pull Request template for a repository.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `agile`, `docs`

#### Template Content:
```markdown
# Pull Request Template Generator

Please generate a comprehensive, professional Markdown Pull Request (PR) Template for a repository based on the following project context or requirements:

```
{{args}}
```

Ensure the template includes the following sections, formatted nicely with markdown comments `<!-- -->` to guide the developer:

  ## 1. PR Description
A section prompting the developer to describe the *why* and the *what* of the changes.

  ## 2. Type of Change
A checklist for the developer to categorize the PR (e.g., Bug fix, New feature, Breaking change, Refactoring, Documentation update).

  ## 3. Ticket / Issue Reference
A place to link the Jira ticket, Linear issue, or GitHub Issue (e.g., `Fixes #123`).

  ## 4. Testing & Verification
A section asking the developer to explain how they tested their changes, and a checklist ensuring tests were added/updated.

  ## 5. Deployment / Rollback Plan (If applicable)
A section for DevOps/Backend projects asking about migration scripts, feature flags, or rollback procedures.

  ## 6. Pre-Merge Checklist
A final checklist for the author (e.g., Self-review completed, CI passing, Documentation updated).

Output ONLY the raw markdown template, ready to be saved as `.github/PULL_REQUEST_TEMPLATE.md`.
```

---

### security-policy

> **Description**: Draft a SECURITY.md or vulnerability disclosure policy.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`, `security`

#### Template Content:
```markdown
# Security Policy Generator

Please generate a professional, standard `SECURITY.md` file (Vulnerability Disclosure Policy) for the following project/organization:

```
{{args}}
```

Ensure the policy includes:

  ## 1. Supported Versions
A clear table indicating which versions of the project are currently supported with security updates.

  ## 2. Reporting a Vulnerability
- Step-by-step instructions on how a security researcher should privately report a vulnerability (e.g., specific email address, PGP key, or HackerOne link).
- Explicitly state *not* to open a public GitHub issue.

  ## 3. Response Process
- A timeline/SLA for when the researcher can expect an initial response, triage, and resolution.
- Expectations regarding embargo periods before public disclosure.

  ## 4. Out of Scope
- A clear list of attack types or issues that are considered out-of-scope for the vulnerability program (e.g., volumetric DDoS, social engineering, physical attacks).
```

---

### write-api-docs

> **Description**: Create API documentation.
> **Input Format**: `Project/App Description`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`

#### Template Content:
```markdown
# Generate API Documentation

Please create comprehensive API documentation for the following code:

{{args}}

  ## Structure

Your API documentation should include:

  ### 1. Overview
- API purpose and capabilities
- Base URL / endpoint
- Authentication method
- Rate limits
- API version

  ### 2. Authentication
- How to authenticate
- API key / token management
- Example authentication requests
- Security considerations

  ### 3. Endpoints

For each endpoint, provide:

  #### Endpoint Name
**Method**: GET/POST/PUT/DELETE/PATCH
**Path**: `/api/v1/resource`
**Description**: Clear description of what this endpoint does

**Authentication Required**: Yes/No

**Request Parameters**:
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| name | string | Yes | User's name | "John Doe" |

**Query Parameters** (if applicable):
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| limit | integer | No | Max results | 10 |

**Request Body** (if applicable):
```json
{
  "field": "value",
  "nested": {
    "field": "value"
  }
}
```

**Response**:
- Status Code: 200 OK
```json
{
  "data": {},
  "message": "Success"
}
```

**Error Responses**:
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing/invalid token
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server error

**Example Request**:
```bash
curl -X POST https://api.example.com/v1/resource -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"key": "value"}'
```

**Example Response**:
```json
{
  "status": "success",
  "data": {}
}
```

  ### 4. Data Models / Schemas
Document all data structures:

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}
```

  ### 5. Error Handling
- Error response format
- Error codes and meanings
- How to handle specific errors

  ### 6. Code Examples
Provide examples in multiple languages:
- JavaScript/TypeScript
- Python
- cURL
- Other relevant languages

  ### 7. Pagination
- How pagination works
- Parameters (page, limit, offset)
- Response metadata

  ### 8. Filtering & Sorting
- Available filters
- Sort parameters
- Search functionality

  ### 9. Rate Limiting
- Rate limit rules
- Headers returned
- How to handle rate limit errors

  ### 10. Webhooks (if applicable)
- How to register webhooks
- Event types
- Payload structure
- Retry logic

  ### 11. SDKs & Libraries
- Available client libraries
- Installation instructions
- Quick start with SDK

  ### 12. Changelog
- API version history
- Breaking changes
- Deprecation notices

  ## Best Practices

- Use consistent formatting
- Provide complete, working examples
- Include all possible parameters
- Document all possible responses
- Use realistic example data
- Keep it up-to-date
- Include common error scenarios
- Make it scannable with clear headings
- Link related endpoints

Generate complete, professional API documentation following these guidelines.
```

---

### write-changelog

> **Description**: Generate changelog from changes.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`

#### Template Content:
```markdown
# Generate Changelog

Please create a comprehensive changelog for the following changes:

{{args}}

  ## Format

Follow the [Keep a Changelog](https://keepachangelog.com/) standard:

  ### Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Any bug fixes

### Security
- Vulnerabilities fixed

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Feature X
- Feature Y

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

  ## Categories

Use these standard categories:

  ### Added
- New features
- New functionality
- New capabilities

  ### Changed
- Changes to existing functionality
- Updated dependencies
- Performance improvements
- Refactoring

  ### Deprecated
- Features that will be removed in future versions
- APIs marked for deprecation

  ### Removed
- Features removed
- APIs removed
- Support dropped

  ### Fixed
- Bug fixes
- Issue resolutions
- Patches

  ### Security
- Security vulnerability fixes
- Security improvements
- CVE addresses

  ## Guidelines

1. **Version Numbers**: Use semantic versioning (MAJOR.MINOR.PATCH)
   - MAJOR: Breaking changes
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes (backward compatible)

2. **Dates**: Use ISO format (YYYY-MM-DD)

3. **Grouping**: Group changes by category

4. **Links**: Link to relevant issues, PRs, or commits

5. **Clarity**: Write for users, not developers
   - Focus on impact, not implementation
   - Use past tense
   - Be concise but clear

6. **Breaking Changes**: Highlight these prominently

7. **Contributors**: Credit contributors where appropriate

  ## Examples

**Good Entry**:
```markdown
### Added
- User authentication with OAuth 2.0 support (#123)
- Export data to CSV functionality (#145)
```

**Bad Entry**:
```markdown
### Added
- Fixed the thing
- Updated stuff
```

  ## Additional Sections (optional)

  ### Migration Guide
For breaking changes, provide migration instructions:

```markdown
### Migration from v1.x to v2.x

**Breaking Changes**:
- Function `oldFunction()` renamed to `newFunction()`
- Parameter order changed in `someMethod()`

**How to Update**:
1. Replace all instances of `oldFunction()` with `newFunction()`
2. Update method calls to match new signature
```

  ### Known Issues
Document known issues for the release:

```markdown
### Known Issues
- Safari browser has rendering issues with feature X (#234)
- Memory leak in long-running processes (#245) - workaround available
```

Generate a complete, well-organized changelog following these standards.
```

---

### write-contributing

> **Description**: Create CONTRIBUTING.md guidelines.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`

#### Template Content:
```markdown
# Generate CONTRIBUTING.md

Please create comprehensive contribution guidelines for the following project:

{{args}}

  ## Structure

Your CONTRIBUTING.md should include:

  ### 1. Welcome Message
- Thank contributors
- State the project's openness to contributions
- Briefly explain the project's mission

  ### 2. Code of Conduct
Reference or include:
```markdown
## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [email].
```

  ### 3. How Can I Contribute?

  #### Reporting Bugs
- Use issue templates
- Search existing issues first
- Include reproduction steps
- Provide system information
- Include error messages and logs

**Bug Report Template**:
```markdown
**Describe the bug**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 10]
- Version: [e.g., 1.0.0]
```

  #### Suggesting Features
- Use feature request template
- Explain the problem it solves
- Provide use cases
- Consider alternatives

**Feature Request Template**:
```markdown
**Is your feature request related to a problem?**
A clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

  #### Pull Requests
- Fork and create branches
- Follow code style
- Write tests
- Update documentation
- Reference issues

  ### 4. Development Setup

  #### Prerequisites
- Required software/tools
- Versions needed
- System requirements

  #### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/user/repo.git

# Navigate to directory
cd repo

# Install dependencies
npm install

# Run tests
npm test

# Start development server
npm run dev
```

  ### 5. Development Workflow

  #### Branch Naming
- `feature/description` for new features
- `fix/description` for bug fixes
- `docs/description` for documentation
- `refactor/description` for refactoring

  #### Commit Messages
Follow conventional commits:
```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(auth): add OAuth2 support
fix(api): resolve timeout issue in user endpoint
docs(readme): update installation instructions
```

  ### 6. Coding Standards

  #### Style Guide
- Language-specific conventions
- Linting rules
- Formatting guidelines
- Naming conventions

  #### Best Practices
- Write self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Follow SOLID principles

  ### 7. Testing

  #### Writing Tests
- Unit tests required for new features
- Integration tests for API changes
- E2E tests for critical user flows

  #### Running Tests
```bash
npm test                 # Run all tests
npm test -- --watch      # Watch mode
npm run test:coverage    # Coverage report
```

  #### Test Coverage
- Minimum coverage requirements
- How to check coverage
- What to test

  ### 8. Documentation

  #### Code Documentation
- JSDoc/docstrings required
- Document public APIs
- Explain complex algorithms
- Include examples

  #### README Updates
- Update for new features
- Add examples for new functionality
- Update configuration options

  ### 9. Pull Request Process

1. **Before Submitting**
   - Run tests locally
   - Run linter
   - Update documentation
   - Self-review your changes

2. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Related Issues
   Fixes #(issue number)

   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests
   - [ ] Updated existing tests

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-reviewed code
   - [ ] Commented complex code
   - [ ] Updated documentation
   - [ ] No new warnings
   ```

3. **Review Process**
   - Reviewers will be assigned
   - Address feedback
   - Maintain discussion
   - Squash commits if requested

4. **Merging**
   - Requires approval from maintainers
   - All checks must pass
   - Conflicts must be resolved

  ### 10. Community

  #### Getting Help
- Where to ask questions (Discussions, Discord, Slack)
- Documentation resources
- FAQ link

  #### Recognition
- Contributors will be acknowledged
- Link to contributors list

  ### 11. Release Process (for maintainers)
- Versioning strategy
- Release checklist
- Changelog updates

  ### 12. License
Reminder about project license and contributor agreement

  ## Tone
- Welcoming and inclusive
- Clear and instructive
- Encouraging
- Professional but friendly

Generate complete, beginner-friendly contribution guidelines following these standards.
```

---

### write-inline-comments

> **Description**: Add helpful code comments.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`

#### Template Content:
```markdown
# Intelligent Code Commenting

Please review the following code and add highly effective, professional inline comments and documentation blocks. 

```
{{args}}
```

**Commenting Guidelines:**
1. **Explain the "Why", not the "What"**: Do not state the obvious. Assume the reader knows the programming language. Explain the *intent*, business logic, or reasons behind non-obvious decisions.
2. **Function/Method Headers**: Provide standard documentation blocks (e.g., JSDoc, Docstrings) for all public functions, including:
   - A brief description of what the function does.
   - `@param` descriptions (types and purposes).
   - `@returns` description.
   - Any `@throws` or exceptions.
3. **Complex Logic**: Add inline comments directly above complex algorithms, regex patterns, or obscure workarounds.
4. **Formatting**: Maintain the original code's indentation and style. Only output the commented code (no additional conversational text).

Please provide the fully commented code below:
```

---

### write-readme

> **Description**: Generate comprehensive README files.
> **Input Format**: `Project/App Description`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`

#### Template Content:
```markdown
# Generate Comprehensive README

Please create a comprehensive README.md file for the following project:

{{args}}

  ## Structure

Your README should include:

  ### 1. Project Title & Badges
- Clear, descriptive title
- Relevant badges (build status, version, license, etc.)
- One-line description

  ### 2. Description
- What the project does
- Why it exists (problem it solves)
- Key features (3-5 bullet points)
- What makes it unique

  ### 3. Table of Contents
(For longer READMEs)

  ### 4. Installation
- Prerequisites
- Step-by-step installation instructions
- Platform-specific notes if needed
- Verification steps

  ### 5. Quick Start / Usage
- Minimal working example
- Common use cases
- Code examples with explanations
- Expected output

  ### 6. API Documentation (if applicable)
- Key functions/methods
- Parameters and return values
- Usage examples

  ### 7. Configuration
- Configuration options
- Environment variables
- Config file examples

  ### 8. Examples
- Real-world usage scenarios
- Screenshots or GIFs if relevant
- Links to example projects

  ### 9. Development
- How to set up development environment
- How to run tests
- How to build the project
- Contributing guidelines link

  ### 10. Roadmap (optional)
- Planned features
- Known issues
- Future directions

  ### 11. Contributing
- How to contribute
- Code of conduct link
- Pull request process

  ### 12. Testing
- How to run tests
- Test coverage
- Types of tests

  ### 13. License
- License type
- Copyright notice

  ### 14. Authors & Acknowledgments
- Main contributors
- Credits and thanks
- Inspiration or related projects

  ### 15. Support & Contact
- Where to get help
- Issue tracker link
- Community channels (Discord, Slack, etc.)

  ## Best Practices

- Use clear, concise language
- Include working code examples
- Add visual elements where helpful
- Use proper Markdown formatting
- Keep it up-to-date and accurate
- Make it beginner-friendly
- Include troubleshooting section if needed

  ## Tone
- Professional but approachable
- Assume basic technical knowledge
- Be enthusiastic but not hyperbolic
- Focus on clarity over cleverness

Generate a complete, production-ready README following these guidelines.
```

---

## <a name='frontend'></a> Frontend

### accessibility-audit

> **Description**: Review HTML/React code for WCAG compliance.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `frontend`, `security`

#### Template Content:
```markdown
# Frontend Accessibility (a11y) Audit

Please analyze the following HTML, React, or Vue component for Web Content Accessibility Guidelines (WCAG) compliance:

```
{{args}}
```

Focus your audit on the following areas:

  ## 1. Semantic HTML
- Are the correct semantic tags used (e.g., `<button>` vs `<div>` for clickable elements, `<nav>`, `<main>`)?
- Are heading levels (`h1`-`h6`) structured logically without skipping levels?

  ## 2. Keyboard Navigation
- Can all interactive elements be reached using the `Tab` key?
- Is there a visible focus indicator (`:focus` or `:focus-visible`)?
- Are `tabindex` attributes used correctly (avoiding positive values)?

  ## 3. Screen Reader Support (ARIA)
- Do images have descriptive `alt` text (or empty `alt=""` for decorative images)?
- Are ARIA roles, states, and properties applied correctly to custom UI components (like modals, dropdowns, or tabs)?
- Are form inputs explicitly associated with `<label>` elements?

  ## 4. Contrast & Visuals
- Are you able to identify any obvious color contrast issues based on the provided classes or styles?

For every issue found, provide a description of why it's an accessibility barrier and supply the corrected code block.
```

---

### component-story

> **Description**: Generate Storybook stories for UI components.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `frontend`

#### Template Content:
```markdown
# Storybook Story Generator

Please generate a comprehensive Storybook file (Component Story Format 3.0 / CSF3) for the following React/Vue/UI component:

```
{{args}}
```

Ensure the generated story includes:

  ## 1. Default Setup
- Correct imports (`Meta`, `StoryObj`).
- The `default export` containing the component `title`, the `component` itself, and appropriate `tags: ['autodocs']`.

  ## 2. Argument Types (ArgTypes)
- Define `argTypes` to provide interactive controls for the component's props (e.g., mapping a 'variant' prop to a select dropdown with options).

  ## 3. Stories
Generate multiple story variations representing different states of the component:
- **Default/Primary**: The standard state.
- **Variations**: (e.g., Primary, Secondary, Disabled, Loading, Error).
- **Edge Cases**: How does the component look with extremely long text or missing optional props?

Output the complete, syntactically correct Storybook file.
```

---

### css-tailwind-converter

> **Description**: Convert standard CSS to Tailwind utility classes.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `frontend`

#### Template Content:
```markdown
# CSS to Tailwind Converter

Please convert the following standard CSS/SCSS or inline styles into modern Tailwind CSS utility classes:

```
{{args}}
```

Provide your response in the following format:

  ## 1. Tailwind Classes
Provide the HTML/JSX element with the generated Tailwind classes applied.

  ## 2. Translation Mapping
Briefly map the complex CSS properties to their Tailwind equivalents (e.g., `display: flex; justify-content: center` -> `flex justify-center`).

  ## 3. Custom Configuration (If Needed)
If the CSS includes arbitrary values (like `#ff0033` or `42px`), show how to write them using Tailwind's arbitrary value syntax (e.g., `text-[#ff0033]`) OR suggest how to add them to `tailwind.config.js`.
```

---

## <a name='infra'></a> Infra

### ci-cd-pipeline

> **Description**: Generate CI/CD pipelines (GitHub Actions, GitLab CI, etc.).
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# CI/CD Pipeline Generator

Please generate a comprehensive CI/CD pipeline configuration (e.g., GitHub Actions `.yaml`, GitLab `.gitlab-ci.yml`, or equivalent) based on the following requirements:

```
{{args}}
```

Ensure the generated pipeline follows these modern CI/CD best practices:

  ## 1. Triggers & Workflow Control
- Define clear trigger events (e.g., push to `main`/`master`, pull requests, or manual dispatches).
- Use path or branch filtering to prevent unnecessary pipeline runs.

  ## 2. Environment & Tooling
- Specify the execution environment/runner (e.g., `ubuntu-latest`).
- Set up the specific programming language, Node/Python/Go version, or Docker environment required for the project.

  ## 3. Standard CI Stages
- **Linting & Formatting**: Include a step to check code style.
- **Testing**: Include a step to run unit/integration tests and output coverage reports.
- **Build**: Compile the application or build the Docker image.

  ## 4. Caching & Optimization
- Implement dependency caching (e.g., `actions/cache` or built-in package manager caching) to significantly speed up build times across runs.

  ## 5. Security & Secrets
- Do not hardcode credentials. Demonstrate how to correctly inject environment variables or secrets from the CI provider's secret store (e.g., `${{ secrets.API_KEY }}`).
- Use least-privilege permissions for the CI token (e.g., `permissions: contents: read` in GitHub Actions).

For your response, provide:
1. **The complete CI/CD configuration code.**
2. **A brief explanation** of the stages, caching strategy, and how the user should configure their secrets.
```

---

### dockerfile-generator

> **Description**: Generate optimized, production-ready Dockerfiles.
> **Input Format**: `App Stack or Requirements`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Dockerfile Generator

Please generate a highly optimized, production-ready `Dockerfile` for the following application/stack:

```
{{args}}
```

Ensure the generated Dockerfile adheres to the following best practices:

  ## 1. Multi-Stage Builds
- Use multi-stage builds to separate the build environment from the runtime environment.
- Keep the final production image as small as possible by only copying compiled artifacts or necessary runtime dependencies.

  ## 2. Base Images
- Select lightweight and secure base images (e.g., `alpine`, `distroless`, or slim variants of official images).
- Pin specific versions/tags (avoid using `latest`) to ensure reproducible builds.

  ## 3. Security & Privileges
- **Never run as root.** Create a dedicated non-root user and group, and use the `USER` directive to switch to it before running the application.
- Ensure proper file permissions are set for the application files.

  ## 4. Caching & Performance
- Order instructions to maximize Docker layer caching (e.g., copy dependency manifest files like `package.json` or `requirements.txt` and install dependencies *before* copying the rest of the source code).
- Clean up package manager caches (e.g., `apt-get clean`, `rm -rf /var/lib/apt/lists/*`, or `npm cache clean`) in the same `RUN` step to reduce layer size.

  ## 5. Configuration & Execution
- Use `ENTRYPOINT` for the main executable and `CMD` for default arguments, or provide a clear standard `CMD`.
- Expose necessary ports using the `EXPOSE` directive.
- Include a `.dockerignore` file recommendation to prevent sensitive or unnecessary files from bloating the build context.

For your response, provide:
1. **The `.dockerignore` content.**
2. **The complete `Dockerfile` code.**
3. **A brief explanation** of the optimizations and security measures you applied.
```

---

### iam-policy

> **Description**: Generate AWS IAM or GCP resource policies with least privilege.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `security`, `infra`

#### Template Content:
```markdown
# IAM Policy Generator

Please generate a secure, least-privilege Identity and Access Management (IAM) policy (AWS JSON or GCP YAML/JSON) for the following use case:

```
{{args}}
```

Ensure the generated policy adheres to these best practices:

  ## 1. Principle of Least Privilege
- Only grant the exact actions required to perform the stated task.
- Avoid using wildcards (`*`) for actions unless absolutely necessary.

  ## 2. Resource Scoping
- Restrict the policy to specific resources (e.g., a specific S3 bucket ARN, a specific DynamoDB table) rather than `Resource: "*"`.

  ## 3. Condition Keys (If Applicable)
- Use condition blocks to further restrict access (e.g., `aws:SourceIp`, `aws:MultiFactorAuthPresent`, or `aws:PrincipalTag`).

Provide the complete JSON/YAML policy along with a brief explanation of the permissions granted and the security considerations taken.
```

---

### kubernetes-manifest

> **Description**: Create Kubernetes Deployment and Service YAML manifests.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Kubernetes Manifest Generator

Please generate production-ready Kubernetes YAML manifests (Deployment and Service) for the following application:

```
{{args}}
```

Ensure the generated manifests follow these Kubernetes best practices:

  ## 1. Workload Configuration (Deployment)
- Define a clear `Deployment` structure with an appropriate `replica` count (e.g., at least 2 for high availability).
- Use specific image tags (do not use `latest`).
- Include standard metadata `labels` (e.g., `app.kubernetes.io/name`, `app.kubernetes.io/version`).

  ## 2. Resilience & Health Checks
- Include a `livenessProbe` to restart the container if it deadlocks.
- Include a `readinessProbe` to ensure traffic is only routed to the pod when it is ready to accept requests.
- Provide sensible defaults for probe `initialDelaySeconds`, `periodSeconds`, and `timeoutSeconds`.

  ## 3. Resource Management
- Define explicit `resources.requests` (CPU/Memory) to ensure the pod is scheduled on an appropriate node.
- Define explicit `resources.limits` (CPU/Memory) to prevent the pod from monopolizing node resources.

  ## 4. Security Context
- Add a `securityContext` at the pod or container level (e.g., `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, dropping default capabilities).

  ## 5. Networking (Service)
- Define a corresponding `Service` to expose the deployment.
- Correctly map the `targetPort` (container port) to the `port` (service port).
- Set an appropriate service `type` (e.g., `ClusterIP` for internal, or `LoadBalancer`/`NodePort` if specified in the prompt).

For your response, provide:
1. **The complete YAML manifest** (combining Deployment and Service using `---`).
2. **A brief explanation** of the specific probes, limits, and security contexts chosen for this stack.
```

---

### terraform-module

> **Description**: Write Infrastructure-as-Code Terraform modules.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `infra`

#### Template Content:
```markdown
# Terraform Module Generator

Please generate a well-structured, modular Terraform configuration for the following cloud infrastructure requirements:

```
{{args}}
```

Ensure the generated code adheres to standard Infrastructure-as-Code (IaC) and Terraform best practices:

  ## 1. File Structure
Separate the configuration into standard files. Output the code with clear headers for:
- `main.tf` (The core resource definitions).
- `variables.tf` (Input variables with descriptions and types).
- `outputs.tf` (Return values for consuming modules).
- `providers.tf` (Provider configuration and required versions).

  ## 2. Variable Management
- Use strong typing for variables (e.g., `type = string`, `type = list(string)`).
- Provide a `description` for every variable.
- Provide sensible `default` values where appropriate.
- Mark sensitive variables (like passwords or API keys) with `sensitive = true`.

  ## 3. Naming Conventions & Tagging
- Use standard naming conventions (snake_case) for resources and variables.
- Implement a standard tagging strategy (e.g., `Environment`, `Project`, `ManagedBy = "Terraform"`) and apply it to all applicable resources using local variables or provider default tags.

  ## 4. State & Remote Backend (Optional but Recommended)
- Provide an example of how to configure a remote state backend (e.g., S3 + DynamoDB, or Terraform Cloud) to prevent state file loss.

  ## 5. Best Practices
- Avoid hardcoding values; use variables, locals, or data sources.
- Utilize standard module patterns if applicable.

For your response, provide:
1. **The complete Terraform code**, clearly separated by file name.
2. **A brief summary** of the resources created and any prerequisite steps (like initializing the backend or providing specific credentials).
```

---

## <a name='learning'></a> Learning

### compare-technologies

> **Description**: Compare different technologies.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`

#### Template Content:
```markdown
# Compare Technologies

Please provide a comprehensive comparison of the following technologies:

{{args}}

  ## Technology Comparison Framework

  ### 1. Overview

  #### Technology A
- **Name**: Full name and version
- **Type**: Framework/Library/Language/Tool
- **Created**: Year and creator
- **Current Status**: Active/Mature/Legacy
- **Purpose**: What it's designed for

  #### Technology B
- **Name**: Full name and version
- **Type**: Framework/Library/Language/Tool
- **Created**: Year and creator
- **Current Status**: Active/Mature/Legacy
- **Purpose**: What it's designed for

  ### 2. Quick Comparison Table

| Feature | Technology A | Technology B | Winner |
|---------|-------------|-------------|---------|
| Learning Curve | Easy/Medium/Hard | Easy/Medium/Hard | |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | |
| Community Size | Large/Medium/Small | Large/Medium/Small | |
| Job Market | High/Medium/Low | High/Medium/Low | |
| Maturity | Mature/Growing/Young | Mature/Growing/Young | |
| Documentation | Excellent/Good/Poor | Excellent/Good/Poor | |
| Ecosystem | Rich/Adequate/Limited | Rich/Adequate/Limited | |

  ### 3. Core Philosophy & Approach

  #### Technology A Philosophy
- Design principles
- Core values
- Intended use cases
- Target audience

  #### Technology B Philosophy
- Design principles
- Core values
- Intended use cases
- Target audience

  #### Key Philosophical Differences
What makes them fundamentally different in approach?

  ### 4. Syntax & Developer Experience

  #### Code Comparison

**Technology A:**
```javascript
// Example implementing same feature
```

**Technology B:**
```javascript
// Same feature in different syntax
```

**Analysis:**
- Which is more readable?
- Which is more concise?
- Which is more intuitive?

  ### 5. Performance Comparison

  #### Benchmarks
```
Operation: [Task]
Technology A: Xms
Technology B: Yms
Winner: [A/B] (Z% faster)

Operation: [Task]
Technology A: Xms
Technology B: Yms
Winner: [A/B] (Z% faster)
```

  #### Performance Characteristics
- **Technology A**: When it's faster and why
- **Technology B**: When it's faster and why

  #### Real-World Performance
- Bundle size
- Startup time
- Runtime performance
- Memory usage

  ### 6. Features & Capabilities

  #### Feature Matrix

| Feature | Tech A | Tech B | Notes |
|---------|--------|--------|-------|
| Feature 1 | ✅ | ✅ | |
| Feature 2 | ✅ | ❌ | Only in A |
| Feature 3 | ❌ | ✅ | Only in B |
| Feature 4 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Better in B |

  #### Unique Features
- **Technology A Only**: What it offers exclusively
- **Technology B Only**: What it offers exclusively

  ### 7. Learning Curve

  #### Technology A
- **Time to Basic Proficiency**: X weeks/months
- **Time to Advanced Skills**: Y months/years
- **Prerequisites**: What you need to know first
- **Learning Resources**: Quality and quantity
- **Gotchas**: Common beginner mistakes

  #### Technology B
- **Time to Basic Proficiency**: X weeks/months
- **Time to Advanced Skills**: Y months/years
- **Prerequisites**: What you need to know first
- **Learning Resources**: Quality and quantity
- **Gotchas**: Common beginner mistakes

  ### 8. Ecosystem & Community

  #### Technology A
- **NPM Packages / Libraries**: Number and quality
- **Community Size**: Developer count
- **Stack Overflow Questions**: Activity level
- **GitHub Stars**: Popularity metric
- **Major Companies Using**: Example companies
- **Community Health**: Active/Declining

  #### Technology B
- **NPM Packages / Libraries**: Number and quality
- **Community Size**: Developer count
- **Stack Overflow Questions**: Activity level
- **GitHub Stars**: Popularity metric
- **Major Companies Using**: Example companies
- **Community Health**: Active/Declining

  ### 9. Documentation & Support

  #### Technology A
- **Official Docs**: Quality rating
- **Tutorials**: Availability
- **Examples**: Quantity and quality
- **Books**: Available titles
- **Courses**: Online learning options
- **Support Channels**: Discord, Forum, etc.

  #### Technology B
- **Official Docs**: Quality rating
- **Tutorials**: Availability
- **Examples**: Quantity and quality
- **Books**: Available titles
- **Courses**: Online learning options
- **Support Channels**: Discord, Forum, etc.

  ### 10. Use Case Analysis

  #### When to Choose Technology A
1. **Use Case 1**: Why A is better here
2. **Use Case 2**: Why A is better here
3. **Use Case 3**: Why A is better here

  #### When to Choose Technology B
1. **Use Case 1**: Why B is better here
2. **Use Case 2**: Why B is better here
3. **Use Case 3**: Why B is better here

  ### 11. Pros & Cons

  #### Technology A

**Pros:**
- ✅ Advantage 1
- ✅ Advantage 2
- ✅ Advantage 3

**Cons:**
- ❌ Disadvantage 1
- ❌ Disadvantage 2
- ❌ Disadvantage 3

  #### Technology B

**Pros:**
- ✅ Advantage 1
- ✅ Advantage 2
- ✅ Advantage 3

**Cons:**
- ❌ Disadvantage 1
- ❌ Disadvantage 2
- ❌ Disadvantage 3

  ### 12. Migration Considerations

  #### From A to B
- **Difficulty**: Easy/Medium/Hard
- **Migration Tools**: Available automation
- **Breaking Changes**: Major differences
- **Estimated Time**: For typical project
- **Worth It?**: Is migration recommended?

  #### From B to A
- **Difficulty**: Easy/Medium/Hard
- **Migration Tools**: Available automation
- **Breaking Changes**: Major differences
- **Estimated Time**: For typical project
- **Worth It?**: Is migration recommended?

  ### 13. Future Outlook

  #### Technology A
- **Development Activity**: Active/Moderate/Slow
- **Roadmap**: Upcoming features
- **Industry Trends**: Growing/Stable/Declining
- **Long-term Viability**: 5-year outlook

  #### Technology B
- **Development Activity**: Active/Moderate/Slow
- **Roadmap**: Upcoming features
- **Industry Trends**: Growing/Stable/Declining
- **Long-term Viability**: 5-year outlook

  ### 14. Job Market

  #### Technology A
- **Job Openings**: Number of positions
- **Salary Range**: Average compensation
- **Geographic Distribution**: Where jobs are
- **Growth Trend**: Increasing/Stable/Decreasing

  #### Technology B
- **Job Openings**: Number of positions
- **Salary Range**: Average compensation
- **Geographic Distribution**: Where jobs are
- **Growth Trend**: Increasing/Stable/Decreasing

  ### 15. Decision Matrix

Help make the choice based on priorities:

```
If you prioritize:
- Performance → Choose [A/B] because...
- Ease of Learning → Choose [A/B] because...
- Job Opportunities → Choose [A/B] because...
- Ecosystem → Choose [A/B] because...
- Modern Features → Choose [A/B] because...
- Stability → Choose [A/B] because...
- Community Support → Choose [A/B] because...
```

  ### 16. Real-World Project Comparison

**Same Project Built with Both:**

**Technology A Version:**
- Lines of code
- Development time
- Performance metrics
- Developer experience
- Maintenance burden

**Technology B Version:**
- Lines of code
- Development time
- Performance metrics
- Developer experience
- Maintenance burden

  ### 17. Expert Opinions

What industry experts say:

**About Technology A:**
- Quote/opinion from expert 1
- Quote/opinion from expert 2

**About Technology B:**
- Quote/opinion from expert 1
- Quote/opinion from expert 2

  ### 18. Final Recommendation

  #### Choose Technology A if:
- Condition 1
- Condition 2
- Condition 3

  #### Choose Technology B if:
- Condition 1
- Condition 2
- Condition 3

  #### Use Both if:
- Scenario where both are appropriate

  #### Avoid Both if:
- When neither is suitable

  ### 19. Learning Path

  #### To Learn Technology A:
1. Start with [resource]
2. Then [next step]
3. Practice by [project idea]

  #### To Learn Technology B:
1. Start with [resource]
2. Then [next step]
3. Practice by [project idea]

  ## Comparison Principles

1. **Be Objective**: Present facts, not opinions
2. **Be Balanced**: Show pros/cons of both fairly
3. **Be Specific**: Use concrete examples and data
4. **Be Current**: Use latest versions and info
5. **Be Practical**: Focus on real-world usage
6. **Be Honest**: Acknowledge limitations
7. **Be Helpful**: Guide decision-making

Generate a comprehensive, balanced comparison following this framework.
```

---

### eli5

> **Description**: Explain like I'm 5 (simple explanations).
> **Input Format**: `Technical Concept`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`

#### Template Content:
```markdown
# Explain Like I'm 5 (ELI5)

Please explain the following concept in the simplest possible terms:

{{args}}

  ## ELI5 Explanation Guidelines

  ### 1. Use Simple Language
- Avoid technical jargon completely
- Use everyday words
- Short, simple sentences
- No acronyms unless explained

  ### 2. Relate to Everyday Life
Use analogies from common experiences:
- Food and cooking
- Playing games
- Family and friends
- School and playground
- Toys and activities
- Animals and nature
- Sports

  ### 3. Tell a Story
Make it narrative and engaging:
- Use characters
- Create a scenario
- Show cause and effect
- Make it relatable

  ### 4. Break It Down
Explain step by step:
- What it is
- Why it exists
- How it works
- Why it matters

  ### 5. Use Visual Metaphors
Paint a mental picture:
- "Imagine..."
- "Think of it like..."
- "It's similar to..."
- "Picture this..."

  ## ELI5 Structure

  ### The Super Simple Explanation
One or two sentences that capture the essence:

"[Concept] is like [everyday thing]. It helps us [benefit] just like how [analogy]."

  ### The Story Explanation
A short story or scenario that demonstrates the concept:

```
Once upon a time, there was [character] who wanted to [goal].
But they had a problem: [problem].

So they used [concept] which works like this:
[Step 1 using simple analogy]
[Step 2 using simple analogy]
[Step 3 using simple analogy]

And that's how [character] solved their problem!
```

  ### The Analogy Explanation
Multiple analogies from different perspectives:

**Food Analogy:**
"Think of [concept] like [food example]. When you [action], it's like [food process]..."

**Game Analogy:**
"It's like playing [game]. The rules are [simple rules], and you win when [outcome]..."

**Building Analogy:**
"Imagine building with LEGO blocks. [Concept] is like [building process]..."

  ### The Visual Explanation
Simple diagrams or step-by-step pictures (ASCII art):

```
Before:
[Simple visual showing problem]

After using [concept]:
[Simple visual showing solution]
```

  ### Why Should You Care?
Explain the benefit in simple terms:

"This is important because [simple benefit that matters to everyone]."

  ### Example in Real Life
A concrete example they can relate to:

"You know how [common experience]? Well, [concept] is what makes that possible!"

  ## Example Format

**Explaining "Database":**

**Super Simple:**
A database is like a giant, organized filing cabinet for computers. Instead of paper files, it stores digital information so you can find it quickly.

**Story:**
Imagine you have a huge toy collection with hundreds of toys. At first, you just threw them all in a big box. Finding your favorite toy takes forever!

So you get smart and use lots of smaller boxes:
- One box for cars
- One box for action figures
- One box for building blocks
- Labels on each box

Now when you want your red race car, you know exactly which box to look in. You can find it in seconds!

That's what a database does - it organizes information into neat boxes (called "tables") so the computer can find what it needs super fast.

**Real Life:**
When you search for your friend on Instagram, Instagram uses a database to look through millions of people and find your friend in less than a second. Without a database, it would be like looking through a pile of billions of photos!

**Why It's Cool:**
Databases are why apps work so fast. They're the reason you can:
- Find any YouTube video instantly
- See your bank balance right away
- Look up your grades in seconds

Without databases, we'd still be waiting minutes or hours for computers to find information!

  ## Writing Tips

1. **Test it on a real 5-year-old** (mentally): Would they understand?
2. **One concept at a time**: Don't introduce multiple ideas
3. **Be patient**: Repeat the key point in different ways
4. **Use "you" language**: Make it personal and engaging
5. **Show don't tell**: Use examples instead of definitions
6. **Keep it fun**: Use humor and relatable situations
7. **Avoid conditionals**: Don't say "if you understand X, then Y"
8. **No prerequisites**: Assume zero prior knowledge

  ## What NOT to Do

❌ Don't use technical terms without explaining
❌ Don't assume prior knowledge
❌ Don't make it too abstract
❌ Don't use complex sentence structures
❌ Don't skip the "why it matters"
❌ Don't make it boring
❌ Don't condescend (talk down)

  ## What TO Do

✅ Use simple, concrete examples
✅ Relate to their world
✅ Make it fun and engaging
✅ Show practical benefits
✅ Use repetition for key points
✅ Build from known to unknown
✅ Encourage curiosity

Generate a comprehensive ELI5 explanation that a 5-year-old (or complete beginner) can understand and find interesting.
```

---

### explain-concept

> **Description**: Explain technical concepts clearly.
> **Input Format**: `Technical Concept`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`

#### Template Content:
```markdown
# Explain Technical Concept

Please provide a comprehensive explanation of the following technical concept:

{{args}}

  ## Explanation Structure

  ### 1. Simple Definition (ELI5 Level)
Start with a simple, intuitive explanation that anyone can understand:
- Use everyday analogies
- Avoid technical jargon
- Focus on the "what" and "why"
- Make it relatable

**Example format:**
"Imagine [everyday analogy]. That's basically how [concept] works..."

  ### 2. Intermediate Explanation
Build on the simple definition with more detail:
- Introduce key terminology
- Explain how it works
- Common use cases
- When and why it's used

  ### 3. Technical Deep Dive
Provide detailed technical explanation:
- Precise technical definition
- Underlying mechanisms
- Implementation details
- Performance characteristics
- Trade-offs and limitations

  ### 4. Visual Representation
Use ASCII diagrams or step-by-step illustrations:
```
Step 1: [Description]
   ┌───────┐
   │  A    │
   └───┬───┘
       │
Step 2: [Description]
   ┌───▼───┐
   │  B    │
   └───────┘
```

  ### 5. Code Examples

  #### Basic Example
```javascript
// Simple, clear example showing the concept
```

  #### Real-World Example
```javascript
// Practical use case
```

  #### Advanced Example
```javascript
// Complex scenario with edge cases
```

  ### 6. Key Concepts & Terminology

**Term 1**: Definition
**Term 2**: Definition
**Term 3**: Definition

  ### 7. Common Use Cases

When to use this concept:
1. **Use Case 1**: Description and example
2. **Use Case 2**: Description and example
3. **Use Case 3**: Description and example

  ### 8. Common Misconceptions

**Misconception 1**: "People think X..."
- **Reality**: "Actually, Y because..."

**Misconception 2**: "Many believe X..."
- **Reality**: "In fact, Y..."

  ### 9. Comparison with Related Concepts

  #### vs Concept A
- **Similarities**: What they have in common
- **Differences**: How they differ
- **When to use each**: Decision criteria

  #### vs Concept B
- **Similarities**: What they have in common
- **Differences**: How they differ
- **When to use each**: Decision criteria

  ### 10. Advantages & Disadvantages

  #### Advantages
- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

  #### Disadvantages
- ❌ Limitation 1
- ❌ Limitation 2
- ❌ Limitation 3

  ### 11. Best Practices

1. **Practice 1**: Description and why it matters
2. **Practice 2**: Description and why it matters
3. **Practice 3**: Description and why it matters

  ### 12. Common Pitfalls

**Pitfall 1**: What to avoid and why
**Pitfall 2**: What to avoid and why
**Pitfall 3**: What to avoid and why

  ### 13. Real-World Applications

Where this concept is used in practice:
- **Industry/Domain 1**: Specific application
- **Industry/Domain 2**: Specific application
- **Popular tools/frameworks**: How they use it

  ### 14. Historical Context (if relevant)

- When was it introduced?
- What problem did it solve?
- How has it evolved?
- Who created/popularized it?

  ### 15. Learning Resources

  #### For Beginners
- Resource 1 (Article/Video)
- Resource 2 (Tutorial)

  #### For Intermediate
- Resource 1 (Book/Course)
- Resource 2 (Documentation)

  #### For Advanced
- Resource 1 (Research paper)
- Resource 2 (Deep dive)

  ### 16. Hands-On Exercise

Provide a practical exercise to reinforce understanding:

**Challenge**: Build/implement something using this concept

**Steps**:
1. Step 1
2. Step 2
3. Step 3

**Solution**:
```javascript
// Implementation
```

  ### 17. Interview Questions

Common questions about this concept:
1. **Q**: Question 1
   **A**: Answer with explanation

2. **Q**: Question 2
   **A**: Answer with explanation

3. **Q**: Question 3
   **A**: Answer with explanation

  ### 18. Related Concepts to Explore

- **Concept A**: Why it's related and worth learning
- **Concept B**: Why it's related and worth learning
- **Concept C**: Why it's related and worth learning

  ## Explanation Guidelines

1. **Progressive Complexity**: Start simple, build up gradually
2. **Multiple Perspectives**: Explain from different angles
3. **Concrete Examples**: Always provide code/practical examples
4. **Visual Aids**: Use diagrams where helpful
5. **Analogies**: Make abstract concepts tangible
6. **Context**: Explain when/why to use it
7. **Completeness**: Cover common questions and edge cases
8. **Accuracy**: Ensure technical correctness
9. **Clarity**: Use clear, precise language
10. **Engagement**: Make it interesting and relatable

Generate a comprehensive, multi-level explanation following this structure.
```

---

### learning-path

> **Description**: Create learning roadmaps.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`

#### Template Content:
```markdown
# Create Learning Roadmap

Please create a comprehensive learning roadmap for:

{{args}}

  ## Learning Roadmap Structure

  ### 1. Current State Assessment

  #### Prerequisites Check
What you should know before starting:
- ☐ Prerequisite 1
- ☐ Prerequisite 2
- ☐ Prerequisite 3

  #### Skill Level Check
Which level are you?
- [ ] **Complete Beginner**: Never touched this topic
- [ ] **Novice**: Familiar with basics
- [ ] **Intermediate**: Can build projects
- [ ] **Advanced**: Production experience
- [ ] **Expert**: Deep expertise

  ### 2. Learning Goals

  #### Short-term Goals (1-3 months)
- [ ] Goal 1: Specific, measurable outcome
- [ ] Goal 2: Specific, measurable outcome
- [ ] Goal 3: Specific, measurable outcome

  #### Medium-term Goals (3-6 months)
- [ ] Goal 1: Specific, measurable outcome
- [ ] Goal 2: Specific, measurable outcome
- [ ] Goal 3: Specific, measurable outcome

  #### Long-term Goals (6-12 months)
- [ ] Goal 1: Specific, measurable outcome
- [ ] Goal 2: Specific, measurable outcome
- [ ] Goal 3: Specific, measurable outcome

  ### 3. Complete Learning Path

  ## Phase 1: Foundations (Weeks 1-4)

  ### Week 1: Getting Started
**Focus**: Core concepts and setup

**Topics to Learn:**
- [ ] Topic 1: What it is and why it matters
- [ ] Topic 2: Core terminology
- [ ] Topic 3: Development environment setup

**Resources:**
- 📚 [Resource 1]: Type (Article/Video/Course)
- 📚 [Resource 2]: Type
- 📚 [Resource 3]: Type

**Practice Projects:**
1. **Project 1**: Simple starter project
   - Description: What you'll build
   - Skills practiced: What you'll learn
   - Time: Estimated hours

**Milestone**: By end of week, you should be able to [specific achievement]

---

  ### Week 2: Building Blocks
**Focus**: Core features and patterns

**Topics to Learn:**
- [ ] Topic 1
- [ ] Topic 2
- [ ] Topic 3

**Resources:**
- 📚 [Resource 1]
- 📚 [Resource 2]

**Practice Projects:**
1. **Project 1**: Description
   - Skills: What you'll practice
   - Time: X hours

**Milestone**: [Specific achievement]

---

  ### Week 3-4: First Real Project
**Focus**: Applying fundamentals

**Project**: Build [specific application]

**Requirements:**
- Feature 1
- Feature 2
- Feature 3

**Learning Objectives:**
- Objective 1
- Objective 2
- Objective 3

**Resources:**
- Tutorial: [Link]
- Documentation: [Link]

**Deliverable**: Completed project with [features]

---

  ## Phase 2: Intermediate Skills (Weeks 5-12)

  ### Week 5-6: Advanced Concepts
**Focus**: Deeper understanding

**Topics:**
- [ ] Advanced topic 1
- [ ] Advanced topic 2
- [ ] Advanced topic 3

**Resources:**
- Book: [Title] (Chapters X-Y)
- Course: [Name] (Modules X-Y)
- Documentation: [Official docs section]

**Practice:**
- Exercise 1
- Exercise 2

**Milestone**: [Achievement]

---

  ### Week 7-8: Best Practices
**Focus**: Professional patterns

**Topics:**
- [ ] Code organization
- [ ] Testing strategies
- [ ] Performance optimization
- [ ] Security practices

**Resources:**
- Guide: [Link]
- Examples: [Repository]

**Project**: Refactor previous project with best practices

---

  ### Week 9-12: Intermediate Project
**Focus**: Building complete application

**Project**: [Full-stack / Complex application]

**Features:**
- Feature 1 (with complexity)
- Feature 2 (with complexity)
- Feature 3 (with complexity)

**Technologies to integrate:**
- Technology 1
- Technology 2
- Technology 3

**Deliverable**: Production-ready application

---

  ## Phase 3: Advanced Topics (Weeks 13-20)

  ### Week 13-14: Performance & Optimization
**Topics:**
- [ ] Performance profiling
- [ ] Optimization techniques
- [ ] Caching strategies
- [ ] Scaling considerations

**Resources:**
- Article: [Link]
- Video series: [Link]

**Practice:**
- Optimize previous projects
- Benchmark and compare

---

  ### Week 15-16: Testing & Quality
**Topics:**
- [ ] Unit testing
- [ ] Integration testing
- [ ] E2E testing
- [ ] Test-driven development

**Resources:**
- Guide: [Link]
- Examples: [Repository]

**Practice:**
- Add tests to previous projects
- Achieve 80%+ coverage

---

  ### Week 17-20: Advanced Project
**Focus**: Industry-level application

**Project**: [Complex, production-grade application]

**Requirements:**
- Professional architecture
- Comprehensive testing
- Performance optimized
- Security hardened
- Fully documented

**Deliverable**: Portfolio-worthy project

---

  ## Phase 4: Specialization (Weeks 21-24)

  ### Choose Your Path:

  #### Path A: [Specialization 1]
**Topics:**
- Topic 1
- Topic 2
- Topic 3

**Resources:**
- Resource 1
- Resource 2

**Project**: [Specialized project]

  #### Path B: [Specialization 2]
**Topics:**
- Topic 1
- Topic 2
- Topic 3

**Resources:**
- Resource 1
- Resource 2

**Project**: [Specialized project]

---

  ## Phase 5: Mastery (Months 7-12)

  ### Contributing to Open Source
- [ ] Find project to contribute to
- [ ] Make first contribution
- [ ] Regular contributions

  ### Building Portfolio
- [ ] Personal website/portfolio
- [ ] 3-5 polished projects
- [ ] Blog posts about learning
- [ ] GitHub profile showcase

  ### Community Engagement
- [ ] Answer questions (Stack Overflow, forums)
- [ ] Write tutorials/articles
- [ ] Give talks or workshops
- [ ] Mentor others

  ### Advanced Topics
- [ ] Advanced topic 1
- [ ] Advanced topic 2
- [ ] Advanced topic 3

---

  ### 4. Daily/Weekly Schedule

  #### Daily Routine (2-3 hours)
- **30 min**: Reading/watching tutorials
- **90 min**: Hands-on coding practice
- **30 min**: Review and reflection

  #### Weekly Routine
- **Monday-Friday**: Daily practice (2-3 hrs)
- **Saturday**: Work on project (4-6 hrs)
- **Sunday**: Review week, plan next week (1-2 hrs)

  ### 5. Resource Library

  #### Essential Books
1. **Book 1**: Title (Best for beginners)
2. **Book 2**: Title (Intermediate)
3. **Book 3**: Title (Advanced)

  #### Online Courses
1. **Course 1**: Platform (Duration, Level)
2. **Course 2**: Platform (Duration, Level)
3. **Course 3**: Platform (Duration, Level)

  #### Documentation
- Official docs: [Link]
- API reference: [Link]
- Guides: [Link]

  #### Practice Platforms
- Platform 1: [Link] (Type of exercises)
- Platform 2: [Link] (Type of exercises)

  #### Community Resources
- Forum: [Link]
- Discord/Slack: [Link]
- Reddit: [Link]
- Newsletter: [Link]

  ### 6. Project Ideas by Level

  #### Beginner Projects
1. **Project 1**: Description (Skills: X, Y, Z)
2. **Project 2**: Description (Skills: X, Y, Z)
3. **Project 3**: Description (Skills: X, Y, Z)

  #### Intermediate Projects
1. **Project 1**: Description (Skills: X, Y, Z)
2. **Project 2**: Description (Skills: X, Y, Z)
3. **Project 3**: Description (Skills: X, Y, Z)

  #### Advanced Projects
1. **Project 1**: Description (Skills: X, Y, Z)
2. **Project 2**: Description (Skills: X, Y, Z)
3. **Project 3**: Description (Skills: X, Y, Z)

  ### 7. Common Pitfalls & How to Avoid

**Pitfall 1**: Tutorial Hell
- **Problem**: Just following tutorials without building
- **Solution**: Build projects independently after each tutorial

**Pitfall 2**: Rushing Ahead
- **Problem**: Skipping fundamentals
- **Solution**: Master basics before advancing

**Pitfall 3**: Not Practicing Enough
- **Problem**: Too much theory, not enough coding
- **Solution**: 70% hands-on, 30% learning

**Pitfall 4**: Analysis Paralysis
- **Problem**: Too many resources, can't decide
- **Solution**: Pick one path and stick to it

  ### 8. Tracking Progress

  #### Weekly Checklist
- [ ] Completed learning goals
- [ ] Finished practice exercises
- [ ] Made project progress
- [ ] Reviewed previous material
- [ ] Noted challenges and questions

  #### Monthly Review
- [ ] Achieved monthly milestones
- [ ] Built planned projects
- [ ] Updated portfolio
- [ ] Adjusted roadmap if needed

  ### 9. Staying Motivated

  #### Tips:
- Join a community
- Find an accountability partner
- Celebrate small wins
- Keep a learning journal
- Build projects you're passionate about
- Take breaks when needed

  #### When You're Stuck:
1. Review fundamentals
2. Ask for help in communities
3. Take a different approach
4. Build something simpler first
5. Take a break and come back fresh

  ### 10. Next Steps After Completion

- [ ] Build a portfolio website
- [ ] Apply knowledge in job/freelance
- [ ] Contribute to open source
- [ ] Learn complementary skills
- [ ] Teach others what you've learned
- [ ] Start advanced specialization

Generate a detailed, actionable learning roadmap following this structure.
```

---

### prompt-best-practices

> **Description**: Learn prompt engineering tips.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`, `prompt-engineering`

#### Template Content:
```markdown
# Prompt Engineering Best Practices

Please provide best practices and tips for prompt engineering related to:

{{args}}

  ## Core Prompt Engineering Principles

  ### 1. Clarity and Specificity

  #### Be Explicit
**Bad:**
```
Write code
```

**Good:**
```
Write a Python function that:
- Takes a list of integers as input
- Returns the sum of even numbers
- Handles empty lists
- Includes type hints
- Has docstring documentation
```

**Why:** AI models perform better with clear, specific instructions.

---

  #### Define the Role
**Bad:**
```
Explain databases
```

**Good:**
```
You are a database expert teaching beginners. Explain what databases are using simple language and everyday analogies.
```

**Why:** Role-setting provides context and adjusts the response style.

---

  #### Specify Output Format
**Bad:**
```
Tell me about error handling
```

**Good:**
```
Explain error handling in the following format:
1. Definition (2-3 sentences)
2. Why it matters (1 paragraph)
3. Code example with comments
4. Common mistakes to avoid (3-5 bullet points)
```

**Why:** Structured outputs are more useful and consistent.

---

  ### 2. Context and Background

  #### Provide Sufficient Context
**Bad:**
```
Fix this code: [code snippet]
```

**Good:**
```
Context: I'm building a React application for e-commerce.
Problem: This checkout component crashes when users have empty carts.
Expected: Should display "Cart is empty" message instead.

Code to fix:
[code snippet]
```

**Why:** Context helps the AI understand the problem domain and constraints.

---

  #### Include Constraints
**Bad:**
```
Design a database schema
```

**Good:**
```
Design a database schema for a blog with these constraints:
- Must support PostgreSQL
- Expected 1M users, 10M posts
- Need to query posts by author quickly
- Must support tags (many-to-many)
- Follow 3NF normalization
```

**Why:** Constraints guide the solution toward practical, feasible answers.

---

  ### 3. Examples and Demonstrations

  #### Use Few-Shot Learning
**Pattern:**
```
Here are examples of what I want:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now do the same for:
Input: [your actual input]
```

**Why:** Examples teach the AI the pattern you want.

---

  #### Show Good and Bad Examples
```
Good example:
✅ [Show correct approach]

Bad example:
❌ [Show wrong approach]

Now apply this to: [your case]
```

**Why:** Contrasts clarify expectations.

---

  ### 4. Step-by-Step Decomposition

  #### Break Complex Tasks
**Bad:**
```
Build a full authentication system
```

**Good:**
```
Let's build an authentication system step by step:

Step 1: Design the user schema
- What fields do we need?
- What constraints?

Step 2: Implement registration
- Input validation
- Password hashing
- Database storage

Step 3: Implement login
- Credential verification
- JWT generation
- Error handling

Let's start with Step 1.
```

**Why:** Complex tasks are easier to handle in pieces.

---

  #### Chain of Thought
```
Think through this problem step by step:

1. First, identify the inputs and outputs
2. Then, consider edge cases
3. Next, outline the algorithm
4. Finally, write the code

Show your reasoning for each step.
```

**Why:** Encourages logical, thorough responses.

---

  ### 5. Output Quality Control

  #### Request Self-Critique
```
[Your prompt]

After providing your answer, critique it by identifying:
1. Potential issues or edge cases missed
2. Alternative approaches
3. Improvements that could be made
```

**Why:** Prompts self-reflection leading to better answers.

---

  #### Ask for Multiple Options
```
Provide 3 different approaches to solve this problem:
1. Approach A: [optimized for performance]
2. Approach B: [optimized for readability]
3. Approach C: [optimized for maintainability]

For each, explain pros and cons.
```

**Why:** Comparison helps you choose the best solution.

---

  ### 6. Constraints and Boundaries

  #### Set Scope Limits
```
Limit your response to:
- Maximum 200 lines of code
- Only use standard library (no external dependencies)
- Must work in Python 3.8+
- Response should be under 500 words
```

**Why:** Prevents overly complex or lengthy responses.

---

  #### Specify What to Avoid
```
Requirements:
- Do NOT use deprecated APIs
- Do NOT include comments explaining every line
- Do NOT make assumptions about user input
- Do NOT use global variables
```

**Why:** Explicitly ruling out unwanted approaches.

---

  ### 7. Iterative Refinement

  #### Version 1: Basic Prompt
```
Explain async/await in JavaScript
```

**Response:** Too basic or too complex

---

  #### Version 2: Add Context
```
Explain async/await in JavaScript to an intermediate developer who understands callbacks and promises.
```

**Response:** Better but still generic

---

  #### Version 3: Add Structure
```
Explain async/await in JavaScript to an intermediate developer:

1. Quick definition (2-3 sentences)
2. How it relates to promises
3. Code example showing conversion from promises to async/await
4. Common pitfalls
5. When to use vs when not to use
```

**Response:** Much more targeted and useful

---

  ### 8. Prompt Patterns

  #### The Template Pattern
```
You are a [role].
Your task is to [objective].

Given:
{{input}}

Requirements:
- [requirement 1]
- [requirement 2]

Output format:
[specify structure]
```

---

  #### The Persona Pattern
```
Act as a [expert type] with [years] of experience in [domain].
You are known for [characteristics].
Your communication style is [style].

[Rest of prompt]
```

---

  #### The Refinement Pattern
```
[Initial prompt]

Please refine your answer by:
1. Adding more specific examples
2. Addressing edge case X
3. Explaining assumption Y
```

---

  #### The Comparison Pattern
```
Compare and contrast [A] vs [B] in the following dimensions:
- Performance
- Ease of use
- Scalability
- Cost
- Maintenance

Provide specific examples for each dimension.
```

---

  #### The Constraint Pattern
```
Given these constraints:
- Constraint 1
- Constraint 2
- Constraint 3

[Task description]

If any constraint cannot be satisfied, explain why and suggest alternatives.
```

---

  ### 9. Common Prompt Mistakes

  #### Mistake 1: Too Vague
❌ "Make it better"
✅ "Improve performance by reducing time complexity from O(n²) to O(n log n)"

  #### Mistake 2: Assuming Context
❌ "Add validation to the form"
✅ "Add email validation to the registration form, checking for: valid format, not already registered, and not from blacklisted domains"

  #### Mistake 3: Multiple Unrelated Tasks
❌ "Build a login system, write tests, create documentation, and deploy it"
✅ "First, let's build the login system. We'll handle tests, docs, and deployment in separate steps."

  #### Mistake 4: No Success Criteria
❌ "Optimize this function"
✅ "Optimize this function to run in under 100ms for inputs up to 10,000 elements"

  #### Mistake 5: Ambiguous Pronouns
❌ "It should connect to it using that"
✅ "The client should connect to the database using connection pooling"

---

  ### 10. Domain-Specific Best Practices

  #### For Code Generation
```
Generate [language] code that:
- Function/class name and purpose
- Input parameters with types
- Return type
- Error handling approach
- Edge cases to handle
- Performance requirements
- Code style preferences
```

  #### For Code Review
```
Review this [language] code for:
1. Security vulnerabilities
2. Performance issues
3. Code quality and maintainability
4. Best practices violations
5. Edge cases not handled

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Explanation
- Fix recommendation
- Example of corrected code
```

  #### For Explanations
```
Explain [concept] with:
1. Simple analogy (ELI5 level)
2. Technical definition
3. Real-world use case
4. Code example
5. Common misconceptions
6. Related concepts

Assume audience: [skill level]
```

  #### For Documentation
```
Create documentation for [code/feature] including:
- Overview (what it does, why it exists)
- Prerequisites
- Installation/setup steps
- Usage examples (basic and advanced)
- API reference
- Common issues and solutions
- Best practices
```

---

  ### 11. Testing Your Prompts

  #### Quality Checklist
- [ ] Is the objective clear?
- [ ] Is the role/context defined?
- [ ] Are constraints specified?
- [ ] Is output format defined?
- [ ] Are examples provided?
- [ ] Are edge cases mentioned?
- [ ] Is success criteria clear?

  #### Test Cases
1. **Minimal input**: Does it work with bare minimum?
2. **Complex input**: Does it handle complexity?
3. **Edge cases**: Does it handle unusual inputs?
4. **Ambiguity**: Could it be misinterpreted?

---

  ### 12. Advanced Techniques

  #### Meta-Prompting
```
Before answering, ask yourself:
- What information is missing?
- What assumptions am I making?
- What edge cases exist?

Then provide your answer addressing these points.
```

  #### Prompt Chaining
```
Prompt 1: Analyze the requirements
Prompt 2: Based on the analysis, design the solution
Prompt 3: Based on the design, implement the code
Prompt 4: Based on the code, write tests
```

  #### Self-Consistency
```
Solve this problem 3 different ways, then:
1. Compare the solutions
2. Identify the best approach
3. Explain why it's best
```

---

  ### 13. Optimization Tips

  #### For Conciseness
- Use bullet points instead of paragraphs for requirements
- Reference examples instead of repeating them
- Use abbreviations consistently (define once)

  #### For Accuracy
- Specify versions (Python 3.10, React 18)
- Include units (milliseconds, MB, percentage)
- Define technical terms
- Provide examples of correct output

  #### For Consistency
- Use templates for similar tasks
- Maintain same structure across prompts
- Define terms consistently
- Use same variable naming

---

  ### 14. Prompt Engineering Workflow

1. **Define Goal**: What do you want to achieve?
2. **Draft Initial Prompt**: Write first version
3. **Test**: Try it out
4. **Analyze Results**: What's good? What's missing?
5. **Refine**: Add specificity, examples, constraints
6. **Re-test**: Try refined version
7. **Iterate**: Repeat until satisfactory
8. **Document**: Save successful prompts for reuse

---

  ### 15. Resources and Further Learning

  #### Key Principles to Remember
1. **Clarity over brevity**: Be detailed, not terse
2. **Show, don't just tell**: Use examples
3. **Structure matters**: Format output explicitly
4. **Context is king**: Provide background
5. **Iterate and refine**: First drafts rarely perfect
6. **Test edge cases**: Think about what could go wrong
7. **Be specific**: Vague prompts = vague answers
8. **Set boundaries**: Define what you don't want

Generate comprehensive prompt engineering guidance following these best practices.
```

---

### prompt-versioning

> **Description**: Guide for managing and versioning prompt templates.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`, `prompt-engineering`

#### Template Content:
```markdown
# Prompt Versioning & Lifecycle Management

Please provide a comprehensive guide and strategy for versioning and managing the lifecycle of the following prompt template or set of prompts:

```
{{args}}
```

Provide your response in the following structured format:

  ## 1. Prompt Semantic Versioning (PSemVer)
Explain how to apply Semantic Versioning to this prompt:
- **Major (X.0.0)**: When to increment (e.g., changing the core task, switching models, or altering mandatory output structure).
- **Minor (0.X.0)**: When to increment (e.g., adding new optional instructions, significantly refining existing guidance, or adding new variables).
- **Patch (0.0.X)**: When to increment (e.g., fixing typos, minor wording tweaks that don't change intent, or formatting updates).

  ## 2. Change Tracking & Documentation
- Suggest a format for an internal `CHANGELOG` within the prompt file or a separate repository.
- How to document the "Why" behind a prompt update (e.g., "Improved response length", "Fixed hallucinations in edge cases").

  ## 3. Testing & Validation Strategy
- **Golden Sets**: How to maintain a set of "ideal" inputs and outputs to test new prompt versions against.
- **A/B Testing**: How to run parallel tests between two prompt versions to measure performance improvements.
- **Regression Testing**: Ensuring a new version doesn't break previously working cases.

  ## 4. Environment & Deployment States
Suggest how to manage prompt states across different environments:
- **Draft**: Initial creation and internal testing.
- **Staging**: Testing with real-world data in a safe environment.
- **Production**: The current "live" version.
- **Deprecated**: Older versions that are no longer recommended but might still be in use.

  ## 5. Automation & Tooling
Suggest tools or scripts to automate:
- Version tagging in Git.
- Automated testing of prompts using LLM-as-a-judge.
- Deployment of updated prompts to production APIs.

Provide a clear, actionable roadmap for implementing this versioning strategy.
```

---

### simplify-jargon

> **Description**: Simplify technical jargon.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`

#### Template Content:
```markdown
# Technical Jargon Simplification

Please take the following highly technical text or concept and translate it into clear, accessible language for a non-technical audience:

```
{{args}}
```

Please structure your explanation as follows:

  ## 1. The "Explain Like I'm 5" (ELI5) Analogy
- Provide a simple, relatable real-world analogy that captures the core concept.

  ## 2. The Plain English Translation
- Rewrite the original text, stripping out all jargon, acronyms, and overly complex phrasing. 
- Keep the sentences short and punchy.
- Focus on *what it means* and *why it matters*, rather than how it works under the hood.

  ## 3. Key Terms Unpacked (Optional)
- If there are 1-3 absolutely essential technical terms the reader *must* know, define them simply here. Otherwise, omit this section.

  ## 4. Real-World Value
- Give a concrete example of how this concept affects a regular user or a business in their day-to-day operations.
```

---

## <a name='prompt-engineering'></a> Prompt Engineering

### create-prompt-template

> **Description**: Create reusable prompt templates.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `prompt-engineering`

#### Template Content:
```markdown
# Create Prompt Template

Please create a reusable prompt template for:

{{args}}

  ## Prompt Template Structure

  ### 1. Template Metadata

**Template Name**: Clear, descriptive name

**Category**: Type of prompt (Technical, Creative, Analysis, etc.)

**Purpose**: What this prompt accomplishes

**Use Cases**: When to use this template
- Use case 1
- Use case 2
- Use case 3

**Target Audience**: Who should use this
- Skill level
- Role
- Context

  ### 2. Template Variables

Define all customizable parts:

**Required Variables:**
- `{{variable1}}`: Description of what goes here
- `{{variable2}}`: Description of what goes here

**Optional Variables:**
- `{{optionalVar}}`: Description (defaults to: X)

**Example Values:**
```
{{variable1}}: "Example input here"
{{variable2}}: "Another example"
```

  ### 3. The Prompt Template

```
[ROLE/CONTEXT]
You are a [role] helping with [task].

[OBJECTIVE]
Your goal is to [primary objective] based on the following [input type]:

{{variable1}}

[CONSTRAINTS/REQUIREMENTS]
Please ensure:
- Requirement 1
- Requirement 2
- Requirement 3

[OUTPUT FORMAT]
Provide your response in the following format:

## Section 1: [Name]
[Description of what goes here]

## Section 2: [Name]
[Description of what goes here]

## Section 3: [Name]
[Description of what goes here]

[ADDITIONAL GUIDELINES]
- Guideline 1
- Guideline 2
- Guideline 3

[EXAMPLES] (if helpful)
Example input:
```
[sample input]
```

Expected output:
```
[sample output]
```
```

  ### 4. Prompt Engineering Best Practices Applied

  #### Clarity
- ✅ Clear role definition
- ✅ Explicit objective
- ✅ Specific requirements
- ✅ Defined output format

  #### Completeness
- ✅ All necessary context provided
- ✅ Edge cases considered
- ✅ Examples included
- ✅ Constraints specified

  #### Flexibility
- ✅ Variables for customization
- ✅ Optional parameters
- ✅ Adaptable to different inputs

  #### Effectiveness
- ✅ Structured output
- ✅ Clear expectations
- ✅ Actionable instructions
- ✅ Quality guidelines

  ### 5. Usage Instructions

  #### How to Use This Template

**Step 1: Prepare Your Input**
Gather the information needed for each variable:
- {{variable1}}: [What to prepare]
- {{variable2}}: [What to prepare]

**Step 2: Fill in Variables**
Replace template variables with your specific content:
```
Original: {{variable1}}
Your input: [Your actual content]
```

**Step 3: Review and Adjust**
- Check that all variables are filled
- Adjust requirements if needed
- Add context-specific constraints

**Step 4: Execute**
Submit the completed prompt to the AI model.

**Step 5: Iterate**
Based on results, refine the prompt:
- Add more specific requirements
- Clarify ambiguous instructions
- Include additional examples

  ### 6. Example Implementations

  #### Example 1: Basic Use Case

**Input:**
```
{{variable1}}: [Example input 1]
{{variable2}}: [Example input 2]
```

**Completed Prompt:**
```
[Full prompt with variables filled in]
```

**Expected Output:**
```
[What the AI should produce]
```

---

  #### Example 2: Advanced Use Case

**Input:**
```
{{variable1}}: [Complex input]
{{variable2}}: [Additional context]
```

**Completed Prompt:**
```
[Full prompt with variables filled in]
```

**Expected Output:**
```
[More complex expected output]
```

  ### 7. Variations and Modifications

  #### Variation 1: [Purpose]
**Modification:**
- Change [element] to [new value]
- Add [new requirement]
- Remove [element]

**When to Use:**
- Scenario 1
- Scenario 2

---

  #### Variation 2: [Purpose]
**Modification:**
- Adjust [element]
- Include [addition]

**When to Use:**
- Scenario 1
- Scenario 2

  ### 8. Common Mistakes to Avoid

**Mistake 1: Being Too Vague**
- ❌ Bad: "Analyze this code"
- ✅ Good: "Perform security analysis focusing on [specific aspects]"

**Mistake 2: Missing Context**
- ❌ Bad: Jumping straight to task without background
- ✅ Good: Providing role, objective, and context first

**Mistake 3: Unclear Output Format**
- ❌ Bad: No structure specified
- ✅ Good: Clear sections and formatting requirements

**Mistake 4: Too Many Requirements**
- ❌ Bad: 20+ bullet points of requirements
- ✅ Good: 5-7 key requirements, grouped logically

  ### 9. Optimization Tips

  #### For Better Clarity:
- Use simple, direct language
- Break complex requests into steps
- Provide examples liberally
- Define technical terms

  #### For Better Results:
- Specify desired output format
- Include quality criteria
- Provide success examples
- Set clear boundaries

  #### For Better Reusability:
- Use variables for all changing parts
- Keep structure consistent
- Document edge cases
- Provide usage examples

  ### 10. Testing Your Template

  #### Test Checklist:
- [ ] Template works with minimal input
- [ ] Template works with complex input
- [ ] Edge cases handled appropriately
- [ ] Output format is consistent
- [ ] Instructions are clear
- [ ] Variables are well-defined
- [ ] Examples are helpful

  #### Test Cases:
1. **Simple case**: [Test with basic input]
2. **Complex case**: [Test with detailed input]
3. **Edge case**: [Test with unusual input]
4. **Error case**: [Test with invalid input]

  ### 11. Template Categories

  #### Technical Prompts
- Code generation
- Code review
- Architecture design
- Debugging
- Optimization

  #### Analysis Prompts
- Data analysis
- Performance analysis
- Security analysis
- Trend analysis
- Comparison

  #### Creative Prompts
- Content writing
- Ideation
- Storytelling
- Design concepts
- Marketing copy

  #### Learning Prompts
- Explanations
- Tutorials
- Study guides
- Question generation
- Learning paths

  #### Professional Prompts
- Email drafting
- Report writing
- Documentation
- Presentations
- Summaries

  ### 12. Advanced Template Features

  #### Conditional Logic
```
{{if variable1}}
  Include this section when variable1 is provided
{{endif}}

{{if-else variable2}}
  Use this when variable2 is X
{{else}}
  Use this otherwise
{{endif}}
```

  #### Multi-Step Templates
```
Step 1: [First task]
{{variable1}}

Step 2: Based on Step 1, [second task]
{{variable2}}

Step 3: Combining results, [final task]
```

  #### Iterative Templates
```
For each {{item}} in {{collection}}:
1. Analyze {{item}}
2. Compare with {{criteria}}
3. Output results
```

  ### 13. Documentation Template

For sharing your template with others:

```markdown
# Template Name

## Description
[What this template does]

## When to Use
- Use case 1
- Use case 2

## Variables

### Required
- `{{var1}}`: Description

### Optional
- `{{var2}}`: Description (default: value)

## Template

[The actual prompt template]

## Examples

### Example 1
Input:
```
var1: value
```

Output:
```
[Expected result]
```

## Notes
- Note 1
- Note 2
```

  ### 14. Prompt Template Library Organization

  #### File Structure
```
templates/
├── technical/
│   ├── code-review.md
│   ├── debugging.md
│   └── architecture.md
├── writing/
│   ├── blog-post.md
│   ├── documentation.md
│   └── email.md
└── analysis/
    ├── data-analysis.md
    └── security-audit.md
```

  #### Naming Convention
- Use kebab-case
- Descriptive names
- Include category prefix if needed
- Example: `tech-code-review-security.md`

  ### 15. Quality Checklist for Templates

**Structure:**
- [ ] Clear role/context
- [ ] Explicit objective
- [ ] Well-defined variables
- [ ] Structured output format
- [ ] Examples provided

**Content:**
- [ ] Comprehensive requirements
- [ ] Appropriate constraints
- [ ] Quality guidelines
- [ ] Edge cases covered

**Usability:**
- [ ] Easy to understand
- [ ] Easy to customize
- [ ] Clear instructions
- [ ] Good documentation

**Effectiveness:**
- [ ] Produces consistent results
- [ ] Works across use cases
- [ ] Handles variations well
- [ ] Tested and validated

Generate a complete, reusable prompt template following this structure.
```

---

### improve-prompt

> **Description**: Improve existing prompts.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `prompt-engineering`

#### Template Content:
```markdown
# Improve This Prompt

Analyze and improve the following prompt:

```
{{args}}
```

  ## Evaluation Criteria:

  ### 1. Clarity & Specificity
**Current State:**
- Is the prompt clear and unambiguous?
- Are the instructions specific enough?
- Is there room for misinterpretation?

**Improvements:**
- Make objectives crystal clear
- Add specific requirements
- Remove ambiguity

  ### 2. Structure & Organization
**Current State:**
- Is the prompt well-organized?
- Does it use headers, lists, or sections?
- Is information presented logically?

**Improvements:**
- Add clear structure with headers
- Use numbered steps for processes
- Group related information

  ### 3. Context & Constraints
**Current State:**
- Does it provide enough context?
- Are constraints clearly defined?
- Are assumptions stated?

**Improvements:**
- Add relevant background information
- Specify limitations and boundaries
- State assumptions explicitly

  ### 4. Output Specification
**Current State:**
- Is the desired output format specified?
- Are examples provided?
- Is the level of detail clear?

**
- Make output requirements clear
- Provide examples of expected output format

  ## Example Improvement:
**Original**: "Write a blog post about AI."
**Improved**: "Write a 500-word blog post about the impact of AI on the healthcare industry. Target audience: healthcare professionals. Include 3 real-world examples and conclude with a summary. Tone: professional but accessible."

Provide the improved prompt directly below your analysis.
```

---

### prompt-best-practices

> **Description**: Learn prompt engineering tips.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`, `prompt-engineering`

#### Template Content:
```markdown
# Prompt Engineering Best Practices

Please provide best practices and tips for prompt engineering related to:

{{args}}

  ## Core Prompt Engineering Principles

  ### 1. Clarity and Specificity

  #### Be Explicit
**Bad:**
```
Write code
```

**Good:**
```
Write a Python function that:
- Takes a list of integers as input
- Returns the sum of even numbers
- Handles empty lists
- Includes type hints
- Has docstring documentation
```

**Why:** AI models perform better with clear, specific instructions.

---

  #### Define the Role
**Bad:**
```
Explain databases
```

**Good:**
```
You are a database expert teaching beginners. Explain what databases are using simple language and everyday analogies.
```

**Why:** Role-setting provides context and adjusts the response style.

---

  #### Specify Output Format
**Bad:**
```
Tell me about error handling
```

**Good:**
```
Explain error handling in the following format:
1. Definition (2-3 sentences)
2. Why it matters (1 paragraph)
3. Code example with comments
4. Common mistakes to avoid (3-5 bullet points)
```

**Why:** Structured outputs are more useful and consistent.

---

  ### 2. Context and Background

  #### Provide Sufficient Context
**Bad:**
```
Fix this code: [code snippet]
```

**Good:**
```
Context: I'm building a React application for e-commerce.
Problem: This checkout component crashes when users have empty carts.
Expected: Should display "Cart is empty" message instead.

Code to fix:
[code snippet]
```

**Why:** Context helps the AI understand the problem domain and constraints.

---

  #### Include Constraints
**Bad:**
```
Design a database schema
```

**Good:**
```
Design a database schema for a blog with these constraints:
- Must support PostgreSQL
- Expected 1M users, 10M posts
- Need to query posts by author quickly
- Must support tags (many-to-many)
- Follow 3NF normalization
```

**Why:** Constraints guide the solution toward practical, feasible answers.

---

  ### 3. Examples and Demonstrations

  #### Use Few-Shot Learning
**Pattern:**
```
Here are examples of what I want:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now do the same for:
Input: [your actual input]
```

**Why:** Examples teach the AI the pattern you want.

---

  #### Show Good and Bad Examples
```
Good example:
✅ [Show correct approach]

Bad example:
❌ [Show wrong approach]

Now apply this to: [your case]
```

**Why:** Contrasts clarify expectations.

---

  ### 4. Step-by-Step Decomposition

  #### Break Complex Tasks
**Bad:**
```
Build a full authentication system
```

**Good:**
```
Let's build an authentication system step by step:

Step 1: Design the user schema
- What fields do we need?
- What constraints?

Step 2: Implement registration
- Input validation
- Password hashing
- Database storage

Step 3: Implement login
- Credential verification
- JWT generation
- Error handling

Let's start with Step 1.
```

**Why:** Complex tasks are easier to handle in pieces.

---

  #### Chain of Thought
```
Think through this problem step by step:

1. First, identify the inputs and outputs
2. Then, consider edge cases
3. Next, outline the algorithm
4. Finally, write the code

Show your reasoning for each step.
```

**Why:** Encourages logical, thorough responses.

---

  ### 5. Output Quality Control

  #### Request Self-Critique
```
[Your prompt]

After providing your answer, critique it by identifying:
1. Potential issues or edge cases missed
2. Alternative approaches
3. Improvements that could be made
```

**Why:** Prompts self-reflection leading to better answers.

---

  #### Ask for Multiple Options
```
Provide 3 different approaches to solve this problem:
1. Approach A: [optimized for performance]
2. Approach B: [optimized for readability]
3. Approach C: [optimized for maintainability]

For each, explain pros and cons.
```

**Why:** Comparison helps you choose the best solution.

---

  ### 6. Constraints and Boundaries

  #### Set Scope Limits
```
Limit your response to:
- Maximum 200 lines of code
- Only use standard library (no external dependencies)
- Must work in Python 3.8+
- Response should be under 500 words
```

**Why:** Prevents overly complex or lengthy responses.

---

  #### Specify What to Avoid
```
Requirements:
- Do NOT use deprecated APIs
- Do NOT include comments explaining every line
- Do NOT make assumptions about user input
- Do NOT use global variables
```

**Why:** Explicitly ruling out unwanted approaches.

---

  ### 7. Iterative Refinement

  #### Version 1: Basic Prompt
```
Explain async/await in JavaScript
```

**Response:** Too basic or too complex

---

  #### Version 2: Add Context
```
Explain async/await in JavaScript to an intermediate developer who understands callbacks and promises.
```

**Response:** Better but still generic

---

  #### Version 3: Add Structure
```
Explain async/await in JavaScript to an intermediate developer:

1. Quick definition (2-3 sentences)
2. How it relates to promises
3. Code example showing conversion from promises to async/await
4. Common pitfalls
5. When to use vs when not to use
```

**Response:** Much more targeted and useful

---

  ### 8. Prompt Patterns

  #### The Template Pattern
```
You are a [role].
Your task is to [objective].

Given:
{{input}}

Requirements:
- [requirement 1]
- [requirement 2]

Output format:
[specify structure]
```

---

  #### The Persona Pattern
```
Act as a [expert type] with [years] of experience in [domain].
You are known for [characteristics].
Your communication style is [style].

[Rest of prompt]
```

---

  #### The Refinement Pattern
```
[Initial prompt]

Please refine your answer by:
1. Adding more specific examples
2. Addressing edge case X
3. Explaining assumption Y
```

---

  #### The Comparison Pattern
```
Compare and contrast [A] vs [B] in the following dimensions:
- Performance
- Ease of use
- Scalability
- Cost
- Maintenance

Provide specific examples for each dimension.
```

---

  #### The Constraint Pattern
```
Given these constraints:
- Constraint 1
- Constraint 2
- Constraint 3

[Task description]

If any constraint cannot be satisfied, explain why and suggest alternatives.
```

---

  ### 9. Common Prompt Mistakes

  #### Mistake 1: Too Vague
❌ "Make it better"
✅ "Improve performance by reducing time complexity from O(n²) to O(n log n)"

  #### Mistake 2: Assuming Context
❌ "Add validation to the form"
✅ "Add email validation to the registration form, checking for: valid format, not already registered, and not from blacklisted domains"

  #### Mistake 3: Multiple Unrelated Tasks
❌ "Build a login system, write tests, create documentation, and deploy it"
✅ "First, let's build the login system. We'll handle tests, docs, and deployment in separate steps."

  #### Mistake 4: No Success Criteria
❌ "Optimize this function"
✅ "Optimize this function to run in under 100ms for inputs up to 10,000 elements"

  #### Mistake 5: Ambiguous Pronouns
❌ "It should connect to it using that"
✅ "The client should connect to the database using connection pooling"

---

  ### 10. Domain-Specific Best Practices

  #### For Code Generation
```
Generate [language] code that:
- Function/class name and purpose
- Input parameters with types
- Return type
- Error handling approach
- Edge cases to handle
- Performance requirements
- Code style preferences
```

  #### For Code Review
```
Review this [language] code for:
1. Security vulnerabilities
2. Performance issues
3. Code quality and maintainability
4. Best practices violations
5. Edge cases not handled

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Explanation
- Fix recommendation
- Example of corrected code
```

  #### For Explanations
```
Explain [concept] with:
1. Simple analogy (ELI5 level)
2. Technical definition
3. Real-world use case
4. Code example
5. Common misconceptions
6. Related concepts

Assume audience: [skill level]
```

  #### For Documentation
```
Create documentation for [code/feature] including:
- Overview (what it does, why it exists)
- Prerequisites
- Installation/setup steps
- Usage examples (basic and advanced)
- API reference
- Common issues and solutions
- Best practices
```

---

  ### 11. Testing Your Prompts

  #### Quality Checklist
- [ ] Is the objective clear?
- [ ] Is the role/context defined?
- [ ] Are constraints specified?
- [ ] Is output format defined?
- [ ] Are examples provided?
- [ ] Are edge cases mentioned?
- [ ] Is success criteria clear?

  #### Test Cases
1. **Minimal input**: Does it work with bare minimum?
2. **Complex input**: Does it handle complexity?
3. **Edge cases**: Does it handle unusual inputs?
4. **Ambiguity**: Could it be misinterpreted?

---

  ### 12. Advanced Techniques

  #### Meta-Prompting
```
Before answering, ask yourself:
- What information is missing?
- What assumptions am I making?
- What edge cases exist?

Then provide your answer addressing these points.
```

  #### Prompt Chaining
```
Prompt 1: Analyze the requirements
Prompt 2: Based on the analysis, design the solution
Prompt 3: Based on the design, implement the code
Prompt 4: Based on the code, write tests
```

  #### Self-Consistency
```
Solve this problem 3 different ways, then:
1. Compare the solutions
2. Identify the best approach
3. Explain why it's best
```

---

  ### 13. Optimization Tips

  #### For Conciseness
- Use bullet points instead of paragraphs for requirements
- Reference examples instead of repeating them
- Use abbreviations consistently (define once)

  #### For Accuracy
- Specify versions (Python 3.10, React 18)
- Include units (milliseconds, MB, percentage)
- Define technical terms
- Provide examples of correct output

  #### For Consistency
- Use templates for similar tasks
- Maintain same structure across prompts
- Define terms consistently
- Use same variable naming

---

  ### 14. Prompt Engineering Workflow

1. **Define Goal**: What do you want to achieve?
2. **Draft Initial Prompt**: Write first version
3. **Test**: Try it out
4. **Analyze Results**: What's good? What's missing?
5. **Refine**: Add specificity, examples, constraints
6. **Re-test**: Try refined version
7. **Iterate**: Repeat until satisfactory
8. **Document**: Save successful prompts for reuse

---

  ### 15. Resources and Further Learning

  #### Key Principles to Remember
1. **Clarity over brevity**: Be detailed, not terse
2. **Show, don't just tell**: Use examples
3. **Structure matters**: Format output explicitly
4. **Context is king**: Provide background
5. **Iterate and refine**: First drafts rarely perfect
6. **Test edge cases**: Think about what could go wrong
7. **Be specific**: Vague prompts = vague answers
8. **Set boundaries**: Define what you don't want

Generate comprehensive prompt engineering guidance following these best practices.
```

---

### prompt-versioning

> **Description**: Guide for managing and versioning prompt templates.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `learning`, `prompt-engineering`

#### Template Content:
```markdown
# Prompt Versioning & Lifecycle Management

Please provide a comprehensive guide and strategy for versioning and managing the lifecycle of the following prompt template or set of prompts:

```
{{args}}
```

Provide your response in the following structured format:

  ## 1. Prompt Semantic Versioning (PSemVer)
Explain how to apply Semantic Versioning to this prompt:
- **Major (X.0.0)**: When to increment (e.g., changing the core task, switching models, or altering mandatory output structure).
- **Minor (0.X.0)**: When to increment (e.g., adding new optional instructions, significantly refining existing guidance, or adding new variables).
- **Patch (0.0.X)**: When to increment (e.g., fixing typos, minor wording tweaks that don't change intent, or formatting updates).

  ## 2. Change Tracking & Documentation
- Suggest a format for an internal `CHANGELOG` within the prompt file or a separate repository.
- How to document the "Why" behind a prompt update (e.g., "Improved response length", "Fixed hallucinations in edge cases").

  ## 3. Testing & Validation Strategy
- **Golden Sets**: How to maintain a set of "ideal" inputs and outputs to test new prompt versions against.
- **A/B Testing**: How to run parallel tests between two prompt versions to measure performance improvements.
- **Regression Testing**: Ensuring a new version doesn't break previously working cases.

  ## 4. Environment & Deployment States
Suggest how to manage prompt states across different environments:
- **Draft**: Initial creation and internal testing.
- **Staging**: Testing with real-world data in a safe environment.
- **Production**: The current "live" version.
- **Deprecated**: Older versions that are no longer recommended but might still be in use.

  ## 5. Automation & Tooling
Suggest tools or scripts to automate:
- Version tagging in Git.
- Automated testing of prompts using LLM-as-a-judge.
- Deployment of updated prompts to production APIs.

Provide a clear, actionable roadmap for implementing this versioning strategy.
```

---

## <a name='security'></a> Security

### accessibility-audit

> **Description**: Review HTML/React code for WCAG compliance.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `frontend`, `security`

#### Template Content:
```markdown
# Frontend Accessibility (a11y) Audit

Please analyze the following HTML, React, or Vue component for Web Content Accessibility Guidelines (WCAG) compliance:

```
{{args}}
```

Focus your audit on the following areas:

  ## 1. Semantic HTML
- Are the correct semantic tags used (e.g., `<button>` vs `<div>` for clickable elements, `<nav>`, `<main>`)?
- Are heading levels (`h1`-`h6`) structured logically without skipping levels?

  ## 2. Keyboard Navigation
- Can all interactive elements be reached using the `Tab` key?
- Is there a visible focus indicator (`:focus` or `:focus-visible`)?
- Are `tabindex` attributes used correctly (avoiding positive values)?

  ## 3. Screen Reader Support (ARIA)
- Do images have descriptive `alt` text (or empty `alt=""` for decorative images)?
- Are ARIA roles, states, and properties applied correctly to custom UI components (like modals, dropdowns, or tabs)?
- Are form inputs explicitly associated with `<label>` elements?

  ## 4. Contrast & Visuals
- Are you able to identify any obvious color contrast issues based on the provided classes or styles?

For every issue found, provide a description of why it's an accessibility barrier and supply the corrected code block.
```

---

### code-review-security

> **Description**: Deep security analysis of code.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `code-review`, `security`

#### Template Content:
```markdown
# Security Code Review

Please perform a comprehensive security analysis of the following code:

```
{{args}}
```

Focus on:

  ## 1. Input Validation & Sanitization
- Are all user inputs properly validated?
- Is input sanitized before use in queries, commands, or rendering?
- Are there risks of injection attacks (SQL, XSS, command injection)?

  ## 2. Authentication & Authorization
- Are authentication mechanisms secure?
- Is authorization properly enforced?
- Are credentials handled securely?
- Is session management secure?

  ## 3. Data Protection
- Is sensitive data encrypted at rest and in transit?
- Are secrets and API keys properly managed?
- Is PII (Personally Identifiable Information) handled correctly?

  ## 4. Common Vulnerabilities
- Check for OWASP Top 10 vulnerabilities
- Look for race conditions and TOCTOU issues
- Identify potential buffer overflows or memory issues
- Check for insecure dependencies

  ## 5. Error Handling & Logging
- Are errors handled without exposing sensitive information?
- Is logging done securely without leaking secrets?
- Are stack traces exposed in production?

  ## 6. Access Control
- Are file permissions appropriate?
- Is path traversal prevented?
- Are resources properly scoped and isolated?

Provide:
1. **Critical Issues**: Vulnerabilities that must be fixed immediately
2. **High Priority**: Significant security concerns
3. **Medium Priority**: Security improvements
4. **Best Practices**: General security recommendations
5. **Code Examples**: Show secure alternatives for each issue

For each issue, explain:
- What the vulnerability is
- Why it's dangerous
- How to fix it
- Example of secure code
```

---

### dependency-audit

> **Description**: Analyze a package.json or requirements.txt for known vulnerable patterns.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `security`

#### Template Content:
```markdown
# Dependency Security Audit

Please analyze the following dependency manifest (e.g., `package.json`, `requirements.txt`, `Gemfile`, or `Cargo.toml`) for security risks, vulnerable patterns, and maintenance issues:

```
{{args}}
```

Provide your analysis in the following format:

  ## 1. Known Vulnerable Packages
Identify any dependencies that are historically known to have major CVEs or frequent security issues in the specified versions. 

  ## 2. Unmaintained or Deprecated Packages
Flag any packages that are officially deprecated, renamed, or haven't seen updates in years. Suggest modern alternatives.

  ## 3. Typo-Squatting & Malicious Risks
Check for packages with unusual names, extremely broad scopes, or common typo-squatting targets.

  ## 4. Supply Chain Best Practices
Recommend improvements such as:
- Pinning versions strictly.
- Using lockfiles (`package-lock.json`, `poetry.lock`).
- Implementing automated auditing (e.g., Dependabot, Snyk).
- Removing unnecessary runtime dependencies (moving them to `devDependencies`).
```

---

### iam-policy

> **Description**: Generate AWS IAM or GCP resource policies with least privilege.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `security`, `infra`

#### Template Content:
```markdown
# IAM Policy Generator

Please generate a secure, least-privilege Identity and Access Management (IAM) policy (AWS JSON or GCP YAML/JSON) for the following use case:

```
{{args}}
```

Ensure the generated policy adheres to these best practices:

  ## 1. Principle of Least Privilege
- Only grant the exact actions required to perform the stated task.
- Avoid using wildcards (`*`) for actions unless absolutely necessary.

  ## 2. Resource Scoping
- Restrict the policy to specific resources (e.g., a specific S3 bucket ARN, a specific DynamoDB table) rather than `Resource: "*"`.

  ## 3. Condition Keys (If Applicable)
- Use condition blocks to further restrict access (e.g., `aws:SourceIp`, `aws:MultiFactorAuthPresent`, or `aws:PrincipalTag`).

Provide the complete JSON/YAML policy along with a brief explanation of the permissions granted and the security considerations taken.
```

---

### security-policy

> **Description**: Draft a SECURITY.md or vulnerability disclosure policy.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `docs`, `security`

#### Template Content:
```markdown
# Security Policy Generator

Please generate a professional, standard `SECURITY.md` file (Vulnerability Disclosure Policy) for the following project/organization:

```
{{args}}
```

Ensure the policy includes:

  ## 1. Supported Versions
A clear table indicating which versions of the project are currently supported with security updates.

  ## 2. Reporting a Vulnerability
- Step-by-step instructions on how a security researcher should privately report a vulnerability (e.g., specific email address, PGP key, or HackerOne link).
- Explicitly state *not* to open a public GitHub issue.

  ## 3. Response Process
- A timeline/SLA for when the researcher can expect an initial response, triage, and resolution.
- Expectations regarding embargo periods before public disclosure.

  ## 4. Out of Scope
- A clear list of attack types or issues that are considered out-of-scope for the vulnerability program (e.g., volumetric DDoS, social engineering, physical attacks).
```

---

### threat-modeling

> **Description**: Generate a STRIDE threat model for a proposed architecture.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `architecture`, `security`

#### Template Content:
```markdown
# Threat Modeling (STRIDE)

Please generate a comprehensive threat model using the STRIDE methodology for the following proposed architecture/system:

```
{{args}}
```

Provide your analysis in the following structured format:

  ## 1. System Overview
Provide a brief summary of the system components and data flow based on the provided description.

  ## 2. STRIDE Analysis
Analyze the system across the 6 STRIDE categories. For each category, identify at least 2 potential threats.
- **Spoofing (Authenticity):** Can an attacker impersonate a user or service?
- **Tampering (Integrity):** Can data be modified in transit or at rest?
- **Repudiation (Non-repudiability):** Can a user perform an action without a trace?
- **Information Disclosure (Confidentiality):** Can sensitive data be exposed?
- **Denial of Service (Availability):** Can the system be brought down or degraded?
- **Elevation of Privilege (Authorization):** Can an unprivileged user gain admin access?

  ## 3. Risk Assessment & Mitigations
For each identified threat, provide:
1. **Risk Level:** (Critical, High, Medium, Low)
2. **Mitigation Strategy:** Concrete technical or architectural steps to resolve or mitigate the threat.

  ## 4. Key Security Recommendations
Summarize the top 3-5 security priorities the development team must focus on before releasing this system.
```

---

## <a name='shell'></a> Shell

### bash-script-generator

> **Description**: Write robust, POSIX-compliant bash scripts.
> **Input Format**: `Task to Script`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `devops`, `shell`

#### Template Content:
```markdown
# Robust Bash Script Generator

Please write a robust, production-ready bash script to accomplish the following task:

```
{{args}}
```

Ensure the script adheres to the following Bash best practices:

  ## 1. Safety & Error Handling
- Start the script with `set -euo pipefail` to ensure it fails fast on errors, undefined variables, and pipe failures.
- Use `trap` for cleanup of temporary files or locks upon script exit or interruption.

  ## 2. Logging & Output
- Implement simple logging functions (e.g., `log_info`, `log_error`, `log_warn`) to standard error (`>&2`) where appropriate, so `stdout` remains clean for piping.
- Include timestamps in the log output.

  ## 3. Argument Parsing & Help
- Implement a `usage()` or `help()` function that explains how to run the script and what arguments it accepts.
- Use a `while/case` loop with `shift` or `getopts` to parse command-line flags securely.

  ## 4. Syntax & Style
- Prefer `[[ ]]` over `[ ]` for test conditions.
- Prefer `"$()"` over backticks `` ` ` `` for command substitution.
- Quote all variables properly (e.g., `"$VAR"`) to prevent word splitting and globbing issues.
- Use `local` variables inside functions to prevent polluting the global scope.

  ## 5. Idempotency & Checks
- Where applicable, check if required commands exist before using them (e.g., using `command -v`).
- Ensure operations are idempotent (e.g., using `mkdir -p` instead of just `mkdir`).

For your response, provide:
1. **The complete, commented bash script.**
2. **A brief explanation** of how to run it, including examples of the flags or arguments.
```

---

### cli-command-explainer

> **Description**: Deeply explain obscure terminal commands/flags.
> **Input Format**: `Technical Concept`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `shell`

#### Template Content:
```markdown
# CLI Command Explainer

Please provide a deep, easy-to-understand explanation of the following terminal command, pipeline, or script:

```
{{args}}
```

Provide your analysis in the following format:

  ## 1. High-Level Summary
What does this entire command achieve in one simple sentence?

  ## 2. Step-by-Step Breakdown
Break down every single component, utility, and pipe `|`:
- Explain the base command.
- Explain what every flag/argument means (e.g., what does the `-p` or `-aux` actually stand for?).
- Explain how data is flowing between piped commands.

  ## 3. Safety Warning
- Is this command destructive? (e.g., Does it delete files, overwrite data, or alter system state?)
- Are there any dangerous assumptions it makes?

  ## 4. Modern Alternatives
If this is an archaic or complex command, is there a simpler, modern alternative (e.g., using `fd` instead of `find`, or `rg` instead of `grep`)?
```

---

### git-workflow

> **Description**: Suggest Git commands to recover from complex merge/rebase states.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `shell`

#### Template Content:
```markdown
# Git Workflow & Recovery Assistant

Please analyze the following Git scenario, error message, or desired workflow state, and provide the exact Git commands to resolve or achieve it safely:

```
{{args}}
```

Provide your response in the following format:

  ## 1. Situation Diagnosis
Explain what is currently happening in the Git tree (e.g., detached HEAD, merge conflict, interactive rebase paused).

  ## 2. Solution Steps
Provide the exact, step-by-step Git commands to resolve the issue. Explain what each command does.

  ## 3. Verification
How can the user verify that the fix worked? (e.g., `git status`, `git log --graph`).

  ## 4. The "Undo" Button
If the user makes a mistake applying your solution, provide the command to safely abort and return to the original state (e.g., `git rebase --abort`, `git reflog`).
```

---

### regex-builder

> **Description**: Generate and explain complex Regular Expressions.
> **Input Format**: `Technical Concept`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `shell`, `db`

#### Template Content:
```markdown
# Regex Builder & Explainer

Please analyze the following text-matching requirement and generate an optimized Regular Expression:

```
{{args}}
```

Provide your response in the following format:

  ## 1. The Regular Expression
Provide the raw regex pattern. If it requires specific flags (like `g`, `i`, `m`), specify them.

  ## 2. Step-by-Step Breakdown
Explain exactly how the regex works, breaking down every token, group, and quantifier.

  ## 3. Test Cases
Provide examples of strings that this regex will successfully **Match**.
Provide examples of similar strings that this regex will correctly **Fail to match** (edge cases).

  ## 4. Performance & ReDoS Warning
- Is this regex susceptible to Catastrophic Backtracking (ReDoS)? 
- Are there any inefficient greedy quantifiers (`.*`) that could be optimized?
```

---

## <a name='test'></a> Test

### generate-e2e-tests

> **Description**: Create end-to-end tests.
> **Input Format**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `test`

#### Template Content:
```markdown
# Generate End-to-End Tests

Please create comprehensive end-to-end tests for the following application/feature:

{{args}}

  ## Test Framework Considerations

Choose appropriate E2E testing framework:
- Web: Playwright, Cypress, Selenium
- Mobile: Appium, Detox
- API: Supertest, REST Assured
- Desktop: TestComplete, WinAppDriver

  ## E2E Test Structure

  ### 1. User Journey Tests

Test complete user workflows from start to finish:
```javascript
test('User can complete signup and login flow', async ({ page }) => {
  // Navigate to signup
  await page.goto('/signup');

  // Fill signup form
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'SecurePass123');
  await page.click('button[type="submit"]');

  // Verify redirect to dashboard
  await expect(page).toHaveURL('/dashboard');

  // Verify welcome message
  await expect(page.locator('.welcome')).toContainText('Welcome');
});
```

  ### 2. Test Categories

  #### Critical User Paths
- User registration and authentication
- Core business workflows
- Payment/checkout processes
- Data submission and retrieval

  #### Cross-Browser/Platform
- Test on major browsers (Chrome, Firefox, Safari, Edge)
- Test on different devices (desktop, tablet, mobile)
- Test on different OS (Windows, macOS, Linux)

  #### Integration Points
- Third-party service integrations
- API interactions
- Database operations
- External system communications

  ### 3. Test Patterns

  #### Page Object Model
```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[name="email"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

  #### Setup and Teardown
```javascript
test.beforeEach(async ({ page }) => {
  // Clear cookies and local storage
  await page.context().clearCookies();
  await page.evaluate(() => localStorage.clear());

  // Navigate to starting point
  await page.goto('/');
});

test.afterEach(async ({ page }, testInfo) => {
  // Screenshot on failure
  if (testInfo.status !== 'passed') {
    await page.screenshot({
      path: `test-results/${testInfo.title}-failure.png`
    });
  }
});
```

  ### 4. Test Scenarios to Cover

  #### Authentication & Authorization
- User registration with valid/invalid data
- Login with correct/incorrect credentials
- Logout functionality
- Password reset flow
- Session management
- Access control (authorized vs unauthorized users)

  #### CRUD Operations
- Create new records
- Read/view records
- Update existing records
- Delete records
- List/search records
- Pagination

  #### Forms & Validation
- Submit valid forms
- Submit invalid forms
- Field validation messages
- Required field enforcement
- Format validation (email, phone, etc.)
- File uploads

  #### Navigation
- Menu navigation
- Breadcrumb navigation
- Back/forward browser buttons
- Deep linking
- Redirects

  #### Search & Filters
- Search with various queries
- Apply filters
- Sort results
- Pagination of results
- Empty results handling

  #### Error Handling
- Network errors
- Server errors (500, 503)
- Not found (404)
- Validation errors
- Timeout scenarios

  ### 5. Waiting Strategies

```javascript
// Wait for element
await page.waitForSelector('.data-loaded');

// Wait for navigation
await page.waitForNavigation();

// Wait for API response
await page.waitForResponse(response =>
  response.url().includes('/api/data')
);

// Wait for condition
await page.waitForFunction(() =>
  document.querySelector('.loading') === null
);

// Custom timeout
await page.waitForSelector('.slow-element', { timeout: 10000 });
```

  ### 6. Data Management

  #### Test Data Setup
```javascript
test.beforeEach(async ({ request }) => {
  // Create test user via API
  await request.post('/api/users', {
    data: {
      email: 'test@example.com',
      name: 'Test User'
    }
  });
});
```

  #### Test Data Cleanup
```javascript
test.afterEach(async ({ request }) => {
  // Delete test data
  await request.delete('/api/users/test@example.com');
});
```

  ### 7. Assertions

```javascript
// Element visibility
await expect(page.locator('.success-message')).toBeVisible();

// Text content
await expect(page.locator('h1')).toHaveText('Dashboard');

// URL
await expect(page).toHaveURL('/dashboard');

// Element count
await expect(page.locator('.item')).toHaveCount(5);

// Attribute
await expect(page.locator('button')).toHaveAttribute('disabled');

// Screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');
```

  ### 8. API Testing in E2E

```javascript
test('should create user via API and verify in UI', async ({ request, page }) => {
  // Create via API
  const response = await request.post('/api/users', {
    data: { name: 'John Doe', email: 'john@example.com' }
  });
  expect(response.ok()).toBeTruthy();

  const user = await response.json();

  // Verify in UI
  await page.goto(`/users/${user.id}`);
  await expect(page.locator('.user-name')).toHaveText('John Doe');
});
```

  ### 9. Mobile/Responsive Testing

```javascript
test('should work on mobile', async ({ page }) => {
  // Set viewport to mobile
  await page.setViewportSize({ width: 375, height: 667 });

  await page.goto('/');

  // Open mobile menu
  await page.click('.mobile-menu-toggle');
  await expect(page.locator('.mobile-menu')).toBeVisible();
});
```

  ### 10. Performance Checks

```javascript
test('page should load within 3 seconds', async ({ page }) => {
  const start = Date.now();
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  const loadTime = Date.now() - start;

  expect(loadTime).toBeLessThan(3000);
});
```

  ## Best Practices

1. **Stability**: Use reliable selectors (data-testid preferred)
2. **Independence**: Tests should not depend on each other
3. **Cleanup**: Always clean up test data
4. **Waits**: Use explicit waits, avoid arbitrary sleeps
5. **Retries**: Configure retries for flaky tests
6. **Parallelization**: Run tests in parallel when possible
7. **Screenshots**: Capture screenshots on failure
8. **Videos**: Record videos for debugging
9. **Logs**: Capture console logs
10. **Reports**: Generate comprehensive test reports

  ## Output Format

Provide:
1. Complete E2E test suite
2. Page Object Models (if applicable)
3. Setup and teardown code
4. Test data factories/fixtures
5. Configuration suggestions
6. Clear test descriptions
7. Comments for complex interactions

Generate a complete, production-ready E2E test suite following these best practices.
```

---

### generate-unit-tests

> **Description**: Create unit tests for code.
> **Input Format**: `Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `test`

#### Template Content:
```markdown
# Generate Unit Tests

Please create comprehensive unit tests for the following code:

{{args}}

  ## Test Framework Considerations

Adapt to the appropriate testing framework:
- JavaScript/TypeScript: Jest, Vitest, Mocha
- Python: pytest, unittest
- Java: JUnit
- C#: xUnit, NUnit
- Go: testing package
- Ruby: RSpec
- PHP: PHPUnit

  ## Test Structure

  ### 1. Test Organization

```
describe('FunctionName' or 'ClassName', () => {
  describe('methodName', () => {
    it('should handle normal case', () => {});
    it('should handle edge case', () => {});
    it('should throw error for invalid input', () => {});
  });
});
```

  ### 2. Test Coverage Areas

  #### Happy Path Tests
Test normal, expected behavior:
- Valid inputs with expected outputs
- Common use cases
- Typical workflows

  #### Edge Cases
Test boundary conditions:
- Empty inputs (null, undefined, empty string, empty array)
- Zero values
- Negative numbers
- Very large numbers
- Maximum/minimum values
- Single element collections

  #### Error Cases
Test error handling:
- Invalid inputs
- Type mismatches
- Out of range values
- Missing required parameters
- Malformed data

  #### Boundary Conditions
- First and last elements
- Off-by-one scenarios
- Limits and thresholds

  ### 3. Test Patterns

  #### Arrange-Act-Assert (AAA)
```javascript
it('should calculate total with discount', () => {
  // Arrange
  const price = 100;
  const discount = 0.2;

  // Act
  const result = calculateTotal(price, discount);

  // Assert
  expect(result).toBe(80);
});
```

  #### Given-When-Then (BDD style)
```javascript
it('should calculate total with discount', () => {
  // Given
  const price = 100;
  const discount = 0.2;

  // When
  const result = calculateTotal(price, discount);

  // Then
  expect(result).toBe(80);
});
```

  ### 4. Test Types to Include

  #### Basic Functionality Tests
```javascript
it('should return correct value for valid input', () => {
  expect(add(2, 3)).toBe(5);
});
```

  #### Parameterized Tests
```javascript
it.each([
  [2, 3, 5],
  [0, 0, 0],
  [-1, 1, 0],
  [100, 200, 300]
])('should add %i and %i to equal %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

  #### Async Tests
```javascript
it('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});
```

  #### Mock/Stub Tests
```javascript
it('should call API with correct parameters', () => {
  const mockApi = jest.fn();
  service.setApi(mockApi);
  service.fetchData(123);
  expect(mockApi).toHaveBeenCalledWith(123);
});
```

  #### State Tests
```javascript
it('should update state correctly', () => {
  const obj = new MyClass();
  obj.setValue(10);
  expect(obj.getValue()).toBe(10);
});
```

  ### 5. Setup and Teardown

```javascript
describe('Database operations', () => {
  beforeAll(() => {
    // Setup before all tests
  });

  beforeEach(() => {
    // Setup before each test
  });

  afterEach(() => {
    // Cleanup after each test
  });

  afterAll(() => {
    // Cleanup after all tests
  });
});
```

  ### 6. Test Naming

Use descriptive names that explain:
- What is being tested
- Under what conditions
- What the expected result is

**Good names**:
- `should return empty array when no items match filter`
- `should throw error when input is negative`
- `should call callback with correct parameters`

**Bad names**:
- `test1`
- `it works`
- `should work correctly`

  ## Test Quality Guidelines

1. **Independence**: Tests should not depend on each other
2. **Repeatability**: Tests should produce same results every time
3. **Fast**: Unit tests should run quickly
4. **Isolated**: Use mocks/stubs for external dependencies
5. **Clear**: Test intent should be obvious
6. **Comprehensive**: Cover all code paths
7. **Maintainable**: Easy to update when code changes

  ## Coverage Goals

Aim to test:
- All public methods/functions
- All branches (if/else)
- All error paths
- All edge cases
- All important combinations

  ## Output Format

Provide:
1. Complete test suite with all necessary imports
2. Setup/teardown if needed
3. Mock configurations
4. Clear test descriptions
5. Comments explaining complex test scenarios
6. Assertion explanations where helpful

Generate a complete, production-ready test suite following these best practices.
```

---

### review-test-coverage

> **Description**: Analyze test coverage gaps.
> **Input Format**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `test`

#### Template Content:
```markdown
# Test Coverage Analysis

Please analyze test coverage for the following code and identify gaps:

{{args}}

  ## Analysis Areas

  ### 1. Code Coverage Metrics

  #### Line Coverage
- Percentage of lines executed
- Uncovered lines identification
- Critical uncovered lines

  #### Branch Coverage
- Percentage of branches tested
- Uncovered if/else branches
- Uncovered switch cases
- Uncovered ternary operators
- Short-circuit evaluations

  #### Function Coverage
- Percentage of functions tested
- Untested functions
- Partially tested functions

  #### Statement Coverage
- Individual statement execution
- Dead code identification

  ### 2. Coverage by Category

  #### Happy Path Coverage
✓ **Covered:**
- Normal operation scenarios
- Expected inputs
- Standard workflows

✗ **Missing:**
- Additional common use cases
- Variations in normal flow

  #### Error Path Coverage
✓ **Covered:**
- Handled exceptions
- Validation errors

✗ **Missing:**
- Unhandled exceptions
- Edge case errors
- System errors
- Network failures

  #### Edge Case Coverage
✓ **Covered:**
- Empty inputs
- Null/undefined
- Basic boundaries

✗ **Missing:**
- Extreme values
- Resource limits
- Concurrent access
- State combinations

  ### 3. Detailed Gap Analysis

For each uncovered area, provide:

  #### Gap Description
What functionality is not tested

  #### Risk Level
- **Critical**: Could cause data loss, security issues, or system failure
- **High**: Could cause incorrect behavior or crashes
- **Medium**: Could cause user-facing issues
- **Low**: Minor issues or unlikely scenarios

  #### Impact Assessment
What could go wrong if this remains untested

  #### Test Recommendation
Specific tests that should be added

  ### 4. Coverage Report Structure

```markdown
## Current Coverage Summary

| Metric | Percentage | Status |
|--------|------------|--------|
| Lines | 75% | 🟡 Fair |
| Branches | 60% | 🔴 Poor |
| Functions | 85% | 🟢 Good |
| Statements | 73% | 🟡 Fair |

### Coverage Goals
- Lines: 80%+ (current: 75%)
- Branches: 75%+ (current: 60%)
- Functions: 90%+ (current: 85%)
- Statements: 80%+ (current: 73%)

## Detailed Gap Analysis

### 1. Uncovered Functions (15%)

#### `handleError(error)` - Lines 45-60
**Risk**: High
**Issue**: Error handling logic is completely untested
**Tests Needed**:
- Test with different error types
- Test error logging
- Test error recovery
- Test error propagation

#### `parseDate(dateString)` - Lines 120-135
**Risk**: Medium
**Issue**: Date parsing edge cases not tested
**Tests Needed**:
- Invalid date formats
- Null/undefined inputs
- Future dates
- Leap year dates

### 2. Uncovered Branches (40%)

#### File: `user.js`, Lines 78-82
```javascript
if (user.age > 18) {
  // ✓ Tested
} else {
  // ✗ Not tested
}
```
**Risk**: Medium
**Tests Needed**: Add test for users under 18

#### File: `payment.js`, Lines 145-152
```javascript
switch (paymentMethod) {
  case 'credit': // ✓ Tested
    break;
  case 'debit': // ✗ Not tested
    break;
  case 'paypal': // ✗ Not tested
    break;
  default: // ✗ Not tested
}
```
**Risk**: Critical
**Tests Needed**: Test all payment methods

### 3. Untested Edge Cases

#### Empty Array Handling
**Location**: Lines 200-210
**Risk**: Medium
**Current**: Only non-empty arrays tested
**Add**: Tests for empty arrays

#### Null/Undefined Inputs
**Location**: Throughout
**Risk**: High
**Current**: Assumes valid inputs
**Add**: Null safety tests for all public functions

### 4. Missing Integration Tests

#### Database Operations
**Coverage**: 0%
**Risk**: High
**Needed**:
- Connection failure handling
- Transaction rollback
- Query timeout
- Concurrent access

#### API Integrations
**Coverage**: 30%
**Risk**: High
**Needed**:
- Error response handling
- Timeout scenarios
- Rate limiting
- Retry logic

### 5. Missing Scenario Tests

#### Concurrent Operations
**Coverage**: 0%
**Risk**: Critical
**Needed**: Race condition tests

#### Resource Exhaustion
**Coverage**: 0%
**Risk**: High
**Needed**: Memory/connection limit tests

#### State Transitions
**Coverage**: 40%
**Risk**: Medium
**Needed**: Invalid state transition tests

## Recommendations

### Priority 1 (Critical) - Implement Immediately
1. Test error handling in `handleError()` function
2. Test all payment method branches
3. Add concurrent operation tests
4. Test database failure scenarios

### Priority 2 (High) - Implement This Sprint
1. Test `parseDate()` edge cases
2. Add null/undefined checks for all public APIs
3. Test API integration error paths
4. Add resource exhaustion tests

### Priority 3 (Medium) - Next Sprint
1. Test else branches in user age validation
2. Test empty array handling
3. Test state transition edge cases
4. Improve boundary value testing

### Priority 4 (Low) - Backlog
1. Test default cases in switches
2. Add performance benchmarks
3. Test obscure edge cases

## Test Code Examples

### Example 1: Error Handling Test
```javascript
describe('handleError', () => {
  it('should log error with correct severity', () => {
    const error = new Error('Test error');
    handleError(error);
    expect(logger.error).toHaveBeenCalledWith(error);
  });

  it('should handle null error gracefully', () => {
    expect(() => handleError(null)).not.toThrow();
  });
});
```

### Example 2: Branch Coverage Test
```javascript
describe('payment processing', () => {
  it('should handle debit card payment', () => {
    const result = processPayment('debit', 100);
    expect(result.method).toBe('debit');
  });

  it('should handle paypal payment', () => {
    const result = processPayment('paypal', 100);
    expect(result.method).toBe('paypal');
  });

  it('should reject invalid payment method', () => {
    expect(() => processPayment('invalid', 100)).toThrow();
  });
});
```

## Coverage Improvement Plan

### Phase 1 (Week 1)
- Add critical missing tests
- Bring branch coverage to 70%
- Test all error paths

### Phase 2 (Week 2)
- Add high-priority tests
- Bring line coverage to 80%
- Add integration tests

### Phase 3 (Week 3)
- Add medium-priority tests
- Achieve 85% total coverage
- Add scenario tests

### Phase 4 (Ongoing)
- Maintain coverage as code evolves
- Add tests for new features
- Refine existing tests

## Metrics Tracking

Track these metrics over time:
- Coverage percentage by type
- Number of uncovered critical paths
- Test execution time
- Test flakiness rate
- Code churn vs test churn
```

Generate a detailed coverage analysis following this structure.
```

---

### test-edge-cases

> **Description**: Identify and test edge cases.
> **Input Format**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `test`

#### Template Content:
```markdown
# Identify Edge Cases

Please identify comprehensive edge cases for the following code or feature:

{{args}}

  ## Edge Case Categories

  ### 1. Boundary Values

  #### Numeric Boundaries
- Zero (0)
- Negative numbers (-1, -100)
- Positive numbers (1, 100)
- Maximum values (Integer.MAX_VALUE, Number.MAX_SAFE_INTEGER)
- Minimum values (Integer.MIN_VALUE, Number.MIN_SAFE_INTEGER)
- Infinity and -Infinity
- NaN (Not a Number)
- Floating point precision issues (0.1 + 0.2)
- Very large numbers
- Very small numbers (near zero)

  #### String Boundaries
- Empty string ("")
- Single character
- Very long strings (1MB+)
- Strings with special characters
- Unicode characters and emojis
- Null bytes (\0)
- Strings with only whitespace
- Leading/trailing whitespace

  #### Collection Boundaries
- Empty array/list ([])
- Single element array
- Very large arrays (millions of elements)
- Null or undefined collections
- Nested empty collections

  #### Date/Time Boundaries
- Epoch time (1970-01-01)
- Very old dates (1900-01-01)
- Future dates (2100-01-01)
- Leap years
- End of year/month
- Daylight saving time transitions
- Different time zones
- Invalid dates (February 30)

  ### 2. Input Validation

  #### Type Mismatches
- Passing string when number expected
- Passing null when object expected
- Passing undefined
- Passing array when string expected
- Mixed types in collections

  #### Format Issues
- Invalid email formats
- Invalid phone numbers
- Invalid URLs
- Invalid JSON
- Invalid XML
- Malformed data structures

  #### Missing Data
- Required fields missing
- Null values
- Undefined values
- Empty objects
- Partial data

  ### 3. State-Related Edge Cases

  #### Order Dependencies
- Operations in different order
- Concurrent operations
- Race conditions
- First-time vs subsequent operations

  #### Lifecycle Edge Cases
- Before initialization
- During initialization
- After cleanup/disposal
- Repeated initialization
- Multiple cleanups

  #### State Combinations
- Combinations of flags/settings
- Conflicting states
- Invalid state transitions

  ### 4. Concurrency Edge Cases

  #### Threading Issues
- Multiple simultaneous requests
- Race conditions
- Deadlocks
- Resource contention

  #### Timing Issues
- Very fast operations
- Very slow operations
- Timeouts
- Retries

  ### 5. Resource Constraints

  #### Memory
- Out of memory scenarios
- Memory leaks
- Large data structures
- Many objects in memory

  #### Storage
- Disk full
- Read-only file system
- File permissions
- File locks

  #### Network
- Network disconnected
- Slow network
- Timeout
- Connection reset
- Partial data received

  ### 6. External Dependencies

  #### Database
- Connection failure
- Query timeout
- Deadlocks
- Duplicate keys
- Foreign key violations

  #### APIs
- API unavailable
- Rate limiting
- Invalid responses
- Slow responses
- Unexpected response format

  #### File System
- File doesn't exist
- File is locked
- No read/write permissions
- Path too long
- Invalid characters in filename

  ### 7. Security Edge Cases

  #### Injection Attacks
- SQL injection
- XSS attacks
- Command injection
- Path traversal

  #### Authentication/Authorization
- Expired tokens
- Invalid tokens
- No authentication
- Insufficient permissions
- Privilege escalation attempts

  ### 8. User Behavior

  #### Unexpected Actions
- Back button usage
- Refresh during operation
- Multiple form submissions
- Rapid clicking
- Copy-paste of data
- Browser auto-fill

  #### International Users
- Different languages
- RTL (right-to-left) languages
- Special characters in names
- Different date/number formats
- Different currencies

  ### 9. Browser/Platform Differences

  #### Cross-Browser
- Different JavaScript engines
- Different CSS rendering
- Different APIs available
- Different storage limits

  #### Device Differences
- Small screens
- Touch vs mouse
- Slow devices
- Limited storage
- Poor network

  ### 10. Business Logic Edge Cases

  #### Domain-Specific
- Minimum order quantities
- Maximum cart size
- Discount combinations
- Expired promotions
- Out of stock
- Partial fulfillment

  #### Workflow Edge Cases
- Skipping steps
- Going backwards
- Abandoning process
- Re-entering process

  ## Output Format

For each edge case, provide:

  ### 1. Description
Clear description of the edge case

  ### 2. Input
Specific input values that trigger it

  ### 3. Expected Behavior
What should happen

  ### 4. Potential Issues
What could go wrong if not handled

  ### 5. Test Case
Concrete test case to verify handling

  ### 6. Fix/Handling
How to properly handle this edge case

  ## Example Output

```markdown
### Edge Case: Empty Input Array

**Description**: Function receives an empty array as input

**Input**: `[]`

**Expected Behavior**:
- Should return empty result
- Should not throw error
- Should handle gracefully

**Potential Issues**:
- Array access without length check
- Division by zero (average of empty array)
- Null pointer when accessing first element

**Test Case**:
```javascript
test('should handle empty array', () => {
  const result = processArray([]);
  expect(result).toEqual([]);
  expect(result).not.toThrow();
});
```

**Fix/Handling**:
```javascript
function processArray(arr) {
  if (!arr || arr.length === 0) {
    return [];
  }
  // Process array
}
```
```

  ## Priority Levels

Mark each edge case with priority:
- **Critical**: Could cause system failure or data loss
- **High**: Could cause incorrect behavior
- **Medium**: Could cause user confusion
- **Low**: Minor inconvenience

Generate a comprehensive list of edge cases following this structure.
```

---

## <a name='writing'></a> Writing

### write-email

> **Description**: Draft professional emails.
> **Input Format**: `Email Content or Goal`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `writing`

#### Template Content:
```markdown
# Draft Professional Email

Please help draft a professional email for:

{{args}}

  ## Email Structure

  ### 1. Subject Line

Create a clear, specific subject line:
- Concise (5-7 words)
- Action-oriented when needed
- Descriptive of content
- Professional tone

**Good Examples:**
- "Meeting Request: Project Timeline Discussion"
- "Update: Q4 Feature Release Schedule"
- "Question about API Documentation"
- "Follow-up: Yesterday's Design Review"

**Bad Examples:**
- "Hey" (too casual)
- "Important!" (vague)
- "Read this" (demanding)

  ### 2. Greeting

Choose appropriate salutation:

**Formal:**
- Dear [First Name] [Last Name],
- Dear Mr./Ms./Dr. [Last Name],
- Dear Hiring Manager,

**Professional:**
- Hi [First Name],
- Hello [First Name],

**Team/Group:**
- Hi team,
- Hello everyone,
- Dear colleagues,

**No Name Known:**
- Hello,
- Greetings,

  ### 3. Opening Line

Start with purpose or context:

**For First Contact:**
- "I hope this email finds you well."
- "I'm reaching out regarding [topic]."
- "My name is [name], and I'm [role] at [company]."

**For Follow-up:**
- "Following up on our conversation about [topic]..."
- "Thank you for your time yesterday discussing [topic]."
- "I wanted to check in about [previous topic]."

**For Request:**
- "I'm writing to request [specific thing]."
- "I'd like to ask for your help with [topic]."

**For Update:**
- "I wanted to update you on [topic]."
- "Quick update about [project/topic]."

  ### 4. Body

  #### Paragraph 1: Purpose
State main reason clearly (1-2 sentences):
- "The purpose of this email is to [objective]."
- What you need/want
- Why you're writing

  #### Paragraph 2: Details
Provide necessary context:
- Background information
- Relevant details
- Supporting information
- Use bullet points for clarity:
  - Point 1
  - Point 2
  - Point 3

  #### Paragraph 3: Action Items (if applicable)
Clear next steps:
- What you need from recipient
- Deadlines if applicable
- Specific requests

  ### 5. Closing

**Call to Action:**
- "Please let me know if this works for you."
- "I'd appreciate your feedback by [date]."
- "Could you please review and approve by [date]?"
- "Let me know if you have any questions."

**Polite Sign-off:**
- "Thank you for your time and consideration."
- "I appreciate your help with this."
- "Looking forward to your response."
- "Thanks in advance for your assistance."

  ### 6. Signature

**Professional Format:**
```
Best regards,
[Your Name]
[Your Title]
[Company Name]
[Email]
[Phone] (optional)
[LinkedIn] (optional)
```

**Sign-offs by Context:**
- **Formal**: Sincerely, Respectfully,
- **Professional**: Best regards, Kind regards,
- **Friendly**: Thanks, Cheers, Warm regards,
- **Casual**: Best, Thanks again,

  ## Email Templates by Type

  ### Template 1: Meeting Request

```
Subject: Meeting Request: [Topic] Discussion

Hi [Name],

I hope this email finds you well. I'd like to schedule a meeting to discuss [specific topic].

I believe it would be beneficial to align on:
- Point 1
- Point 2
- Point 3

Would you be available for a [duration]-minute meeting next week? I'm flexible with timing and happy to work around your schedule. Here are some options:
- [Date/Time option 1]
- [Date/Time option 2]
- [Date/Time option 3]

Please let me know what works best for you, or suggest an alternative time.

Thank you,
[Your Name]
```

  ### Template 2: Following Up

```
Subject: Follow-up: [Previous Topic]

Hi [Name],

I wanted to follow up on my email from [date] regarding [topic].

To recap, I was hoping to [restate request/question]. I understand you're busy, but this would help us [benefit/reason].

If you need any additional information from me, please don't hesitate to ask.

I'd appreciate an update when you have a moment.

Thanks again,
[Your Name]
```

  ### Template 3: Requesting Information

```
Subject: Question about [Topic]

Hi [Name],

I have a question about [specific topic] and thought you might be able to help.

[Provide context in 1-2 sentences]

Specifically, I'm wondering:
- Question 1
- Question 2

Any guidance you can provide would be greatly appreciated. There's no rush, but if possible, having this information by [date] would be helpful for [reason].

Thank you for your time,
[Your Name]
```

  ### Template 4: Sharing Update

```
Subject: Update: [Project/Topic]

Hi [Name/Team],

I wanted to share a quick update on [project/topic].

**Progress:**
- Completed item 1
- Completed item 2

**In Progress:**
- Item 3 (expected completion: [date])
- Item 4 (expected completion: [date])

**Upcoming:**
- Item 5 (starting: [date])

**Blockers:**
- Issue 1: [brief description and needed help]

Please let me know if you have any questions or concerns.

Best regards,
[Your Name]
```

  ### Template 5: Asking for Feedback

```
Subject: Feedback Request: [Topic/Document]

Hi [Name],

I hope you're doing well. I've completed [document/project/work] and would greatly appreciate your feedback.

[Provide brief context about what you're sharing]

I've attached [document] / shared the link: [URL]

Specifically, I'm looking for feedback on:
- Area 1
- Area 2
- Area 3

If possible, could you review by [date]? I want to ensure we have time to incorporate your suggestions before [deadline/reason].

Thank you for your time and expertise.

Best regards,
[Your Name]
```

  ### Template 6: Thank You

```
Subject: Thank You for [Specific Thing]

Hi [Name],

I wanted to take a moment to thank you for [specific action/help].

[Explain impact or how it helped you]

Your [expertise/time/guidance] was invaluable, and I really appreciate you taking the time to [what they did].

Thanks again for your support.

Best regards,
[Your Name]
```

  ### Template 7: Declining Politely

```
Subject: Re: [Original Subject]

Hi [Name],

Thank you for thinking of me for [opportunity/request].

Unfortunately, I won't be able to [take on project/attend meeting/etc.] due to [brief, professional reason - current commitments/schedule conflicts/etc.].

[If appropriate] I'd be happy to [offer alternative/suggest someone else/help in different way].

I appreciate your understanding.

Best regards,
[Your Name]
```

  ### Template 8: Apology/Error Correction

```
Subject: Correction: [Topic]

Hi [Name],

I realized there was an error in my previous email about [topic].

[Clearly state the mistake]

The correct information is:
[Provide correct details]

I apologize for any confusion this may have caused. Please let me know if you have any questions.

Thank you for your understanding.

Best regards,
[Your Name]
```

  ## Email Best Practices

  ### Do's ✅
- **Be Clear**: State purpose in first paragraph
- **Be Concise**: Respect recipient's time
- **Be Specific**: Include dates, times, details
- **Be Polite**: Use please and thank you
- **Be Professional**: Proper grammar and spelling
- **Use Paragraphs**: Break up text for readability
- **Proofread**: Check before sending
- **Include Context**: If continuing conversation
- **Use Bullet Points**: For lists or multiple points
- **Set Clear Expectations**: Deadlines, next steps

  ### Don'ts ❌
- **Don't Use All Caps**: LOOKS LIKE SHOUTING
- **Don't Over-Explain**: Keep it focused
- **Don't Use Emojis**: Unless very casual context
- **Don't Send When Emotional**: Wait and revise
- **Don't Forget Attachments**: Mention if included
- **Don't Use Unclear Pronouns**: Be specific
- **Don't Write Novels**: Keep it brief
- **Don't Be Vague**: Be specific about requests
- **Don't Assume Tone Conveys**: Be explicit
- **Don't Overuse Exclamation Points**: Unprofessional

  ## Tone Guidelines

  ### Formal (Senior executives, clients, first contact)
- Use complete sentences
- Avoid contractions
- Use formal salutations
- Professional language
- Structured format

  ### Professional (Colleagues, regular contacts)
- Friendly but respectful
- Can use contractions
- Clear and direct
- Appropriate warmth
- Professional tone

  ### Casual (Close colleagues, internal team)
- Conversational
- Friendly tone
- Brief and direct
- Can be less formal
- Still professional

  ## Email Checklist

Before sending, verify:

- [ ] Subject line is clear and relevant
- [ ] Recipient email is correct
- [ ] Greeting is appropriate
- [ ] Purpose stated clearly in opening
- [ ] All necessary information included
- [ ] Action items are clear
- [ ] Deadlines specified if applicable
- [ ] Tone is appropriate for recipient
- [ ] Grammar and spelling checked
- [ ] Attachments included if mentioned
- [ ] Signature is complete
- [ ] Reply all used appropriately
- [ ] Sent at appropriate time

Generate a complete, professional email following these guidelines.
```

---

### write-presentation

> **Description**: Create presentation outlines.
> **Input Format**: `Input Content`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `writing`

#### Template Content:
```markdown
# Create Presentation Outline

Please create a comprehensive presentation outline for:

{{args}}

  ## Presentation Planning

  ### 1. Audience Analysis

**Who is your audience?**
- Technical level: Beginner/Intermediate/Expert
- Role: Developers/Managers/Executives/Mixed
- Size: Small group / Large audience
- Prior knowledge: What do they already know?
- What they care about: Their interests/concerns

**Audience Goals:**
- What do they want to learn?
- What problems are they trying to solve?
- What decisions will they make after?

  ### 2. Presentation Goals

**Primary Objective:**
What is the ONE main thing you want audience to take away?

**Secondary Objectives:**
- Objective 1
- Objective 2
- Objective 3

**Success Metrics:**
How will you know if presentation was successful?
- Audience understands [concept]
- Audience can [action]
- Audience feels [emotion/confidence]

  ### 3. Presentation Structure

  ## Opening (5 minutes)

  ### Slide 1: Title Slide
**Content:**
- Presentation Title
- Your Name & Title
- Date
- Company/Conference Logo

**Speaker Notes:**
"Good [morning/afternoon], thank you for joining me today."

---

  ### Slide 2: Hook / Problem Statement
**Content:**
- Compelling statistic or fact
- Relatable problem scenario
- Provocative question

**Visual:**
- Impactful image
- Large number/stat
- Problem illustration

**Speaker Notes:**
"[Tell brief story or present problem that resonates]"

**Example:**
"Did you know that 70% of software projects fail due to poor architecture decisions? Today, we're going to explore how to avoid becoming part of that statistic."

---

  ### Slide 3: Agenda / What You'll Learn
**Content:**
"In the next [X] minutes, we'll cover:
1. [Topic 1]
2. [Topic 2]
3. [Topic 3]
4. [Topic 4]"

**Visual:**
- Simple numbered list
- Progress bar showing sections
- Timeline

**Speaker Notes:**
"By the end of this presentation, you'll understand [key benefit]."

---

  ## Body Section 1: [Foundation] (10 minutes)

  ### Slide 4: Main Concept Introduction
**Content:**
- Clear definition
- Why it matters
- Key principle

**Visual:**
- Simple diagram
- Icon + text
- Minimal text (rule: 6 words per line, 6 lines max)

**Speaker Notes:**
[Detailed explanation you'll say verbally]

---

  ### Slide 5: Deep Dive
**Content:**
- Detailed breakdown
- 3-4 key points

**Visual:**
- Diagram/illustration
- Before/after comparison
- Process flow

**Speaker Notes:**
"Let me break this down..."

---

  ### Slide 6: Example
**Content:**
- Real-world example
- Code snippet (if technical)
- Case study

**Visual:**
- Code with syntax highlighting
- Screenshot
- Real example

**Speaker Notes:**
"Here's how this works in practice..."

---

  ## Body Section 2: [Application] (10 minutes)

  ### Slide 7: Transition
**Content:**
- Bridge from theory to practice
- "Now that we understand [X], let's see how to apply it"

**Visual:**
- Simple transition graphic
- Icon indicating shift

---

  ### Slide 8-10: Step-by-Step Process
**Content (each slide):**
- One step per slide
- Clear action items
- Visual demonstration

**Visual:**
- Numbered steps
- Screenshots
- Diagrams

**Speaker Notes:**
"First, you'll... Then... Finally..."

---

  ### Slide 11: Demo (if applicable)
**Content:**
- "Let me show you..."
- Live demo or video

**Visual:**
- Screen sharing
- Video recording
- Animated GIF

**Speaker Notes:**
[Detailed demo script with what you'll show]

---

  ## Body Section 3: [Advanced Topics / Best Practices] (8 minutes)

  ### Slide 12: Key Takeaways
**Content:**
- 3-5 most important points
- Best practices
- Do's and Don'ts

**Visual:**
- Checkmarks and X marks
- Two column: Good vs Bad
- Icons

---

  ### Slide 13: Common Mistakes
**Content:**
- Top 3 pitfalls to avoid
- How to recognize them
- How to fix them

**Visual:**
- Warning icons
- Before/after examples

---

  ### Slide 14: Pro Tips
**Content:**
- Advanced techniques
- Insider knowledge
- Efficiency hacks

**Visual:**
- Lightbulb icons
- Highlighted text

---

  ## Closing (5 minutes)

  ### Slide 15: Summary
**Content:**
"Today we covered:
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]"

**Visual:**
- Same structure as agenda slide
- Checkmarks showing completion

**Speaker Notes:**
"Let's quickly recap what we've learned..."

---

  ### Slide 16: Call to Action
**Content:**
- What to do next
- Action steps
- Where to learn more

**Visual:**
- Clear action button/text
- Next steps list

**Example:**
"Your Next Steps:
1. Try implementing [X] in your project
2. Read the documentation at [URL]
3. Join our community at [link]"

---

  ### Slide 17: Resources
**Content:**
- Links to documentation
- Further reading
- Contact information
- Community links

**Visual:**
- QR codes
- Clickable links
- Resource icons

---

  ### Slide 18: Q&A
**Content:**
- "Questions?"
- Your contact info
- Social media handles

**Visual:**
- Large question mark
- Friendly image
- Contact details

**Speaker Notes:**
"I'll be happy to answer any questions."

---

  ### Slide 19: Thank You
**Content:**
- "Thank You!"
- Your name
- Email/Twitter/LinkedIn
- Where to find slides

**Visual:**
- Professional photo
- Contact info
- Company/event logo

---

  ## Presentation Best Practices

  ### Slide Design

**Visual Principles:**
- **One idea per slide**
- **Minimal text**: 6x6 rule (6 words per line, 6 lines max)
- **High contrast**: Dark text on light background or vice versa
- **Large fonts**: Minimum 24pt, prefer 32pt+
- **Quality images**: High resolution, relevant
- **Consistent design**: Same fonts, colors throughout
- **White space**: Don't crowd slides

**Color Guidelines:**
- Use brand colors or professional palette
- Maximum 3-4 colors
- Ensure accessibility (color blind friendly)
- High contrast for readability

**Fonts:**
- Sans-serif for body (Arial, Helvetica, Calibri)
- Maximum 2 font families
- Size hierarchy: Title (40-44pt), Heading (32-36pt), Body (24-28pt)

  ### Content Guidelines

**Text:**
- Bullet points, not paragraphs
- Active voice
- Action-oriented language
- Avoid jargon (or explain it)

**Visuals:**
- Use diagrams over text when possible
- Arrows to show flow/relationships
- Icons to represent concepts
- Charts/graphs for data

**Code (if technical):**
- Syntax highlighting
- Large font (18-20pt minimum)
- Focus on key lines
- Remove boilerplate
- Add comments for clarity

  ### Delivery Tips

**Preparation:**
- Rehearse 3-5 times
- Time yourself
- Practice transitions
- Prepare for technical issues
- Have backup plan (offline slides)

**During Presentation:**
- Make eye contact
- Use natural gestures
- Speak clearly and pace yourself
- Pause for emphasis
- Engage audience with questions
- Tell stories and examples
- Show enthusiasm

**Handling Questions:**
- Listen fully before answering
- Repeat question for audience
- Be honest if you don't know
- Offer to follow up
- Keep answers concise

  ### Timing Guide

For 30-minute presentation:
- Opening: 5 minutes (15%)
- Body section 1: 8 minutes (25%)
- Body section 2: 8 minutes (25%)
- Body section 3: 5 minutes (15%)
- Conclusion: 4 minutes (10%)
- Q&A: 10 minutes (30%)

**Buffer:** Plan for 80% of allotted time, leaving 20% buffer

  ### Technical Checklist

**Before Presentation:**
- [ ] Test equipment (projector, mic, clicker)
- [ ] Check internet connection
- [ ] Test demos/videos
- [ ] Have backup of slides (USB, email, cloud)
- [ ] Arrive early to set up
- [ ] Test from presenter mode
- [ ] Check display resolution
- [ ] Silence phone
- [ ] Have water available

**Slide Deck Checklist:**
- [ ] No typos or grammar errors
- [ ] All images load properly
- [ ] Videos embedded or linked
- [ ] Fonts embedded (or using system fonts)
- [ ] Links work
- [ ] Consistent formatting
- [ ] Speaker notes complete
- [ ] Timing practiced
- [ ] Exported to PDF (backup)

  ### Audience Engagement

**Techniques:**
- Ask questions
- Show of hands polls
- Quick exercises
- Group discussions
- Real-time demos
- Share relatable stories
- Use humor (appropriately)
- Reference current events

**Interactive Elements:**
- Live polls (Mentimeter, Slido)
- Q&A throughout (not just end)
- Chat for questions
- Breakout discussions
- Hands-on exercises

  ## Specialized Presentation Types

  ### Technical Deep Dive
- More code examples
- Detailed diagrams
- Architecture views
- Performance metrics
- Technical trade-offs

  ### Executive Presentation
- Focus on business value
- ROI and metrics
- Strategic implications
- Less technical detail
- More business context

  ### Workshop/Tutorial
- Heavy on demos
- Step-by-step guides
- Hands-on exercises
- Code repositories
- Follow-along format

  ### Conference Talk
- Entertaining
- Storytelling
- Big picture ideas
- Memorable takeaways
- Social media friendly

  ## Slide Note Example

**Slide 5: "Why This Matters"**

**Content on Slide:**
- Reduces bugs by 40%
- Saves 10 hours/week
- Improves team collaboration

**Visual:**
- Three icons with stats
- Bar chart showing improvements

**Speaker Notes:**
"Now you might be wondering, why should you care about this? Let me give you three compelling reasons.

First, teams using this approach report 40% fewer bugs in production. That's almost half the bugs you're dealing with right now.

Second, developers save an average of 10 hours per week. That's time you can spend building features instead of fixing issues.

And third, this dramatically improves team collaboration because everyone's on the same page about code quality.

Let me share a quick story about how one team implemented this..."

Generate a complete presentation outline following this structure.
```

---

### write-technical-blog

> **Description**: Write technical blog posts.
> **Input Format**: `Blog Topic or Outline`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-21`
> **Tags**: `writing`

#### Template Content:
```markdown
# Write Technical Blog Post

Please write a comprehensive technical blog post about:

{{args}}

  ## Blog Post Structure

  ### 1. Title

Create an engaging, SEO-friendly title:
- Clear and specific
- Include main keyword
- Promise value/solution
- 50-60 characters optimal

**Format examples:**
- "How to [Achieve Result] with [Technology]"
- "[Technology]: A Complete Guide for [Audience]"
- "[Number] Ways to [Benefit] using [Technology]"
- "Understanding [Concept]: A Deep Dive"

  ### 2. Meta Description (150-160 characters)
Brief summary for search engines and social sharing.

  ### 3. Introduction

**Hook** (1-2 paragraphs):
Start with:
- A relatable problem
- Surprising stat or fact
- Personal anecdote
- Common misconception

**Context** (1-2 paragraphs):
- Why this topic matters
- Who should read this
- What you'll learn

**Preview**:
"In this post, you'll learn:
- Key point 1
- Key point 2
- Key point 3"

  ### 4. Main Content

  #### Section 1: [Foundational Concept]

**Explanation**:
Clear, concise explanation of the concept

**Code Example**:
```javascript
// Well-commented, working code
```

**Visual Aid** (if applicable):
Diagram, screenshot, or ASCII art

**Key Takeaway**:
- Main point summarized

---

  #### Section 2: [Practical Application]

**Real-World Scenario**:
Describe when/why you'd use this

**Step-by-Step Guide**:
1. **Step 1**: Description
   ```javascript
   // Code
   ```

2. **Step 2**: Description
   ```javascript
   // Code
   ```

3. **Step 3**: Description
   ```javascript
   // Code
   ```

**Common Pitfalls**:
- ⚠️ Mistake 1: How to avoid
- ⚠️ Mistake 2: How to avoid

---

  #### Section 3: [Advanced Topic]

**Going Deeper**:
Advanced concepts for experienced readers

**Code Example**:
```javascript
// More complex implementation
```

**Performance Considerations**:
- Optimization tip 1
- Optimization tip 2

**Best Practices**:
- ✅ Do this
- ❌ Don't do this

  ### 5. Complete Working Example

**Full Implementation**:
```javascript
// Complete, working code example
// that readers can copy and run
```

**Demo/Live Example**:
Link to CodePen, CodeSandbox, or GitHub repo

  ### 6. Comparison / Alternatives

Compare with related approaches:

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| Approach A | ... | ... | ... |
| Approach B | ... | ... | ... |

  ### 7. Troubleshooting

**Common Issues**:

**Issue 1: Error message or problem**
- **Cause**: Why it happens
- **Solution**: How to fix it
- **Prevention**: How to avoid it

**Issue 2: Error message or problem**
- **Cause**: Why it happens
- **Solution**: How to fix it
- **Prevention**: How to avoid it

  ### 8. Conclusion

**Summary**:
- Recap main points in 2-3 sentences
- Restate key benefit

**Call to Action**:
- Try implementing this
- Share your results
- Ask questions in comments
- Check out related posts

**Next Steps**:
- Related topic to explore
- Advanced guide link
- Community resources

  ### 9. Additional Resources

**Further Reading**:
- [Official Documentation](link)
- [Related Article](link)
- [Video Tutorial](link)

**Tools & Libraries**:
- [Tool 1](link): Description
- [Tool 2](link): Description

**Community**:
- [Forum/Discord](link)
- [GitHub Discussions](link)

  ## Writing Style Guidelines

  ### Tone
- **Conversational**: Write like you're explaining to a friend
- **Clear**: Avoid unnecessary jargon
- **Confident**: Be authoritative but not condescending
- **Encouraging**: Make readers feel capable

  ### Structure
- **Short paragraphs**: 2-4 sentences max
- **Subheadings**: Every 200-300 words
- **Lists**: Break down complex info
- **White space**: Don't wall-of-text

  ### Code Examples
- **Working**: All code should run
- **Complete**: Include imports/setup
- **Commented**: Explain non-obvious parts
- **Formatted**: Proper indentation
- **Tested**: Verify it works

  ### Visuals
- **Diagrams**: For architecture/flow
- **Screenshots**: For UI/tools
- **Syntax highlighting**: For code
- **Annotations**: Point out key parts

  ## SEO Best Practices

  ### Keywords
- Include main keyword in title
- Use in first paragraph
- Sprinkle naturally throughout
- Use in subheadings

  ### Structure
- Use H2, H3 hierarchy
- Add meta description
- Internal links to related posts
- External links to authority sites

  ### Readability
- Short sentences (15-20 words)
- Simple language (8th-grade level)
- Active voice
- Scannable format

  ## Content Checklist

Before publishing, verify:

- [ ] Title is clear and compelling
- [ ] Introduction hooks the reader
- [ ] Code examples are complete and working
- [ ] Explanations are clear and jargon-free
- [ ] Screenshots/diagrams enhance understanding
- [ ] Common pitfalls are addressed
- [ ] Troubleshooting section included
- [ ] Conclusion summarizes key points
- [ ] Links to resources provided
- [ ] SEO optimized (keywords, meta, structure)
- [ ] Proofread for typos/grammar
- [ ] Technical accuracy verified
- [ ] Code tested and runs correctly

  ## Example Sections

  ### Good Introduction Example:
```
Ever spent hours debugging only to find a missing semicolon? We've all been there.
But what if I told you there's a way to catch these errors before they even reach
your browser?

That's where [Technology] comes in. It's a static analysis tool that checks your
code as you write it, catching errors, enforcing best practices, and making your
code more maintainable.

In this comprehensive guide, you'll learn:
- How to set up [Technology] in your project
- Essential rules every developer should use
- Advanced configurations for team projects
- Common issues and how to solve them

Whether you're a beginner or experienced developer, this guide will help you write
better, more reliable code.
```

  ### Good Conclusion Example:
```
You've now learned how to set up [Technology], configure it for your project, and
customize it for your team's needs. By following these best practices, you'll catch
bugs earlier, write more consistent code, and ship with confidence.

Ready to try it? Start by adding [Technology] to one of your projects today. Begin
with the basic configuration, then gradually add rules as your team gets comfortable.

Have questions or run into issues? Drop a comment below or join the [community link].

**Next Steps:**
- Check out my guide on [related topic]
- Explore the [official documentation]
- Join the [community] for support

Happy coding!
```

Generate a complete, publication-ready blog post following these guidelines.
```

---


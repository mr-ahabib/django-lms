
---

```markdown
# 🎓 Learning Management System (LMS) API Documentation

## 🧩 1. Project Overview

This project is a **Learning Management System (LMS)** built with **Django REST Framework (DRF)** for the backend.

It allows **students** to enroll in online courses, **instructors** to create and manage their own courses, and **admins** to oversee the entire system — including users, courses, enrollments, and payments.

The API follows REST principles, supports **JWT authentication**, and integrates **Stripe** for secure online payments.  
All operations are permission-controlled based on user roles.

---

## 🧱 2. Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django, Django REST Framework (DRF) |
| Database | MySQL (for local dev) |
| Authentication | JWT (SimpleJWT) |
| Payment Gateway | Stripe API |
| Caching (optional) | Redis |
| Frontend | (to be built using Next.js or React) |

---

## 👥 3. User Roles and Permissions

| Role | Description | Permissions |
|------|--------------|-------------|
| 🧑‍🎓 **Student** | Enrolls in and pays for courses | - Can view courses <br> - Can make payments <br> - Can view own enrollments & payments |
| 🧑‍🏫 **Instructor** | Creates and manages courses | - Can create/update/delete own courses <br> - Can view payments related to their courses |
| 🧑‍💼 **Admin** | Manages entire system | - Full CRUD on all users, courses, enrollments, and payments |

---

## 🌐 4. Base URL

```

[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

```

### 🔑 Authentication Header

Add this to all protected endpoints:

```

Authorization: Bearer <access_token>

````

---

## 👤 5. Users API

### 🪪 Register
**POST** `/users/register/`  
**Auth:** ❌ No  

Creates a new user.

**Request:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123",
  "role": "student"
}
````

**Response:**

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "role": "student"
}
```

---

### 🔐 Login

**POST** `/users/login/`
**Auth:** ❌ No

Returns JWT tokens.

**Request:**

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### ♻️ Token Refresh

**POST** `/users/token/refresh/`
**Auth:** ❌ No

**Request:**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response:**

```json
{
  "access": "<new_access_token>"
}
```

---

### 👤 Current User

**GET** `/users/me/`
**Auth:** ✅ Yes

**Response:**

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "role": "student"
}
```

---

## 📚 6. Courses API

| Method    | Endpoint         | Auth | Role             | Description         |
| --------- | ---------------- | ---- | ---------------- | ------------------- |
| GET       | `/courses/`      | ✅    | All              | List all courses    |
| POST      | `/courses/`      | ✅    | Instructor/Admin | Create a new course |
| GET       | `/courses/{id}/` | ✅    | All              | Get a course by ID  |
| PUT/PATCH | `/courses/{id}/` | ✅    | Instructor/Admin | Update a course     |
| DELETE    | `/courses/{id}/` | ✅    | Instructor/Admin | Delete a course     |

**Example Course Object:**

```json
{
  "id": 2,
  "title": "Django REST Framework Masterclass",
  "description": "Build real-world APIs with Django and DRF",
  "price": "120.00",
  "instructor": 3,
  "created_at": "2025-10-25T14:00:00Z"
}
```

**Create Course Example:**

```http
POST /courses/
```

**Request:**

```json
{
  "title": "Next.js for Beginners",
  "description": "Frontend fundamentals using Next.js 15",
  "price": 99.99
}
```

---

## 🎓 7. Enrollments API

| Method | Endpoint             | Auth | Role          | Description                                         |
| ------ | -------------------- | ---- | ------------- | --------------------------------------------------- |
| GET    | `/enrollments/`      | ✅    | All           | List enrollments                                    |
| POST   | `/enrollments/`      | ✅    | Student       | Create enrollment (usually automatic after payment) |
| GET    | `/enrollments/{id}/` | ✅    | Student/Admin | Retrieve enrollment                                 |
| DELETE | `/enrollments/{id}/` | ✅    | Admin         | Delete enrollment                                   |

**Example Enrollment Object:**

```json
{
  "id": 1,
  "student": 1,
  "course": 2,
  "enrolled_at": "2025-10-25T15:00:00Z"
}
```

> 🧠 Note: When a payment is successful, the system automatically creates an enrollment for the student via **Stripe Webhook**.

---

## 💳 8. Payments API

| Method | Endpoint             | Auth | Role          | Description          |
| ------ | -------------------- | ---- | ------------- | -------------------- |
| GET    | `/payments/`         | ✅    | All           | List payments        |
| POST   | `/payments/`         | ✅    | Student       | Create payment       |
| GET    | `/payments/{id}/`    | ✅    | Student/Admin | Get a payment by ID  |
| DELETE | `/payments/{id}/`    | ✅    | Admin         | Delete payment       |
| POST   | `/payments/webhook/` | ❌    | Stripe        | Handle Stripe events |

---

### 💰 Create Payment

**POST** `/payments/`

**Request:**

```json
{
  "course": 2,
  "amount": 120.00
}
```

**Response:**

```json
{
  "client_secret": "",
  "payment": {
    "id": 5,
    "student": 1,
    "course": 2,
    "amount": "120.00",
    "status": "pending",
    "stripe_payment_intent": "pi_3Pdxxxxxx"
  }
}
```

Use `client_secret` on the frontend to confirm payment using **Stripe.js**.

---

### 🧾 Webhook Endpoint

**POST** `/payments/webhook/`

Stripe will send events like:

* `payment_intent.succeeded`
* `payment_intent.payment_failed`

**Example Webhook Payload:**

```json
{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_3Pdxxxxxx",
      "amount_received": 12000,
      "metadata": {
        "student_id": "1",
        "course_id": "2"
      }
    }
  }
}
```

**Backend Logic:**

* Updates payment status to `"succeeded"`
* Creates an enrollment for the student in the course

---

## 🧭 9. Role-Based Workflow

| Step | Role       | Action                      | Endpoint                             | Description              |
| ---- | ---------- | --------------------------- | ------------------------------------ | ------------------------ |
| 1    | Admin      | Registers or promotes users | `/users/register/`                   | Creates accounts         |
| 2    | Instructor | Creates courses             | `/courses/`                          | Posts new course         |
| 3    | Student    | Views courses               | `/courses/`                          | Browses course catalog   |
| 4    | Student    | Makes payment               | `/payments/`                         | Initiates Stripe payment |
| 5    | Stripe     | Sends payment confirmation  | `/payments/webhook/`                 | Confirms payment         |
| 6    | System     | Auto-enrolls student        | `/enrollments/`                      | Creates enrollment       |
| 7    | Student    | Views enrollments           | `/enrollments/`                      | Sees enrolled courses    |
| 8    | Admin      | Monitors all                | `/payments/`, `/courses/`, `/users/` | Full control             |

---

## 🧩 10. Future Enhancements

* Course reviews & ratings
* Instructor dashboards & analytics
* Certificate generation
* Email notifications (SendGrid/Mailgun)
* Frontend integration using Next.js

---




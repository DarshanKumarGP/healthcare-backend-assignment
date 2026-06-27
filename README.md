# Healthcare Backend — Django + DRF + PostgreSQL + JWT

A secure backend for a healthcare application: users register/log in, then manage
patient and doctor records and assign doctors to patients. Built for the WhatBytes
Backend Developer Intern assignment — and built to be a little better than asked.

This README is written as a step-by-step mentor walkthrough. Follow it top to bottom
and you'll have the project running, tested, and submitted.

---

## 0. What's in this project

```
healthcare-backend-assignment/
├── manage.py
├── requirements.txt
├── .env.example            # copy to .env and fill in real values
├── .gitignore
├── postman_collection.json # import into Postman, everything pre-built
├── README.md                # you are here
├── healthcare_backend/       # Django project config (settings, urls, wsgi/asgi)
├── core/                      # shared utilities: permissions, pagination,
│                               # validators, consistent response envelope,
│                               # global error handler
├── accounts/                  # custom User model + register/login (JWT)
├── patients/                  # Patient model + CRUD, owned by the creator
├── doctors/                   # Doctor model + CRUD, shared directory
└── mappings/                  # PatientDoctorMapping + assign/list/remove
```

Each Django app follows the same internal shape: `models.py` → `serializers.py` →
`views.py` → `urls.py` → `admin.py`. Once you've read one app you can read all of them.

---

## 1. Prerequisites

Install these once on your machine before touching the project:

1. **Python 3.10+** — check with `python3 --version`
2. **PostgreSQL 13+** — check with `psql --version`. If you don't have it:
   - macOS: `brew install postgresql@15 && brew services start postgresql@15`
   - Ubuntu/Debian: `sudo apt update && sudo apt install postgresql postgresql-contrib`
   - Windows: install from https://www.postgresql.org/download/windows/
3. **Git** — to push your final repo to GitHub.

---

## 2. Project setup (do this once)

Open a terminal in the folder where you unzipped this project (the folder containing
`manage.py`), then run each block in order.

### 2.1 Create and activate a virtual environment

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You'll know it worked because your terminal prompt now starts with `(venv)`.

### 2.2 Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django, Django REST Framework, simplejwt, psycopg2 (PostgreSQL driver),
python-decouple (.env loader), and django-cors-headers.

### 2.3 Create the PostgreSQL database

Open a `psql` shell:

```bash
psql -U postgres
```

Then, inside the `psql` prompt, run:

```sql
CREATE DATABASE healthcare_db;
CREATE USER healthcare_user WITH PASSWORD 'your_strong_password';
ALTER ROLE healthcare_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;
\q
```

(If you'd rather just use your existing `postgres` superuser and its password, that's
fine too — skip creating `healthcare_user` and use `postgres` in the next step.)

### 2.4 Configure environment variables

Copy the template and edit it:

```bash
cp .env.example .env
```

Open `.env` and fill in the database values you just created, for example:

```env
SECRET_KEY=any-long-random-string-you-want
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432

ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
```

`.env` is already in `.gitignore` — it will never be pushed to GitHub. Good, because it
holds your DB password.

### 2.5 Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

You should see a list of `Applying accounts.0001_initial... OK`,
`Applying patients.0001_initial... OK`, etc.

### 2.6 (Optional) Create an admin superuser

```bash
python manage.py createsuperuser
```

It will ask for email, name, and password (there's no "username" — this project uses
email as the login field). Once created, you can browse all data at
`http://127.0.0.1:8000/admin/`.

### 2.7 Run the development server

```bash
python manage.py runserver
```

You should see `Starting development server at http://127.0.0.1:8000/`.

Open `http://127.0.0.1:8000/api/health/` in your browser — you should get:

```json
{ "success": true, "message": "Healthcare Backend API is running.", "data": { "status": "ok" } }
```

If you see that, the whole stack — Django, DRF, PostgreSQL — is wired correctly.

---

## 3. Testing every endpoint

### Option A — Postman (recommended, fastest)

1. Open Postman → **Import** → select `postman_collection.json` from this project.
2. The collection has a `base_url` variable already set to `http://127.0.0.1:8000/api`.
3. Run **Auth → Register** once (creates a test user).
4. Run **Auth → Login**. A test script automatically saves the returned access token
   into the collection variable `access_token` — every other request in the collection
   already has Bearer auth wired to that variable, so you don't paste tokens by hand.
5. Run requests in the **Patients**, **Doctors**, **Mappings** folders top to bottom.
   "Create" requests auto-save the new record's id (`patient_id`, `doctor_id`,
   `mapping_id`) so the detail/update/delete requests right below them just work.

### Option B — curl

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith", "email": "jane@example.com", "password": "SecurePass123"}'

# 2. Login (copy the "access" value from the response)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "password": "SecurePass123"}'

# 3. Use the token for everything else
export TOKEN="paste-the-access-token-here"

# Create a patient
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 34, "gender": "M", "address": "221B Baker Street", "phone_number": "+919876543210"}'

# List your patients
curl http://127.0.0.1:8000/api/patients/ -H "Authorization: Bearer $TOKEN"

# Create a doctor
curl -X POST http://127.0.0.1:8000/api/doctors/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "Dr. Aarav Mehta", "specialization": "Cardiology", "age": 45, "gender": "M"}'

# Assign the doctor to the patient (use the real ids returned above)
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"patient": 1, "doctor": 1}'

# See all doctors assigned to patient 1
curl http://127.0.0.1:8000/api/mappings/1/ -H "Authorization: Bearer $TOKEN"
```

---

## 4. Full API reference

Every response (success or error) follows one of two consistent shapes:

```jsonc
// Single object
{ "success": true, "message": "...", "data": { ... } }

// List endpoints (paginated)
{ "success": true, "count": 12, "next": "...", "previous": null, "results": [ ... ] }

// Errors
{ "success": false, "message": "...", "errors": { "field": ["what's wrong"] } }
```

### Authentication

| Method | Endpoint | Auth | Body |
|---|---|---|---|
| POST | `/api/auth/register/` | none | `{ "name", "email", "password" }` |
| POST | `/api/auth/login/` | none | `{ "email", "password" }` → returns `access`, `refresh`, `user` |

Send the access token on every other request as `Authorization: Bearer <token>`.
Access tokens expire after 60 minutes (configurable in `.env`); use the `refresh`
token with simplejwt's standard refresh flow if you extend this project further.

### Patients (private to the creator)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Add a new patient |
| GET | `/api/patients/` | List **your own** patients |
| GET | `/api/patients/<id>/` | Get one patient (must be yours) |
| PUT | `/api/patients/<id>/` | Update a patient (must be yours) |
| DELETE | `/api/patients/<id>/` | Delete a patient (must be yours) |

Patient fields: `name`, `age` (0-150), `gender` (`M`/`F`/`O`), `address`,
`phone_number`, `medical_history`.

### Doctors (shared directory, owner-only writes)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a new doctor |
| GET | `/api/doctors/` | List **all** doctors (any authenticated user) |
| GET | `/api/doctors/<id>/` | Get one doctor (any authenticated user) |
| PUT | `/api/doctors/<id>/` | Update a doctor (creator only) |
| DELETE | `/api/doctors/<id>/` | Delete a doctor (creator only) |

Doctor fields: `name`, `specialization`, `age` (18-100, optional), `gender`
(optional), `email` (optional), `phone_number` (optional).

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient: body `{ "patient": <id>, "doctor": <id> }` |
| GET | `/api/mappings/` | List all mappings you created |
| GET | `/api/mappings/<patient_id>/` | List all doctors assigned to that patient |
| DELETE | `/api/mappings/<mapping_id>/` | Remove a mapping |

> **A deliberate design call, worth mentioning in your interview:** the original
> spec lists `GET /api/mappings/<patient_id>/` and `DELETE /api/mappings/<id>/` as
> if they were different URL shapes, but they're actually the *same* path
> (`/api/mappings/<id>/`) used with two different HTTP methods. Rather than invent
> an inconsistent extra path segment to avoid the "collision," this project embraces
> it: one view (`MappingDetailView`) handles `GET` (interpreting `<id>` as a patient
> id, returning that patient's doctors) and `DELETE` (interpreting `<id>` as a
> mapping id, removing that mapping). That's exactly what REST means by letting the
> HTTP verb carry the intent on a shared resource path. Mentioning this shows you
> read the spec closely rather than just pattern-matching it.

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | No-auth liveness check |

---

## 5. Design decisions (read this before your interview)

A few choices that go beyond the bare assignment text — be ready to explain *why*:

- **Email-based login, no separate username.** The spec says "register with name,
  email, and password" — there's no mention of a username, so the custom `User`
  model in `accounts/models.py` drops it entirely and uses email as the unique
  identifier. One less field for the client to send, one less thing that can be
  inconsistent with the email.
- **Patients are private; doctors are shared.** The spec literally says "Retrieve
  all patients **created by the authenticated user**" but "Retrieve all doctors"
  (no ownership qualifier). The permission classes in `core/permissions.py` encode
  exactly that asymmetry — `IsOwner` for patients, `IsOwnerForWriteElseAuthenticated`
  for doctors (anyone can read, only the creator can edit/delete).
- **Consistent response envelope everywhere.** Every endpoint — success or error —
  returns the same `{success, message, data}` (or `{success, count, results}` for
  lists) shape, via `core/utils.success_response` and
  `core/exception_handler.custom_exception_handler`. A frontend integrating with
  this API never has to special-case any single endpoint's response shape.
- **Validation beyond "is it present."** Phone numbers are regex-validated
  (`core/validators.py`), ages are range-checked, duplicate patient-doctor mappings
  are rejected, and you can't assign a doctor to a patient you don't own (checked in
  `mappings/serializers.py`).
- **Environment-based configuration.** All secrets and the database connection
  live in `.env` (via `python-decouple`), never hard-coded — exactly what "use
  environment variables for sensitive configurations" asks for.
- **JWT via `djangorestframework-simplejwt`**, with the login response enriched to
  include basic user info (`accounts/serializers.py: LoginSerializer`) so the
  frontend doesn't need a second round trip just to know who's logged in.

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `psycopg2` fails to install | On Linux you may need `sudo apt install libpq-dev python3-dev` first. On Apple Silicon Macs, try `pip install psycopg2-binary` again after `brew install postgresql`. |
| `django.db.utils.OperationalError: could not connect to server` | PostgreSQL isn't running. Start it (`brew services start postgresql@15` or `sudo service postgresql start`), or double-check `DB_HOST`/`DB_PORT` in `.env`. |
| `FATAL: password authentication failed for user` | The `DB_USER`/`DB_PASSWORD` in `.env` don't match what you created in step 2.3. |
| `relation "patients_patient" does not exist` | You forgot to run `python manage.py migrate`. |
| `401 Unauthorized` on every protected endpoint | Your access token expired (60 min default) or wasn't sent. Log in again and re-copy the token, or just re-run the Postman Login request. |
| Port 8000 already in use | Run `python manage.py runserver 8001` and use that port instead. |

---

## 7. Pushing to GitHub and submitting

```bash
git init
git add .
git commit -m "Healthcare backend: Django + DRF + PostgreSQL + JWT"
```

Create a new **empty** repository on GitHub (don't initialize it with a README —
you already have one), then:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Double-check before you submit:

- [ ] `.env` is **not** in the repo (check on GitHub — only `.env.example` should appear)
- [ ] `python manage.py runserver` works from a fresh clone after following section 2
- [ ] All endpoints in section 4 respond as documented
- [ ] The repo is public, or you've added the reviewer as a collaborator

Then reply to the assignment email with your GitHub repo link, as instructed:
> "Please send your GitHub repo link in the email thread."

Good luck with the interview — lean on section 5 above if they ask you to justify any
design choice; it shows you understood the spec rather than just transcribed it.

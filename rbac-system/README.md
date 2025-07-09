# 🛡️ Role-Based Access Control (RBAC) Web App with Guest Access
A full-stack RBAC system built using **Flask (Python)** and a **simple frontend (HTML, Bootstrap, JavaScript)**. Users are assigned roles like Admin, Manager, Contributor, or Viewer, and can perform actions based on their role. Public **guest links** can also be generated to share resource access externally.


## 🖥️ Frontend Usage
All interaction happens through your browser using these HTML pages:

| Page                            | Description                                                   |
|---------------------------------|---------------------------------------------------------------|
| `register.html`                 | New users sign up (name, email, password, role)               |
| `login.html`                    | Users login to receive a JWT and get redirected               |
| `dashboard.html`                | Role-based UI showing only allowed actions                    |
| `guest-view.html?token=<token>` | Anyone can access a resource via a shared link                |


## 👥 Roles & Permissions
| Role        | Can Create Org  | Can Create Dept    | Can Create Resource   | Can Share Resource    | Can View    |
|-------------|-----------------|--------------------|-----------------------|-----------------------|----------   |
| Admin       | ✅              | ✅                | ✅                    | ✅                   | ✅          |
| Manager     | ❌              | ✅                | ✅                    | ✅                   | ✅          |
| Contributor | ❌              | ❌                | ✅                    | ❌                   | ✅          |
| Viewer      | ❌              | ❌                | ❌                    | ❌                   | ✅(Read-only) |
| Guest       | ❌              | ❌                | ❌                    | ❌                   | ✅(via token) |


## 📸 How to Use the App (Step-by-Step)
1. **Open `register.html` in your browser**
   - Fill in name, email, password, and role (Admin/Manager/etc.)
   - On success, you’re redirected to the login page.

2. **Login from `login.html`**
   - Enter your registered email and password
   - You’ll be redirected to `dashboard.html`
   - Your role determines which actions are visible

3. **Dashboard**
   - Admin can create orgs, depts, resources, and share links
   - Manager can create depts/resources and share links
   - Contributor can create resources only
   - Viewer can view, but not modify anything

4. **Creating Organizations**
   - Admins will see a form to enter an Org name
   - On success, you’ll get the Org ID from the alert or check DB

5. **Creating Departments**
   - Managers/Admins can enter Org ID and Dept Name

6. **Creating Resources**
   - Contributors/Managers/Admins can enter:
     - Dept ID
     - Resource Title
     - Resource Content
   - On success, a Resource ID is returned (needed for guest sharing)

7. **Generating Guest Links**
   - Managers/Admins enter:
     - Resource ID
     - Permission (`view` or `edit`)
     - Expiry in days
   - A guest link will appear below — shareable with anyone

8. **Guest Access**
   - Guests can visit:
     guest-view.html?token=<your-token-here>
   - They'll be able to see the resource (and edit, if allowed)


## 🏗️ Technologies Used
- **Frontend**:
  - HTML5 + Bootstrap 5
  - Vanilla JavaScript (Fetch API)
  - LocalStorage for JWT and user info

- **Backend**:
  - Flask + Flask-JWT-Extended
  - SQLAlchemy for ORM
  - SQLite DB (can be replaced with PostgreSQL/MySQL)


## 🔧 Setup Guide (Localhost)
### 1. Clone the project
git clone https://github.com/your-username/rbac-system.git
cd rbac-system

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Initialize the database
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

### 5. Start the Flask server
python backend/run.py
Server will run at `http://127.0.0.1:5000`

## 🌐 Open Frontend Pages
You can open each of the following pages directly in your browser:

* `templates/register.html`
* `templates/login.html`
* `templates/dashboard.html`
* `templates/guest-view.html?token=...`

Make sure the Flask server is running so the frontend can call the backend APIs.


## 📂 File Structure (Simplified)
rbac-system/
├── backend/
│   ├── app/
│   │   ├── models/            ← SQLAlchemy models
│   │   ├── routes/            ← Auth, orgs, resources, guest
│   │   └── utils/             ← Role-based decorator
│   ├── run.py                 ← Flask entry point
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── guest-view.html
├── requirements.txt
└── README.md

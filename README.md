# Admin Dashboard Application

A web-based application for managing user and vaccination data efficiently. The Admin Dashboard provides a simple interface for performing CRUD (Create, Read, Update, Delete) operations and streamlining vaccination record management as well as users searching for their data.

---

## **Features**

### User Management:
- Add new users with detailed personal information.
- View user records in a tabular format.
- Edit existing user details dynamically.
- Delete users from the database.
- Search bar for Users 

### Vaccination Management:
- Add and update vaccination details for each user.
- View a user’s vaccination history, including type, manufacturer, and status.

### Admin Features:
- Secure login system for admin access.
- Easy-to-navigate dashboard interface.
- Logout functionality to protect admin sessions.

---

## **Tech Stack**

### Backend:
- **Django**: Framework for handling backend operations.
- **Django REST Framework (DRF)**: To build RESTful APIs for the app.
- **SQLite**: Default database for development.

### Frontend:
- **HTML**: Structure of the web application.
- **CSS**: Styling for the application UI.
- **JavaScript**: Dynamic behavior and interactions.

---

## **API Endpoints**

The app uses RESTful APIs for all data operations.

| **Endpoint**                              | **Method** | **Description**                       |
|-------------------------------------------|------------|---------------------------------------|
| `/api/retrieveindividuals/`               | GET        | Fetch all users and their data.      |
| `/api/individual/<patient_number>/`       | GET        | Fetch data for a specific user.      |
| `/api/admin/update/<patient_number>/`     | PUT        | Update user and vaccination details. |
| `/api/admin/delete/<patient_number>/`     | DELETE     | Delete a user record.                |
| `/api/individual_with_vaccination/`       | POST       | Add a new user and their vaccination.|

---

## **Setup and Installation**

### Prerequisites:
- Python (v3.8+ recommended)
- `pip` (Python package manager)

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/admin-dashboard.git
   cd admin-dashboard
   ```

2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework
   ```

3. **Set Up the Database**:
   - Apply migrations to initialize the database:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**:
   - Open your browser and go to `http://127.0.0.1:8000/`.

---

## **Usage**

### Dashboard

1. Log in using your admin credentials.
2. Use the **Add New User** button to register a user.
3. View, edit, or delete user records directly from the table.

### Vaccination Management
- View vaccination history for each user.
- Add or update vaccination records (type, manufacturer, status, etc.).

### Logout
- Click the logout button to securely end your session.

---

## **Development Notes**

### File Structure:
- `templates/`: Contains the HTML files for the app.
- `static/css/`: Stores CSS files for styling.
- `static/js/`: Contains JavaScript for dynamic behavior.
- `views.py`: Manages backend logic and API endpoints.
- `urls.py`: Defines routes for the application.

### Customization:
- Update the `styles.css` file in `static/css/` to modify the design.
- Extend the `views.py` file to add new features or endpoints.

---

## **Troubleshooting**

1. **Database Issues**:
   - Ensure migrations are correctly applied with:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

2. **API Errors**:
   - Use tools like **Postman** to test endpoints and verify request payloads.

3. **Static Files Not Loading**:
   - Collect static files by running:
     ```bash
     python manage.py collectstatic
     ```

4. **JavaScript Errors**:
   - Open browser developer tools (F12) and check the console for logs.

---

## **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push the changes:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
- Built using the Django and Django REST Framework.
- Inspired by the need for efficient vaccination and user record management.

Link to Pitchdeck https://gamma.app/docs/Vaccination-Tracker-A-Comprehensive-Solution-for-Vaccination-and--vje5fr4sy517ew2

Feel free to contribute, suggest improvements, or report issues. 🚀
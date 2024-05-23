# RS Fullstack Developer Challenge

## Environment Setup Instructions

### Client Setup

To set up the frontend environment, follow these steps:

1. cd into the client directory `cd client`
2. Install the dependencies with `npm install`
3. Build the client app with `npm run build`

### Server Setup

To initialize the server environment and database, follow these steps:

1. From the `scripts` directory, execute `./init-db.sh` to initialize the database. Alternatively, review the script and manually set up the database.
2. Install `pipenv` by running `pip install pipenv` for managing Python packages.
3. Use `pipenv install` to install the server dependencies.
4. Activate the virtual environment with `pipenv shell`.
5. Migrate the database schemas with `python manage.py migrate`.
6. Collect static assets `python manage.py collectstatic`.
7. Start the Django API server with `python manage.py runserver`.

## Project Objective

The goal is to develop a comprehensive product gallery application enabling users to register, log in, and manage (add/update/delete) products. Each product should include attributes such as name, price, description, and images.

### Requirements

#### Setup

- Prepare your development environment following the provided setup instructions.

#### Backend

- Implement the following RESTful API endpoints:
  1. User Registration
  2. CRUD operations for Products
- Modify the product deletion functionality from hard delete to soft delete. Implement a way to record the deletion date of products.

Ensure the backend is scalable, secure, and adheres to best practices for API development.

#### Frontend

- Design and implement the UI using a CSS framework or vanilla CSS for:
  1. Login page
  2. Registration page
  3. A grid view displaying the user's products

Focus on responsive design and user experience.

### Additional Tasks

For additional credit, consider implementing the following features:

1. **Security Enhancements:**
   - Conduct a security audit of both the server and client.
   - Implement improvements such as secure authentication, data validation, and protection against common vulnerabilities.

2. **Codebase Optimization:**
   - Review the codebase for any redundant code or logic and remove it.

3. **Version Control:**
   - Utilize Git for version control.
   - Ensure regular commits with clear and concise commit messages.
   - Push your project to GitHub and maintain a clean, organized repository.

4. **Testing:**
   - Write comprehensive unit tests for the newly created API endpoints.

5. **Deployment:**
   - Deploy the project to a cloud service such as Heroku, AWS, or GCP.
   - Ensure the deployment process is documented and reproducible.

6. **Documentation:**
   - Provide documentation for the API endpoints. -> generate schema locally using `./manage.py spectacular --color --file schema.yml --validate`

**Note:** Pay attention to both the project description and the existing codebase for additional insights and requirements.

**Submission:** Please ensure your project is thoroughly documented and submitted via GitHub. Include instructions for accessing the deployed application, if applicable.

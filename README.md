# Quiz CLI App
A simple quiz system.

**Features**:-

* **Roles**:
  * Admin: can add quizzes & questions
  * Student: can take quizzes
  * Unclassified: a temporary role for when a new user attempts to create an admin account but couldn't provide the secret key
* **Authentication & Authorization**
  * Login/Registration
  * Admin registration
* **Data Persistence**
  * User data is stored on disk under the location set in the DB_LOCATION_ON_DISK constant inside of the constants.py file
* **Security**
  * Sensitive data like passwords are hashed and stored as as a salted hash
* **Portability & Compatibility**
  * All data is stored with portability in mind
  * The use of JSON in Persistent Storage ensures that the user data is stored in a way that’s portable and universal

**Technical:-**
  * **Meaningful error messaging** on wrong input & input verification using guard clauses to force correct input
  * **OO** design of critical and expected-to-change components
  * **Code Reuse**: the usage of a constants file to store all values that are project wide
  * **Function-driven design**, which ensures abstraction, improves maintainability, enables code reuse, and allows for the implementation to be easily updated later and for all
  * Design pattern usage:-
    * **Singleton** pattern for the Database component, ensuring that there’s either zero or one single instance of the database at any given time, which ensures data protection against corruption
    * **MVC** pattern
  * Note when running the source code via an IDE:-
    * Before deploying the app, set the environment variable for the admin secret with the name QUIZ_APP_ADMIN_SECRET inside the .env file

**Enjoy!**

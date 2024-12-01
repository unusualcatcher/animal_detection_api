# Animal Detection API with YOLO

This is a Django-based API that uses the YOLO (You Only Look Once) model to classify images of animals into categories like CAT, DOG, or COW. The project also accepts location data and stores animal information in a database.

## Project Setup

### 1. Download the Project

First, download the project ZIP file, extract it to your desired location.

### 2. Set Up Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

#### On macOS/Linux:
```bash
# Navigate to the project directory
cd path/to/animal_detection_api

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```
#### On Windows:
```
# Navigate to the project directory
cd path\to\animal_detection_api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```
### 3. Install Dependencies
Once the virtual environment is activated, install the necessary dependencies:
```
pip install -r requirements.txt
```
### 4. Configure Database
The project uses SQLite by default for database storage, but you can configure any other database you prefer.

Run database migrations to create the necessary tables:
```
python manage.py migrate
```
### 5. Run the Development Server
After everything is set up, you can run the Django development server:
```
python manage.py runserver
```
This will start the application on http://127.0.0.1:8000/. You can use tools like Postman to send POST requests to the API endpoints.

### 6. API Endpoints
Submit Image and Location (/submit/)
This endpoint accepts an image in Base64 format and location data (latitude, longitude) to classify the animal in the image.

Method: POST

Get All Animal Locations (/api/locations/)
This endpoint returns all the animals' locations stored in the database.

Method: GET

### Custom CNN Model
The custom CNN model was trained using a kaggle notebook which is available at: https://www.kaggle.com/code/unusualcatcher/notebooka4be39a321



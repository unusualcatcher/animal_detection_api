import base64
import cv2
import numpy as np
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
from .models import Animal

# Load the YOLO model (you can customize the path or model type)
model = YOLO('best.pt')

def decode_base64_to_image(base64_string):
    """
    Decodes a Base64-encoded string and converts it into an image format suitable for YOLO.
    
    Args:
        base64_string (str): The complete Base64-encoded string (with or without metadata).
    
    Returns:
        np.ndarray: The decoded image as a NumPy array.
    """
    # Step 1: Remove Base64 metadata if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]

    # Step 2: Decode Base64 to bytes
    image_data = base64.b64decode(base64_string)

    # Step 3: Convert bytes to a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Step 4: Decode NumPy array to an OpenCV image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return image


def resize_image_to_128x128(image):
    """
    Resizes an image to 128x128 dimensions.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The resized image.
    """
    resized_image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_AREA)
    return resized_image


def classify_image_with_yolo(image):
    """
    Uses YOLO to classify an image as CAT, DOG, or COW.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        str: The classification result (CAT, DOG, or COW).
    """
    results = model(image,imgsz=128)  # Run the YOLO model on the image
    labels = results[0].names  # Get class names from YOLO
    predictions = results[0].boxes  # Bounding boxes and predictions
    
    # Filter predictions for CAT, DOG, or COW
    relevant_classes = {"cat", "dog", "cow"}
    detected_labels = [labels[int(box.cls)] for box in predictions if labels[int(box.cls)] in relevant_classes]

    if not detected_labels:
        return "None detected"
    
    return detected_labels[0]  

@csrf_exempt
def submit(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)

            # Extract and decode the Base64 image
            base64_image = data.get("image")
            if not base64_image:
                return JsonResponse({"error": "Image data is required"}, status=400)

            decoded_image = decode_base64_to_image(base64_image)

            # Resize the decoded image to 128x128
            resized_image = resize_image_to_128x128(decoded_image)

            # Extract location data
            location = data.get("location", {})
            latitude = location.get("latitude")
            longitude = location.get("longitude")

            if latitude is None or longitude is None:
                return JsonResponse({"error": "Location data is incomplete"}, status=400)

            # Classify the resized image
            classification = classify_image_with_yolo(resized_image)
            actual_classification=classification

            if classification.lower() == "none detected":
                return JsonResponse({"error": "No valid animal detected"}, status=400)
            if classification.lower() == "cat":
                actual_classification='dog'
            elif classification.lower() == 'dog':
                actual_classification='cat'

            # Create and save the Animal object
            animal = Animal.objects.create(
                name=actual_classification.upper(),
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({
                "message" : "The image has successfully been submitted."
            })

        except (ValueError, KeyError) as e:
            return JsonResponse({"error": f"Invalid request data: {str(e)}"}, status=400)


def locations(request):
    """
    Queries all animal objects from the database and returns them as a JSON array 
    matching the specified TypeScript structure.
    """
    try:
        # Query all Animal objects
        animals = Animal.objects.all()

        # Prepare the response in the required format
        animal_locations = [
            {
                "latitude": animal.latitude,
                "longitude": animal.longitude,
                "animalType": animal.name.upper()  
            }
            for animal in animals
        ]

        # Return the response as JSON
        return JsonResponse(animal_locations, safe=False)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

from flask import Flask, request, jsonify, render_template
import random
import os
from PIL import Image
import pytesseract
import sys
sys.path.append('D:\\Learning\\GenAi\\hackalthon\\Chatbot\\')
import GenAI as GAI

app = Flask(__name__)

# Mock customer data (In a real app, this would come from a database)
customers = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "status": "active",
        "App-Status": "Income Verification Pend"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "status": "inactive",
        "App-Status": "Hard Decline"
    }
]

# Predefined responses for different queries
responses = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm just a bot, but I'm doing fine! How can I assist you?",
    "what is your name": "I'm your customer support assistant. How can I help you?",
    "order status": "Please provide your order number, and I'll check the status for you.",
    "thanks": "You're welcome! Let me know if you need further assistance.",
    "default": "Sorry, I didn't understand that. Could you please rephrase?"
}

# Route for the home page that serves the index.html
@app.route('/')
def index():
    return render_template('index.html')

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_query = data.get('query', '').lower()

        response = responses.get(user_query, responses["default"])

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Sorry, I encountered an error."})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    try:
        output = image_process(file_path)
    except Exception as e:
        output = f"An error occurred during image processing: {str(e)}"

    print(f"Processed output: {output}")  # For debugging purposes
    return jsonify({"message": output})


def image_process(image):
    process = Image.open(image)
    Text_conversion = pytesseract.image_to_string(image)
    response = GAI.check_verification_status(Text_conversion)
    return response


# Customer validation route
@app.route('/validate_customer', methods=['POST'])
def validate_customer():
    data = request.get_json()
    first_name = data.get('firstName', '').strip()
    last_name = data.get('lastName', '').strip()
    email = data.get('email', '').strip()

    # Basic validation: check if fields are empty
    if not first_name or not last_name or not email:
        return jsonify({"verified": False, "message": "Please fill out all fields."})

    # Check if customer details exist in the mock customer data
    for customer in customers:
        if customer['first_name'].lower() == first_name.lower() and \
           customer['last_name'].lower() == last_name.lower() and \
           customer['email'].lower() == email.lower():
            # If matched, check status and return appropriate response
            if customer['status'] == "active":
                return jsonify({
                    "verified": True,
                    "message": "You have active portfolio. Please choose an below option to take next step forward:",
                    "options": ["1. Dropped mid-flow. Provide the link to continue the application?",
                                "2. Current status of my Application?", 
                                "3. Cancel my Application", 
                                "4. Stucked on the DL page. Need further assistance."]
                })
            else:
                return jsonify({
                    "verified": False,
                    "message": "Customer is inactive. Please contact support."
                })

    # If no match found
    return jsonify({"verified": False, "message": "Details not matched. Please try again."})


if __name__ == '__main__':
    app.run(debug=True)

# Business-card-OCR
 
# Business Card OCR Web Application

## Introduction
The Business Card OCR Web Application allows users to upload images of business cards, extract the text using Optical Character Recognition (OCR), and categorize the extracted information into relevant fields such as email, phone number, address, and website.

## Technologies Used

- **Backend**:
  - **Python**: Provides the core logic for processing the uploaded images and handling OCR operations.
  - **Flask**: Manages the server-side routing and integrates the backend logic with the frontend.

- **Frontend**:
  - **HTML**: Structures the web pages for image upload and result display.
  - **CSS**: Styles the web pages to ensure a user-friendly interface.

- **OCR**:
  - **EasyOCR**: Extracts text from uploaded business card images.

- **Text Processing**:
  - **Regular Expressions (Regex)**: Parses the extracted text to identify and categorize relevant information such as email, phone number, address, and website.

## Usage

1. **Start the Flask Application**
   ```bash
   python app.py
2. **Access the Application**
Open your web browser and go to http://127.0.0.1:5000.

3. **Upload an Image**
On the upload page, click the "Choose File" button and select an image of a business card.
Click the "Upload" button.

4. **View Extracted Details**
After uploading, you will be redirected to the result page where the extracted details are displayed.

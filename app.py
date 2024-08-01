from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageFilter
import numpy as np
import easyocr as ocr
import re
import Levenshtein
import os
import uuid

app = Flask(__name__)
reader = ocr.Reader(['en'])  # Initialize EasyOCR reader

def string_similarity(s1, s2):
    distance = Levenshtein.distance(s1, s2)
    similarity = 1 - (distance / max(len(s1), len(s2)))
    return similarity * 100

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if file:
            # Save the uploaded image to a temporary location
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join('static', filename)
            input_image = Image.open(file)
            input_image.save(filepath)
            
            # Perform OCR on the image
            input_image=input_image.convert("L")
            # input_image = input_image.filter(ImageFilter.MaxFilter(9))
            # input_image.save("geeks.jpg") 
            result = reader.readtext(np.array(input_image))
            result_text = [text[1] for text in result]
            
            EMAIL, PIN, WEB = "", "", ""
            PH, ADD = [], set()
            EID, PID, WID = -1, -1, -1
            PHID, AID = [], []

            for i, string in enumerate(result_text):
                if re.search(r'@', string.lower()):
                    EMAIL = string.lower()
                    EID = i

                match = re.search(r'\d{6,7}', string.lower())
                if match:
                    PIN = match.group()
                    PID = i

                match = re.search(r'(?:ph|phone|phno)?\s*(?:[+-]?\d\s*[\(\)]*){7,}', string)
                match = re.search(r'(?:(?:ph|phone|phno)?\s*(?:\+91[-\s]?)?91[-\s]?)?(?:[+-]?\d\s*[\(\)]*){7,}', string)
                if match and len(re.findall(r'\d', string)) > 5:
                    PH.append(string)
                    PHID.append(i)

                keywords = ['road', 'floor', ' st ', 'st,', 'street', ' dt ', 'district', 'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road', 'state', 'country', 'post', 'zip', 'city', 'zone', 'mandal', 'town', 'rural', 'circle', 'next to', 'across from', 'area', 'building', 'towers', 'village', ' ST ', ' VA ', ' VA,', ' EAST ', ' WEST ', ' NORTH ', ' SOUTH ']
                digit_pattern = r'\d{6,7}'
                if any(keyword in string.lower() for keyword in keywords) or re.search(digit_pattern, string):
                    ADD.add(string)
                    AID.append(i)

                states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'France', 'India', 'Canada', 'Italy', 'South Korea', 'Russia', 'Australia', 'Brazil', 'Spain', 'Mexico', 'USA', 'UK']
                for x in states:
                    similarity = string_similarity(x.lower(), string.lower())
                    if similarity > 50:
                        ADD.add(string)
                        AID.append(i)

                if re.match(r"(?!.*@)(www|.*com$)", string):
                    WEB = string.lower()
                    WID = i

            IDS = [EID, PID, WID] + AID + PHID
            fin = []
            for i, string in enumerate(result_text):
                if i not in IDS:
                    if len(string) >= 4 and ',' not in string and '.' not in string and 'www.' not in string:
                        if not re.match("^[0-9]{0,3}$", string) and not re.match("^[^a-zA-Z0-9]+$", string):
                            numbers = re.findall('\d+', string)
                            if len(numbers) == 0 or all(len(num) < 3 for num in numbers):
                                fin.append(string)
            
            return render_template("results.html", web=WEB, email=EMAIL, pin=PIN, phone=PH, address=ADD, other_details=fin, image_path=filename)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


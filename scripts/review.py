import pandas as pd
import requests
import pdfplumber
import os
import re
from tqdm import tqdm

# Load the CSV file
csv_file_path = './output/Questions_List.csv'
data = pd.read_csv(csv_file_path)

# Filter the data to only include questions of interest
#questions_data = data[data['Correct / Incorrect'] == 'Incorrect'] # incorrect questions only

topics_of_interest = [' infectious/immune/inflammatory disorders']
questions_data = data[data['Subtopic'].isin(topics_of_interest)] # all questions on a given topic

# Function to extract text and images from PDF
def extract_text_and_images_from_pdf(pdf_path, output_dir, question_id):
    text = ""
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text += page.extract_text() + "\n"
            # Extract images
            for img in page.images:
                img_bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                cropped_image = page.within_bbox(img_bbox).to_image()
                img_path = os.path.join(output_dir, f"{question_id}_img_{len(images)+1}.png")
                cropped_image.save(img_path)
                images.append(img_path)
    return text, images

# Create a directory for extracted images
output_dir = './output/extracted_images'
os.makedirs(output_dir, exist_ok=True)

explanations_dir = './output/explanations'
os.makedirs(explanations_dir, exist_ok=True)

# HTML content initialization
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Questions</title>
    <script>
        function checkAnswer(selected, correct, explanationUrl) {
            if (selected === correct) {
                if (confirm("Correct! Would you like to view the explanation?")) {
                    window.open(explanationUrl, '_blank');
                }
            } else {
                if (confirm("Incorrect! Would you like to view the explanation?")) {
                    window.open(explanationUrl, '_blank');
                }
            }
        }
    </script>
</head>
<body>
"""

# Process each row in the filtered data with progress tracking
for index, row in tqdm(questions_data.iterrows(), total=questions_data.shape[0], desc="Processing questions"):
    pdf_url = row['Answer Explanation']
    question_id = row['Question Id']
    content_topic = row['Content Topic']
    content_description = row['Content Description']
    pdf_file_path = 'downloaded.pdf'

    # Download the PDF file
    response = requests.get(pdf_url)
    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(response.content)

    # Extract text and images from the downloaded PDF
    pdf_text, pdf_images = extract_text_and_images_from_pdf(pdf_file_path, output_dir, question_id)

    # Move the explanations to a dedicated folder
    new_pdf_url = os.path.join(explanations_dir, question_id + ".pdf")
    os.rename(pdf_file_path, new_pdf_url)
    new_pdf_url = os.path.join("./explanations", question_id + ".pdf") # poor error handling -- FIX later

    # Parse the text to extract the question, choices, correct answer
    lines = pdf_text.split("\n")
    question = []
    choices = []
    correct_answer = ""
    is_question = True

    choice_pattern = re.compile(r'^[A-Z]\.')

    for line in lines:
        line = line.strip()
        if line.startswith("Correct Answer:"):
            correct_answer = line.split("Correct Answer:")[1].strip().split(".")[0]
            is_question = False
        elif line and is_question:
            if choice_pattern.match(line):
                choices.append(line)
            else:
                question.append(line)

    # Add the question text to the HTML content
    html_content += "<h2>Question:</h2>\n"
    html_content += f"<p>{' '.join(question)}</p>\n"

    # Add any images extracted from the PDF
    for img_path in pdf_images:
        html_content += f"<img src='{img_path}' alt='PDF Image' style='max-width:100%; height:auto;'>\n"

    # Add the answer options to the HTML content
    html_content += "<h3>Options:</h3>\n<ul>\n"
    for choice in choices:
        choice_letter = choice.split('.')[0]
        html_content += f"<li><a href='javascript:void(0)' onclick=\"checkAnswer('{choice_letter}', '{correct_answer}', '{new_pdf_url}')\">{choice}</a></li>\n"
    html_content += "</ul>\n"

    # Add the content topic and description below the answer options
    html_content += f"<p><strong>Content Topic:</strong> {content_topic}</p>\n"
    html_content += f"<p><strong>Content Description:</strong> {content_description}</p>\n"

# Close the HTML tags
html_content += """
</body>
</html>
"""

# Write the HTML content to a file
with open('./output/questions.html', 'w') as html_file:
    html_file.write(html_content)

print("Interactive HTML file 'questions.html' has been created.")

# NBMEanalyzer
A better way to review NBME Self-Assessments. Designed for Step 2 CK. 

This script processes a CSV file containing question data, downloads associated PDFs, extracts text and images from the PDFs, and generates an interactive HTML file that allows users to answer questions and view explanations.

## Prerequisites
- Python 3.6 or higher
- Required Python packages:
	- pandas
	- requests
	- pdfplumber
	- tqdm

## Installation
Clone the repository or download the script.

Install the required Python packages using pip:
```
pip install pandas requests pdfplumber tqdm
```
## Usage
Place the Questions_List.csv file in the same directory as the script.

Run the script:
```
python ./scripts/review.py
```
The script will process the questions, download the associated PDFs, extract text and images, and generate an interactive HTML file named questions.html in the same directory.

## Output
The output will be an HTML file named questions.html that includes:

- Question text
- Images extracted from the PDF, if any
- Answer options
- Content Topic and Content Description
- Interactive functionality to check answers and view explanations

### Progress Tracker
The script includes a progress tracker that shows the processing status of each question.

## Other Scripts
### stats.py
### process.py
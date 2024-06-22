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
Place the `Questions_List.csv` file in the same directory as the script. This file should be downloaded from the NBME insights website under the "Question Details" tab.

### stat.py
First, run the `stat.py` script:
```
python ./scripts/stat.py
```
This script will generate and display useful performance statistics as well as create a new `Questions_List.csv` file that is required for `review.py`. 

### review.py
Next, run the `review.py` script:
```
python ./scripts/review.py
```
The script will process the questions, download the associated PDFs, extract text and images, and generate an interactive HTML file named questions.html in the same directory.

The script's progress will be shown in the terminal.

#### Output
The output of `review.py` will be an HTML file named `questions.html` that includes:

- Question text
- Images extracted from the PDF, if any
- Answer options
- Content Topic and Content Description
- Interactive functionality to check answers and view explanations
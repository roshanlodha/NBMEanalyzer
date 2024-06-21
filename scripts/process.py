import pandas as pd

# Load the CSV file
file_path = './Question_List_1718993426157.csv'
data = pd.read_csv(file_path)

# Extract the form number from the "Exam Take" column
data['Form Number'] = data['Exam Take'].str.extract(r'Form (\d+)')

# Extract the date and time from the "Exam Take" column
data['Date Time'] = data['Exam Take'].str.extract(r'(\d+/\d+/\d+ \| \d+:\d+\w{2})')

# Convert the "Date Time" column to a DateTime object
data['Date Time'] = pd.to_datetime(data['Date Time'], format='%m/%d/%Y | %I:%M%p')

# Drop the "Exam Take" column
#data.drop(columns=['Exam Take'], inplace=True)

# Sort by the "Date Time" column
data = data.sort_values(by=['Form Number', 'Seq'])

# Save the updated dataframe to a new CSV file
data.to_csv('./Questions_List.csv', index=False)

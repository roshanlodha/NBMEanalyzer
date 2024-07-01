import pandas as pd
import os

# Load the CSV file
file_path = './Question_List_1719085415430.csv'
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

# Ensure the "output" directory exists
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# Split the "Content Description" column into three new columns
# If there are fewer than 3 parts, fill the missing parts with empty strings
split_columns = data['Content Description'].str.split(':', expand=True, n=2)
split_columns.columns = ['General Topic', 'Subtopic', 'Subsubtopic']

# Ensure all columns are present
split_columns['Subsubtopic'] = split_columns['Subsubtopic'].fillna('')

# Add the new columns to the dataframe
data = pd.concat([data, split_columns], axis=1)

data.to_csv(os.path.join(output_dir, 'Questions_List.csv'), index=False)

# Calculate incorrect questions based on General Topic
incorrect_by_topic = data[data['Correct / Incorrect'] == 'Incorrect'].groupby('General Topic').size().reset_index(name='Number Incorrect')
total_by_topic = data.groupby('General Topic').size().reset_index(name='Total Questions')
incorrect_by_topic = pd.merge(incorrect_by_topic, total_by_topic, on='General Topic')
incorrect_by_topic['Percent Incorrect'] = (incorrect_by_topic['Number Incorrect'] / incorrect_by_topic['Total Questions']) * 100
incorrect_by_topic = incorrect_by_topic.sort_values(by=['Number Incorrect', 'Percent Incorrect'], ascending=[False, False])

# Calculate incorrect questions based on Subtopic
incorrect_by_subtopic = data[data['Correct / Incorrect'] == 'Incorrect'].groupby('Subtopic').size().reset_index(name='Number Incorrect')
total_by_subtopic = data.groupby('Subtopic').size().reset_index(name='Total Questions')
incorrect_by_subtopic = pd.merge(incorrect_by_subtopic, total_by_subtopic, on='Subtopic')
incorrect_by_subtopic['Percent Incorrect'] = (incorrect_by_subtopic['Number Incorrect'] / incorrect_by_subtopic['Total Questions']) * 100
incorrect_by_subtopic = incorrect_by_subtopic.sort_values(by=['Number Incorrect', 'Percent Incorrect'], ascending=[False, False])

# Save the Incorrect Questions by Subtopic dataframe to a CSV file inside the "output" folder
incorrect_by_subtopic.to_csv(os.path.join(output_dir, 'Incorrect_Questions_by_Subtopic.csv'), index=False)

# Calculate incorrect questions based on Content Description
incorrect_by_description = data[data['Correct / Incorrect'] == 'Incorrect'].groupby('Content Description').size().reset_index(name='Number Incorrect')
total_by_description = data.groupby('Content Description').size().reset_index(name='Total Questions')
incorrect_by_description = pd.merge(incorrect_by_description, total_by_description, on='Content Description')
incorrect_by_description['Percent Incorrect'] = (incorrect_by_description['Number Incorrect'] / incorrect_by_description['Total Questions']) * 100
incorrect_by_description = incorrect_by_description.sort_values(by=['Number Incorrect', 'Percent Incorrect'], ascending=[False, False])

# Calculate average time for correct and incorrect answers
avg_time_correct = data[data['Correct / Incorrect'] == 'Correct']['Time (sec)'].mean()
avg_time_incorrect = data[data['Correct / Incorrect'] == 'Incorrect']['Time (sec)'].mean()

# Calculate average time based on Content Topic
avg_time_by_topic = data.groupby('Content Topic')['Time (sec)'].mean().reset_index(name='Average Time (sec)')

# Calculate average time based on Content Description
avg_time_by_description = data.groupby('Content Description')['Time (sec)'].mean().reset_index(name='Average Time (sec)')

# Output the results
print("Incorrect Questions by General Topic:")
print(incorrect_by_topic)
print("\nIncorrect Questions by Subtopic:")
print(incorrect_by_subtopic)
print("\nIncorrect Questions by Content Description:")
print(incorrect_by_description)
print("\nAverage time for a correct answer:", avg_time_correct)
print("Average time for an incorrect answer:", avg_time_incorrect)
print("\nAverage Time by Content Topic:")
print(avg_time_by_topic)
print("\nAverage Time by Content Description:")
print(avg_time_by_description)

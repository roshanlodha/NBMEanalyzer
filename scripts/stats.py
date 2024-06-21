import pandas as pd

# Load the CSV file
file_path = './Questions_List.csv'
data = pd.read_csv(file_path)

# Calculate incorrect questions based on Content Topic
incorrect_by_topic = data[data['Correct / Incorrect'] == 'Incorrect'].groupby('Content Topic').size().reset_index(name='Number Incorrect')
total_by_topic = data.groupby('Content Topic').size().reset_index(name='Total Questions')
incorrect_by_topic = pd.merge(incorrect_by_topic, total_by_topic, on='Content Topic')
incorrect_by_topic['Percent Incorrect'] = (incorrect_by_topic['Number Incorrect'] / incorrect_by_topic['Total Questions']) * 100
incorrect_by_topic = incorrect_by_topic.sort_values(by=['Number Incorrect', 'Percent Incorrect'], ascending=[False, False])

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
print("Incorrect Questions by Content Topic:")
print(incorrect_by_topic)
print("\nIncorrect Questions by Content Description:")
print(incorrect_by_description)
incorrect_by_description.to_csv('incorrect_by_description.csv', index=False)
print("\nAverage time for a correct answer:", avg_time_correct)
print("Average time for an incorrect answer:", avg_time_incorrect)
print("\nAverage Time by Content Topic:")
print(avg_time_by_topic)
print("\nAverage Time by Content Description:")
print(avg_time_by_description)

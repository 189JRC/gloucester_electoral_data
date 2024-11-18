# Define the input and output file paths
input_file = 'page_content.txt'
output_file = 'page_content_formatted.txt'

# Read the content from the input file
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Remove all newline characters
formatted_content = content.replace('\n', '')

# Write the formatted content to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(formatted_content)
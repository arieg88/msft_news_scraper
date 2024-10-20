def remove_lines(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    with open(output_file_path, 'w', encoding='utf-8', errors='ignore') as output_file:
        for line in lines:
            if not line.startswith(('<<<', '>>>')):
                output_file.write(line)
# Example usage
input_file = 'microsoft_news_analysis.ipynb'
output_file = 'cleaned_microsoft_news_analysis.ipynb'
remove_lines(input_file, output_file)

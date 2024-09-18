import re
import csv

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract questions with a more flexible pattern
    questions = re.findall(r'(\d+)\.?\s*(.*?)\n\s*A\.?\s*(.*?)\n\s*B\.?\s*(.*?)\n\s*C\.?\s*(.*?)\n\s*D\.?\s*(.*?)(?=\n\d+\.|\Z)', content, re.DOTALL)

    csv_data = []
    processed_count = 0
    skipped_count = 0

    for q in questions:
        question_num, question, a, b, c, d = [item.strip() for item in q]
        
        # Find the corresponding comment for this question
        comment_pattern = rf"Commented \[MC\d+\]: ([A-D])\n(.*?)(?=\n\n|\Z)"
        comment_match = re.search(comment_pattern, content[content.index(question):], re.DOTALL)
        
        if comment_match:
            correct_ans = comment_match.group(1)
            explanation = comment_match.group(2).strip()
            correct_ans_index = ord(correct_ans) - ord('A') + 1
            processed_count += 1
        else:
            print(f"Warning: No comment found for question {question_num}")
            correct_ans_index = ''
            explanation = ''
            skipped_count += 1

        row = [question, a, b, c, d, str(correct_ans_index), 'radio', explanation]
        csv_data.append(row)

    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Ans1', 'Ans2', 'Ans3', 'Ans4', 'Correct ans', 'check_radio', 'Explanation'])
        writer.writerows(csv_data)

    print(f"Total questions found: {len(questions)}")
    print(f"Questions processed with answers: {processed_count}")
    print(f"Questions skipped (no answer found): {skipped_count}")
    print(f"Check {output_file} for results.")

# Usage
process_file('AWS-Quiz.txt', 'AWS-Quiz.csv')
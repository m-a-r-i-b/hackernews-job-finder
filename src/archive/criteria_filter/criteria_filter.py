import os
from langchain_openai import ChatOpenAI
from const import CRITERIA_FILE_PATH, RAW_COMMENTS_DIR
from langchain_core.prompts import ChatPromptTemplate
from jinja2 import Template


comments_folder = RAW_COMMENTS_DIR
criteria_file_path = CRITERIA_FILE_PATH

with open(criteria_file_path, 'r') as criteria_file:
    criteria = criteria_file.read().strip()

comment_files = os.listdir(comments_folder)

llm = ChatOpenAI()

def check_comment_with_criteria(comment, criteria):
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir,"prompt"), 'r') as template_file:
        prompt_template_content = template_file.read()

    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template_content),
            ("human", f"""
                Given below is the job post: 
                {comment}

                And the criteria file:
                {criteria}
            """)
        ]
    )

    messages = chat_template.format_messages(comment=comment, criteria=criteria)
    response = llm(messages)
    
    return response.content.strip()

for comment_file_name in comment_files:
    comment_file_path = os.path.join(comments_folder, comment_file_name)
    
    with open(comment_file_path, 'r') as comment_file:
        comment_content = comment_file.read().strip()
    
    decision = check_comment_with_criteria(comment_content, criteria)
    
    print(f"Contents of {comment_file_name}:")
    print(comment_content)
    print(f"Output =  {decision}")
    print('-' * 40)
    break

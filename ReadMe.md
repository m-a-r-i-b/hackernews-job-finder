<p align="center" width=10%>

<img src="https://github.com/user-attachments/assets/df3a2dbb-69aa-4185-88aa-19ec02957e0d" width="40%">
  
</p>


<h3 align="center">
  Leverage LLMs to filter, extract and generate information about each job post on HN  
</h3>



## Agents
- ResumeParser
    -  Description: Extracts work experience and skills from the given resume.
    -  Model: GPT-4 Omni
    
-  IsRemote
    -  Description: Checks if the job post allows remote work or not.
    -  Model: GPT-3.5
   
-  RoleExtractor
    -  Description: Finds out what job roles are being offered in the job post.
    -  Model: GPT-3.5

-  KeywordExtractor
    -  Description: Extracts technological keywords from the job post, such as Python, JavaScript, React, TensorFlow, etc.
    -  Model: GPT-3.5
   
-  ContactInfoExtractor
    -  Description: Extracts email or application links for the job post.
    -  Model: GPT-3.5
   
-  CoverLetterGenerator
    -  Description: Uses the extracted details from your resume and job description to write a small cover letter email based on the overlap between the resume and job description.
    -  Model: GPT-4 Omni



### Demo
https://github.com/user-attachments/assets/db0bfaa1-de86-43d6-8bcc-43e188c53940




### High Level Architecture
![image](https://github.com/user-attachments/assets/829ffcfa-a703-4905-b0e8-8f01224bd404)



### How It Works
- Scraps all posts on a thread, given thread link.
- Submits these posts to a pool of background workers.
- For every post, a worker passes it through a sequence of LLM powered agents to extract info.
- Async updates are pushed to the frontend via web sockets.
- Behind the scenes all data/information is periodically persisted to a json file via a "Fake database" interface.



### Getting Started
1) Clone this repository
2) Provide OpenAI API key in .env file in the backend directory (see .env.sample)
3) Run "docker compose up --build"
4) Open http://localhost:3000 


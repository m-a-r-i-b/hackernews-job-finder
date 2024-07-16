<p align="center" width=10%>

<img src="https://github.com/user-attachments/assets/df3a2dbb-69aa-4185-88aa-19ec02957e0d" width="40%">
  
</p>


<h3 align="center">
  Leverage LLMs to filter, extract and generate information about each job post on HN  
</h3>


## Agents

| **Name**               | **Description**                                                                                              | **Model**        |
|-------------------------|--------------------------------------------------------------------------------------------------------------|------------------|
| **ResumeParser**        | Extracts work experience and skills from the given resume.                                                   | GPT-4 Omni       |
| **IsRemote**            | Checks if the job post allows remote work or not.                                                            | GPT-3.5          |
| **RoleExtractor**       | Finds out what job roles are being offered in the job post.                                                  | GPT-3.5          |
| **KeywordExtractor**    | Extracts technological keywords from the job post, such as Python, JavaScript, React, TensorFlow, etc.        | GPT-3.5          |
| **ContactInfoExtractor**| Extracts email or application links for the job post.                                                        | GPT-3.5          |
| **CoverLetterGenerator**| Uses the extracted details from your resume and job description to write a small cover letter email based on the overlap between the resume and job description. | GPT-4 Omni       |



## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Docker installed on your machine
- OpenAI API key

### Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/m-a-r-i-b/hackernews-job-finder.git
    cd hackernews-job-finder
    ```

2. **Provide OpenAI API key:**

    Navigate to the backend directory:
    ```bash
    cd backend
    ```

    Create a `.env` file with following contents & replace "your_openai_api_key":
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. **Build and run the Docker containers:**
    
    At the root directory of project, run:
    ```bash
    docker-compose up --build
    ```

5. **Open your browser and navigate to:**

    ```arduino
    http://localhost:3000
    ```



## High Level Architecture

<p align="center" width=25%>

<img src="https://github.com/user-attachments/assets/829ffcfa-a703-4905-b0e8-8f01224bd404" width="70%">
  
</p>



## How It Works
- Scraps all posts on a thread, given thread link.
- Submits these posts to a pool of background workers.
- For every post, a worker passes it through a sequence of LLM powered agents to extract info.
- Async updates are pushed to the frontend via web sockets.
- Behind the scenes all data/information is periodically persisted to a json file via a "Fake database" interface.



## Demo
https://github.com/user-attachments/assets/db0bfaa1-de86-43d6-8bcc-43e188c53940


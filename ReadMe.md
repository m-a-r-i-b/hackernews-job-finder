<p align="center" width=25%>
  
![banner](https://github.com/user-attachments/assets/2b65ed44-580d-4474-aa87-7beddfdad173)

  
</p>

## About
An app that provides a simple user interface to scrap "hackernews who is hiring threads" & leverage LLMs to filter, extract and generate information about each job post.   



### Demo
https://github.com/user-attachments/assets/db0bfaa1-de86-43d6-8bcc-43e188c53940




### High Level Architecture
<img src="https://github.com/m-a-r-i-b/hackernews-job-finder/blob/main/system-overview.png" />


### How It Works
- Scraps all posts on a thread
- Submits these posts to a pool of background workers
- For every post, a worker executes passes it through a sequence of LLM powered agents to extract info
- Async updates are pushed to the frontend via web sockets.
- Behind the scenes all data/information is periodically persisted to a json file via a "Fake database" interface.



### Getting Started
1) Clone this repository
2) Provide OpenAI API key in .env file in the backend directory (see .env.sample)
3) Run "docker compose up --build"
4) Open http://localhost:3000 


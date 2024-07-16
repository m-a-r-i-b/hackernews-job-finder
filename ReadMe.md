<p align="center" width=25%>
<img src="https://oscimg.cellmean.com/oscnet/up-3b137e2e6620f7a63f11a96485b1fb3b.png">
</p>


<h3 align="center">
  Leverage LLMs to filter, extract and generate information about each job post on HN  
</h3>


<p align="center" width=50%>
  




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


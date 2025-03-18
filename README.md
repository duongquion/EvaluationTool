# Evaluation Tool
The project is a tool used to calculate the scores of employees working in a department and report the results to people with high authority.
## Why I do?
Project is a system that I use to learn and explore new technologies like GIT, Scrum team, Docker, and a few other tools.
## How to run?
I have designed and you can run it easily using Docker. (But before you run it I recommend you download some environments).
#### Enviroment (Prerequisite)
- Python
- PostgreSQL
- Docker desktop (Recommend if you're using Window)

After you have successfully installed and setup the environment:
1. Install VSCODE extension such as Python Extension Pack (Python, Pylane), Dev Containers, Docker.
2. Make sure there is a Dockerfile in Evaluation-Tool\backend\ , and there is a dockercompose.yml in the root directory (\Evaluation_tool\).
3. Run docker or run the whole project

```docker
docker-compose up -d --build
docker-compose up
```
## Important Note
- Encoding must be UTF-8
- En of Sequence recommend is LF

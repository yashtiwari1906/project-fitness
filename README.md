# project-fitness
An AI assisted fitness application currently only know how to count squats.

# Table of Contents 
  * Installation & Usage
    * Docker Installation & Usage
    * Local Installation & Usage
 
  * Refferences
    - https://google.github.io/mediapipe/


## Installation & Usage
### Docker Installation & Usage
1.) Building an Image from Dockerfile 
- sudo docker build -t <name_of_image> ./docker
2.) Running the image 
- sudo docker run -p 8000:8080 <name_of_image>

### Local Installation & Usage
* make a virtual environment in python 
  - python -m venv <name_of_environment> 
* Install requirements.txt into this virtual environment 
  - pip install -r requirements.txt 
* Activate this Virtual Environment  
  - for linux -> source <name_of_environment>/bin/activate 
  - for windows -> source <name_of_enviroment>/scripts/activate  
* cd src 
* python app.py




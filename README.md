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
1.) make a virtual environment in python 
 - python -m venv <name_of_environment> 
2.) Install requirements.txt into this virtual environment 
 - pip install -r requirements.txt 
3.) Activate this Virtual Environment  
 - for linux -> source <name_of_environment>/bin/activate 
 - for windows -> source <name_of_enviroment>/scripts/activate  
4.) cd src 
5.) python app.py




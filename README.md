# project-fitness
This project is all about implementing machine learning algorithms in the fitness application so that it would help people to learn how modern software concepts are applied with machine learning.

![alt text](https://github.com/yashtiwari1906/project-fitness/blob/main/data/fitness-proj-image.png)

# Table of Contents 
  * Installation & Usage
    * Docker Installation & Usage
    * Local Installation & Usage
 
  * Refferences
    - https://google.github.io/mediapipe/


## Installation & Usage
### Docker Installation & Usage
* Building an Image from Dockerfile 
  - ```sudo docker build -t <name_of_image> ./docker```
* Running the image 
  ```sudo docker run -p 8000:8080 <name_of_image>```

### Local Installation & Usage
* make a virtual environment in python 
  - ```python -m venv <name_of_environment>```
* Install requirements.txt into this virtual environment 
  - ```pip install -r requirements.txt``` 
* Activate this Virtual Environment  
  - for linux -> ```source <name_of_environment>/bin/activate```
  - for windows -> ```source <name_of_enviroment>/scripts/activate```  
* ```cd src``` 
* ```python app.py```




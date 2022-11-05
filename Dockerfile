FROM continuumio/anaconda3
COPY . /app/ 
EXPOSE 8000 
WORKDIR /app/ 
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y && pip install --upgrade pip && pip install -r requirements.txt
CMD ["python",  "./src/app.py"] 



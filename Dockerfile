FROM python:latest

COPY . /home/MovieRecommendApp_v3

WORKDIR /home/MovieRecommendApp_v3

RUN pip install -r /home/MovieRecommendApp_v3/requirements.txt

# CMD ["python", "/recsys/get_rec_model.py"]

# CMD sleep 20

CMD ["python", "main.py"]

EXPOSE 5000

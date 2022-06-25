HOW TO USE:
  - To get one recommended film use 'http://localhost:5000/recommend_one?user_id=user-id'
  - To get several recommended film use 'http://localhost:5000/recommend?user_id=user-id&n=N' where 'user-id' is ID of User and 'N' is amount of film to show. Return .json file where {count :'id': movie_id 'title' :  title  , 'genre' :  genre }
  - To add new film use 'http://localhost:5000/add_new_film' and follow the form.

HOW TO RUN IN DOCKER:
  - Use command 'docker build . --tag [CONTAINER NAME]'
  - Then use command 'docker run -d --network="host" [CONTAINER NAME]'

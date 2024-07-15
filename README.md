
# Movie Collection API

We need to develop a web application which allows people to create collections of movies they like.


## Features

- Register using a username and password(JWT Authentication)
- Retrive all Movies details using third-party API
- Listing of all my movie collections
- Create favaurite movie collection
- Update,retrive and delete collection
- Track number of requests served by the server


## Installation

1. Clone the Repository

```bash
git clone https://github.com/GaneshJondhalekar/Movie_Collection_API.git

cd Movie_Collection_API
```
    
2. Create virtual Environment
```bash
python -m venv env
```

3. Activate Environment
```bash
env\Scripts\activate
```

4. Install requirements.txt
```bash
pip install requirements.txt
```

5. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Running Server
```bash
python manage.py runserver
visit: http://localhost:8000/
```
## API Endpoints

- User Signup: `POST /register/`
- Retrive Movies: `GET /movies/`
- Create Collection: `POST /collection/`
- List Collecction: `GET /collection/`
- Update Collection: `PATCH /collection/uuid/`
- Delete Collection: `DELETE /collection/uuid/`
- Retrive Collection: `GET /collection/uuid/`
- Request Count:  `GET /request-count/`
- Reset request count  `POST /request-count/reset/`


## Support

If facing any problem then reachout to ganeshjondhalekar3@gmail.com

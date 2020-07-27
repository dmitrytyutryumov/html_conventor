## How to run 
### Prepare working rabbitmq and remember host

### build docker images
`docker build . -t convertor_app `
`docker build . -f Dockerfile.celery -t convertor_celery`

BY DEFAULT DEBUG MODE IS OFF. Don't be afraid of plain ui, we will have fix it in few minutes.
`DJANGO DEBUG=True/true` - to switch django to debug mode
`DJANGO DEBUG=Fakse/false/any value except true` - django debug mode is off

### Run it with env vars (all env vars are places in  `.env` file)
`docker run -p 8000:8000 -e DEBUG=False -e RABBITMQ_HOST=172.17.0.1 -d --name convertor_app -v "$PWD/site_parser/media:/usr/src/app/media" -v "$PWD/db.sqlite3:/usr/src/db.sqlite3" convertor_app`

`docker run -e DEBUG=False -e RABBITMQ_HOST=172.17.0.1 -d --name convertor_celery -v "$PWD/site_parser/media:/usr/src/app/media" -v "$PWD/db.sqlite3:/usr/src/db.sqlite3" convertor_celery`

### Run migrations
`docker exec -it convertor_app python manage.py migrate`

## How to upload link/html file. 
* Use this API `http://127.0.0.1:8000/convert/html/`
  ** Request body:
    source -- str/file  // url or html file 
    email -- str  // By this email will have been sent pdf file
    domain -- (optional) str // Correct url, it will be used for html with relative static file paths
  ** Response:
        statuc 200 or 400

### For local development use `docker-compose` 
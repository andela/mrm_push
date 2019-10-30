# mrm_push

## Description

mrm_push is a micro-service that receives notifications from the Google Calendar API and sends them to various subscribers.

---
## Setup using Docker

- Install docker
    ```
    brew cask install docker
    ```
    OR

    [install via dmg file](https://docs.docker.com/docker-for-mac/install/)

- Create Application environment variables and save them in .env file
    ```
    source venv/bin/activate
    export APP_SETTINGS=
    export SECRET_KEY=
    export API_KEY=
    export OOATH2_CLIENT_ID=
    export OOATH2_CLIENT_SECRET=
    export FCM_API_KEY=
    export DEV_NOTIFICATION_URL=
    export NOTIFICATION_URL=
    export DEV_CONVERGE_MRM_URL=
    export CONVERGE_MRM_URL=

    export USER_TOKEN=
    export DEV_REDIS_URL=""
    export PROD_REDIS_URL=""
    export TEST_REDIS_URL=""

    export VAPID_EMAIL=""
    export VAPID_PRIVATE_KEY=""
    export VAPID_PUBLIC_KEY=""
    ```
- Run application.
    ```
    make build
    ```
    This will create 2 services

     - app
     - redis

    Start the gunicorn server
    ```
    make run-app
    ```
- Show services
    ```
    make services
    ```
- Check the status
    ```
    make status
    ```
- Start services individually
    ```
    make start service=<service name>
    ```
- Create services individually
    ```
    make create service=<service name>
    ```
- Stop all services
    ```
    make down
    ```
- Stop services individually
    ```
    make stop service=<service name>
    ```
- Remove services individually
    ```
    make remove service=<service name>
    ```
- Restarting a service
    ```
    make restart service=<service name>
    ```
- Kill services
    ```
    make kill
    ```
- Remove a container
    ```
    make remove
    ```
- SSH into a container
    ```
    make ssh service=<service name>
    ```
- Running Tests

  - Create Application environment variables and save them in .env.tests file. Do not include comments
    ```
    source venv/bin/activate
    export APP_SETTINGS=
    export SECRET_KEY=
    export API_KEY=
    export OOATH2_CLIENT_ID=
    export OOATH2_CLIENT_SECRET=
    export FCM_API_KEY=
    export DEV_NOTIFICATION_URL=
    export NOTIFICATION_URL=
    export DEV_CONVERGE_MRM_URL=
    export CONVERGE_MRM_URL=

    export USER_TOKEN=
    export DEV_REDIS_URL=""
    export PROD_REDIS_URL=""
    export TEST_REDIS_URL=""

    export VAPID_EMAIL=""
    export VAPID_PRIVATE_KEY=""
    export VAPID_PUBLIC_KEY=""
    ```
  - To run  and check for test coverage. Run the command below:
     ```
     make test test="coverage run -m pytest"
     ```

## Endpoints

| Endpoints      | description  |
| ------------- |-------------|
| http://127.0.0.1:8000/subscribe| This endpoint allows users to subscribe to the service. |
| http://127.0.0.1:8000/notifications| This is the endpoint that is hit by the Google calendar API. |
| http://127.0.0.1:8000/refresh|This will update the events in Backend database with the ones in the calendar API. |
| http://127.0.0.1:8000/channels|This will create notification channels for the rooms on the database using the room's calender_id. |

## setup using virtual env.

* Check that python 3(preferably 3.6), pip and virtualenv are installed.
* Clone the mrm_push repo and cd into it.

```
git clone https://github.com/andela/mrm_push.git
```
* Create virtual env using the following command.

```
virtualenv --python=python3 venv
```

* Activate virtual env.

```
source venv/bin/activate
```

* Install dependencies.

```
pip install -r requirements.txt
```

* Create environmental variables and store them in .env file.

```
source venv/bin/activate
export APP_SETTINGS=
export SECRET_KEY=
export API_KEY=
export OOATH2_CLIENT_ID=
export OOATH2_CLIENT_SECRET=
export FCM_API_KEY=
export DEV_NOTIFICATION_URL=
export NOTIFICATION_URL=
export DEV_CONVERGE_MRM_URL=
export CONVERGE_MRM_URL=

export USER_TOKEN=
export DEV_REDIS_URL=""
export PROD_REDIS_URL=""
export TEST_REDIS_URL=""

export VAPID_EMAIL=""
export VAPID_PRIVATE_KEY=""
export VAPID_PUBLIC_KEY=""
```

## Running migrations

- Initial migration commands
```
$ alembic revision --autogenerate -m "Migration message"

$ alembic upgrade head
```
- If you have one migration file in the alembic/version folder. Run the commands below:
```
$ alembic stamp head

$ alembic upgrade head
```
- If you have more than 2 migration files in the alembic/versions folder. Rum the commands bellow
```
$ alembic stamp head

$ alembic upgrade head

$ alembic revision --autogenerate -m "Migration message"

$ alembic upgrade head
```
## Running the application
* make sure Redis is running
* run server

```
python manage.py runserver
```
## Running the tests

* Run the following command

```
coverage run -m pytest
```

## Endpoints

| Endpoints      | description  |
| ------------- |-------------|
| http://127.0.0.1:5000/subscribe| This endpoint allows users to subscribe to the service. |
| http://127.0.0.1:5000/notifications| This is the endpoint that is hit by the Google calendar API. |
| http://127.0.0.1:5000/refresh|This will update the events in Backend database with the ones in the calendar API. |
| http://127.0.0.1:5000/channels|This will create notification channels for the rooms on the database using the room's calender_id. |

# Subscription
* You hit this endpoint with the following body
```
{
"subscriber_info":{
"platform":<The platform you need the notifications in>
"subscription_info": <the url for the notification>
"calendars":<a list of calendars you would like to get notified about>
}
}
```
 * The supported platforms are web, graphql, rest and android.

 * If the platform is android, the subscription_info is the firebase token.
 * If the platform is web, the subscription_info is generated by the web browser. An example is;
 ```
 {
   "endpoint":"https://updates.push.services.mozilla.com/wpush/v2/gAAAAABcdOPnizhcTfbJhEOXH7ZbYrtixdYjYkgMZr4XXfNi6pD0lyNi-qWnGSPnrEzuntkWjZmWXiwkXmtE56rijiBO9jmFek50_B28ESaXNzvauhdFyBBXv2KThItuIjk2j-iDIZro1hMBgOzQEwuNs1pH618tSSLYcwMh4iXJu-UElDw1lZ4",
   "keys":{
      "auth":"_UZRj2dSvv1OGZX33mjrvA",
      "p256dh":"BEogBP0XVGGXLGlCO_E0RwfjNSBA-NQFfm56ArrQ5VqMjHo7HyKr418etfMulDD_KTKG09fPymwTXBfeXZlOtyI"
   }
}
 ```
 * If graphql or rest, the subscription_info should be the url you wish to be notified on sent as a string.
 * For rest ensure that the endpoint accepts post.
 * For graphql ensure the registered endpoint accepts this exact mutation.
 ```
 {
     mutation{
         mrmNotification(calendarId:<recieves calendar id>){
             message
         }
     }
 }
 ```

## Built with
- Python version  3
- Flask
- Grapghql
- Redis
- pywebpush

## Contribution guide
##### Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change. This Project shall be utilizing a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2154921) to track the work done.

 ##### Pull Request Process
- A contributor shall identify a task to be done from the [pivotal tracker](https://www.pivotaltracker.com/n/projects/2154921). If there is a bug, feature or chore that has not to be included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
- The Contributor shall then create a branch off the ` develop` branch where they are expected to undertake the task they have chosen.
- After undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review.
- If there any changes requested, it is expected that these changes shall be effected and the pull request resubmitted for review. Once all the changes are accepted, the pull request shall be closed and the changes merged into `develop` by the owners of this repository.

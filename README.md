# Yes We Bike
We are a group of students from Data Engineering in Universidat Autònoma de Barcelona, this is our dashboard proyect. Our goal is to provide helpful information about the state of Barcelona's public bike service, [Bicing](https://www.bicing.barcelona/).

## Our proyect
We are using [plotly](https://plotly.com/) for our visualizations and the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework for serving our app, thus we follow their convenctions for static and templates folders. `visualizations` contains the scripts for all the real-time visualizations. All the graphs based on our graph of the network are precomputed and stored as `html`s inside the `templates` folder.

For our UI we are using the [Soft UI Dasboard](https://www.creative-tim.com/product/soft-ui-dashboard) based on Bootstrap 4 from Creative Tim.

## Data
In order to get all the needed files you must execute the following command.
```bash
bash fetch_data.sh
```

## How to 
In order to execute correctly this app you will need [Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) installed in your system. Afterwards you should execute the following command on your terminal.
```bash
cd source/docker && docker-compose up
```
This docker-compose will create the app image and get from docker-hub the latest postgres image for the database, insert all required data and start up the app. It is accessible through the port `8000` in your `localhost`.

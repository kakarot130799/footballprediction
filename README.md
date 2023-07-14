# Football Predictor

This investigation aims to analyse the _English Premier League_ and demonstrate how a microservice architecture lets us pull from a range of languages and frameworks to deliver a cohesive solution.

Per focal area, we highlight what we have completed and what is stil TODO.

**Note that these models are for demonstrative purposed only and should not be taken as an indicator of a team's future performance.**

## Modelling
The modelling approach taken is to train a Bayesian linear model p/team, using Turing.jl, based on historic games played, and produce an API which lets us predict the outcome of future games by pitting one team's model against the other. The model takes in information on the match played including their opponent and predicts the number of goals scored by our modelled team.

The guide https://datasciencejuliahackers.com/football-simulation.html provided a helpful resource for conducting a Bayesian analysis of football games.

### TODO
Currently, we only account for the 2021/2022 season, but work is under way to develop a system to incrementally update a model on a season-by-season basis. In other words, if we have a Liverpool baseline model trained up to the 2019/2020 season, we assess to what extent the model requires adjusting based off the 2020/2021 season and make micro adjustments as appropriate by fitting the residual -- saving down a model p/season to allow us to simulate 'dream matches' like 2015/2016 Liverpool vs 2022/2023 Man City.

As we are using Bayesian models, we will also want to produce simulations e.g. average outcome of 5 000 games between Liverpool and Man City, or 1-in-100 game event between Burnley and Spurs.

## Database
### TODO
The data is currently stored in flat files, but will be moved to a PostgreSQL container as part of the deployment/package.

## Frontend
We have a basic Streamlit dashboard container which serves as the frontend.
### TODO
Work is underway to add interactive visualisations via Altair and Plotly. We are also considering a static site offering using e.g. Vue.js or Svelte alongside Plotly.js

## Model API
Models are served using Genie.jl via a POST API in a container. The API accepts the home and away team, looks up the appropriate models, and outputs goals scored by the home team and away team. Trained models are stored in this container.
### TODO
We would want to expand the API to accomodate the given season's team and any simulation criteria. The output will reflect this info and inform the frontend.

## Deployment
We use a Docker Compose set-up to serve a frontend container and an API container.
### TODO
The database container will act as a third, and we may wish to have a separate model object container serving as a 'bucket'.

In addition, we wish to include a guide on how to get this set-up running on a local cluster via Minikube, using Kompose to switch from Docker Compose to services. Further work will explore how to create a Helm chart from this and attempt to run it on EKS.

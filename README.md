# Football Predictor

This investigation aims to analyse the _English Premier League_ and demonstrate how a microservice architecture lets us pull from a range of languages and frameworks to deliver a cohesive solution.

**Note that these models are for demonstrative purposed only and should not be taken as an indicator of a team's future performance.**

## Modelling
The modelling approach taken is to train a Bayesian linear model p/team based on historic games played, and produce an API which lets us predict the outcome of future games by pitting one team's model against the other. The model takes in information on the match played including their opponent and predicts the number of goals scored by our modelled team.

### TODO
Currently, we only account for the 2021/2022 season, but work is under way to develop a system to incrementally update a model on a season-by-season basis. In other words, if we have a Liverpool baseline model trained up to the 2019/2020 season, we assess to what extent the model requires adjusting based off the 2020/2021 season and make micro adjustments as appropriate by fitting the residual -- saving down a model p/season to allow us to simulate 'dream matches' like 2015/2016 Liverpool vs 2022/2023 Man City.

As we are using Bayesian models, we will also want to produce simulations e.g. average outcome of 5 000 games between Liverpool and Man City, or 1-in-100 game event between Burnley and Spurs.

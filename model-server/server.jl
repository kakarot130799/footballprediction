using Genie, Genie.Router, Genie.Requests, Genie.Renderer.Json
using JLD2
using Turing, DataFrames

function prediction(X, chain)
  params = DataFrame(mean(chain))[:, 2]
  poss = params[1]
  sh = params[2]
  sot = params[3]
  dist = params[4]
  fk = params[5]
  pk = params[6]
  venue_code = params[7]
  opp_code = params[8]

  goals = abs.(round.(poss .* X.poss .+ sh .* X.sh .+ sot .* X.sot .+ dist .* X.dist .+ fk .* X.fk .+ pk .* X.pk .+ venue_code .* X.venue_code .+ opp_code .* X.opp_code))

  return goals
end;

fta_ = load_object("model-objects/league_models.jld2");
team_mapping = load_object("model-objects/team_mapping.jld2");

route("/", method = POST) do
  ht = jsonpayload()["home"]
  at = jsonpayload()["away"]

  home_team_ = team_mapping[team_mapping.team .== ht, :index][1]
  away_team_ = team_mapping[team_mapping.team .== at, :index][1]
  home_team_code = team_mapping[team_mapping.team .== ht, :home_code][1]
  away_team_code = team_mapping[team_mapping.team .== at, :home_code][1]
  home_team = fta_[home_team_]
  away_team = fta_[away_team_]
  pred_home = prediction(home_team.sub_league[(home_team.sub_league.opp_code .== away_team_code .&& home_team.sub_league.venue_code .== 0), :], home_team.samples)[1]
  pred_away = prediction(away_team.sub_league[(away_team.sub_league.opp_code .== home_team_code .&& away_team.sub_league.venue_code .== 0), :], away_team.samples)[1]
  json(Dict{String, Int64}("Home Goals"=>pred_home, "Away Goals"=>pred_away))
end

up(7979, "0.0.0.0", async=false)

using Genie, Genie.Router, Genie.Requests, Genie.Renderer.Json
using JLD2
using DataFrames, Turing, StatsBase 

function simulate_matches(team_chain::DataFrame, h::Int64, a::Int64, n_matches::Int64)::DataFrame
  post_home = team_chain.home
  post_att = team_chain[:, r"^att*"]
  post_def = team_chain[:, r"^def*"]

  home::Float64 = mean(Array(post_home[500:end]))
  att₁::Float64 = mean(Array(post_att[500:end, h]))
  att₂::Float64 = mean(Array(post_att[500:end, a]))
  def₁::Float64 = mean(Array(post_def[500:end, h]))
  def₂::Float64 = mean(Array(post_def[500:end, a]))

  logθ₁::Float64 = home + att₁ + def₂
  logθ₂::Float64 = att₂ + def₁

  scores₁::Vector{Int64} = rand(LogPoisson(logθ₁), n_matches)
  scores₂::Vector{Int64} = rand(LogPoisson(logθ₂), n_matches)
  match_status::Vector{Int8} = Vector{Int8}(undef, n_matches)

  for i ∈ 1:n_matches
    if scores₁[i] > scores₂[i]
      match_status[i] = 3
    elseif scores₁[i] < scores₂[i]
      match_status[i] = 0
    else
      match_status[i] = 1
    end
  end
  df::DataFrame = DataFrame(
		 "home_score" => scores₁,
		 "away_score" => scores₂,
		 "match_status" => match_status,
		 )

  return df
end

team_model::DataFrame = load_object("model-objects/league_model.jld2");
team_mapping::Dict{String, Int64} = load_object("model-objects/team_mapping.jld2");

route("/", method = POST) do
  ht = jsonpayload()["home"]
  at = jsonpayload()["away"]

  home_team::Int64 = team_mapping[ht]
  away_team::Int64 = team_mapping[at]

  pred_game::DataFrame = simulate_matches(team_model, home_team, away_team, 1_000_000) 

  json(Dict{String, Int64}("Home Goals"=>pred_game.home_score[1], "Away Goals"=>pred_game.away_score[1]))
end

up(7979, "0.0.0.0", async=false)

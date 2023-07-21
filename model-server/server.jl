using Genie, Genie.Router, Genie.Requests, Genie.Renderer.Json
using JLD2
using DataFrames, Turing, StatsBase 

function simulate_matches(team_chain::DataFrame, h::Int64, a::Int64, n_matches::Int64)::DataFrame
  post_home::Vector = team_chain.home
  post_att::DataFrame = team_chain[:, r"^att*"]
  post_def::DataFrame = team_chain[:, r"^def*"]

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
  ht::String = jsonpayload()["home"]
  at::String = jsonpayload()["away"]
  n::Int64 = 1_000_000

  home_team::Int64 = team_mapping[ht]
  away_team::Int64 = team_mapping[at]

  pred_game::DataFrame = simulate_matches(team_model, home_team, away_team, n) 

  home_score::Int64 = pred_game.home_score[1]
  away_score::Int64 = pred_game.away_score[1]

  home_win_percentage::Float64 = mean(pred_game.match_status .== 3)
  home_draw_percentage::Float64 = mean(pred_game.match_status .== 1)
  home_lose_percentage::Float64 = mean(pred_game.match_status .== 0)
  prob_scoreline::Float64 = mean(pred_game.home_score .== home_score .&& pred_game.away_score .== away_score)



  json(Dict(
	    "Home Goals" => home_score, 
	    "Away Goals" => away_score,
	    "Win" => home_win_percentage,
	    "Draw" => home_draw_percentage,
	    "Lose" => home_lose_percentage,
	    "Prob of Scoreline" => prob_scoreline
	    )
       )
end

up(7979, "0.0.0.0", async=false)

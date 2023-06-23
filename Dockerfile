FROM julia:1.9.1-bullseye
RUN apt-get update && apt-get upgrade -y
WORKDIR notebook/
COPY football.jl football.jl
COPY Project.toml Project.toml
COPY Manifest.toml Manifest.toml
COPY data/cleaned_data.csv data/cleaned_data.csv
EXPOSE 8989
RUN julia --project -e 'using Pkg; Pkg.instantiate();'
CMD julia --project -e 'using Pluto; Pluto.run(; host="0.0.0.0", port=8989)'

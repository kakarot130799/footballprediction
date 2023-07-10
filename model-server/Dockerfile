FROM julia:1.9.2-bullseye
RUN apt-get update && apt-get upgrade -y
WORKDIR server/
COPY . .
EXPOSE 7979
RUN julia --project -e 'using Pkg; Pkg.instantiate();'
CMD julia --project server.jl

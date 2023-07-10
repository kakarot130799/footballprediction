FROM julia:1.9.2-bullseye
RUN apt-get update && apt-get upgrade -y
WORKDIR notebook/
COPY data/cleaned_data.csv data/cleaned_data.csv
COPY . .
EXPOSE 8989
RUN julia --project -e 'using Pkg; Pkg.instantiate();'
CMD julia --project -e 'using Pluto; Pluto.run(; host="0.0.0.0", port=8989)'

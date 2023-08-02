FROM python:3.10-slim
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
WORKDIR dashboard/
COPY app.py app.py
COPY data/ data/
COPY logos/ logos/
EXPOSE 9000
CMD streamlit run app.py --server.port 9000 --server.address '0.0.0.0'

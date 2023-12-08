FROM pytorch/torchserve:latest-cpu

# install dependencies
RUN pip3 install transformers

# copy model artifacts, custom handler and other dependencies
COPY ./handler.py /home/model-server/
COPY ./my_model /home/model-server/
COPY ./bert_dga_classifier.pt /home/model-server/


# create torchserve configuration file
USER root
RUN printf "\nservice_envelope=json" >> /home/model-server/config.properties
RUN printf "\ninference_address=http://0.0.0.0:7080" >> /home/model-server/config.properties
RUN printf "\nmanagement_address=http://0.0.0.0:7081" >> /home/model-server/config.properties
USER model-server

# expose health and prediction listener ports from the image
EXPOSE 7080
EXPOSE 7081


# create model archive file packaging model artifacts and dependencies
RUN torch-model-archiver -f --model-name=model --version=1.0 \
  --model-file=/home/model-server/model.safetensors \
  --serialized-file=/home/model-server/bert_dga_classifier.pt \
  --handler=/home/model-server/handler.py \
  --extra-files "/home/model-server/config.json" \
  --export-path=/home/model-server/model-store


# run Torchserve HTTP serve to respond to prediction requests
CMD ["torchserve", \
     "--start", \
     "--ts-config=/home/model-server/config.properties", \
     "--models", \
     "model=model.mar", \
     "--model-store", \
     "/home/model-server/model-store"]
# deeplab socket api

## server

get [model file](https://drive.google.com/drive/folders/1J20pyswo0PjDZx5g-_ZJXwwbd4qOqR5w) and put it in `server/models/deeplabv3/` to run inference

> python server/serverbatch.py

modify `create_model()` in `server/inference_softmax.py` to change model_path and save_path

## client
> matlab client/client.m

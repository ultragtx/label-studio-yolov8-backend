# YOLOv8 ML backend for the Label Studio

This project contains an ML backend for segmenting and detecting pills in Label Studio. It uses the YOLOv8 model and can segment or detect and classify pills as capsules or tablets.

## Project Structure

### The repository contains the following files and directories:

- **Dockerfile**: The Dockerfile for building the backend container.

- **docker-compose.yml**: The docker-compose file for running the backend.

- **model.py**:  The Python code for the ML backend model for image detection (RectangleLabels).

- **best.pt**: The pre-trained YOLOv8 model for pill classification.

- **requirements.txt**: The list of Python dependencies for the backend.

## Getting Started

Refer to https://github.com/HumanSignal/label-studio-ml-backend/tree/master/label_studio_ml/examples/grounding_dino for additional information.

1. Clone the Label Studio Machine Learning Backend git repository.

2. Paste you Label Studio IP and API key in `model.py`.

3. Update self.labels based on your model.

4. To use this backend, you'll need to have Docker and docker-compose installed. Then, run the following command to start the backend:

   `docker-compose up`


&emsp; &emsp;This will start the backend on localhost:11302.

&emsp; &emsp;Check if it works:

```bash
$ curl http://localhost:11302/health
{"status":"UP"}
```


4. Connect running backend to Label Studio:

   `label-studio start --init new_project --ml-backends http://localhost:11302`

&emsp; &emsp;Or write it manually in Settings - Machine - Add Model.

5. Start the labeling process.

## Training

Model training is **not included** in this project. This will probably be added later.

## Contributing

Contributions to this project are welcome. To contribute, please submit an issue or pull request.

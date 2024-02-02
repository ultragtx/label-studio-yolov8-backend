import os
import random
import requests
import socket
from PIL import Image
from io import BytesIO
import json

from ultralytics import YOLO
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_single_tag_keys, get_local_path


# hostname = socket.gethostname()
# LS_URL = socket.gethostbyname(hostname)
# print("Hostname: ", hostname)
# print("IP Address: ", ip_address)

LS_URL = "http://192.168.10.216:11231"
# LS_URL = "http://127.0.0.1:11231"
LS_API_TOKEN = "c5a6e12f1bc2458b899c061e83ab2feb3970db20"


# Initialize class inhereted from LabelStudioMLBase
class YOLOv8Model(LabelStudioMLBase):
    def __init__(self, project_id, **kwargs):
        # Call base class constructor
        super(YOLOv8Model, self).__init__(project_id, **kwargs)
        # Initialize self variables
        self.labels = ['Bracelets', 'Brooches', 'belt', 'earring', 'maangtika', 'necklace', 'nose ring', 'ring', 'tiara']
        # Load model
        current_script_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_script_directory, "best_det.pt")
        self.model = YOLO(model_path)

    # Function to predict
    def predict(self, tasks, **kwargs):
        """
        Returns the list of predictions based on input list of tasks for 1 image
        """
        task = tasks[0]

        # print('predict')
        # print(json.dumps(task, indent=2) )

        self.from_name, self.to_name, self.value = self.get_first_tag_occurence('RectangleLabels', 'Image')

        # print(self.from_name, self.to_name, self.value)

        # Getting URL of the image
        image_url = task['data'][self.value]
        full_url = LS_URL + image_url
        # print("FULL URL: ", full_url)

        # Header to get request
        header = {
            "Authorization": "Token " + LS_API_TOKEN}

        # Getting URL and loading image
        image = Image.open(BytesIO(requests.get(
            full_url, headers=header).content))
        
        # Height and width of image
        original_width, original_height = image.size

        # Creating list for predictions and variable for scores
        predictions = []
        score = 0
        i = 0

        # Getting prediction using model
        results = self.model.predict(image)

        # Getting mask segments, boxes from model prediction
        for result in results:
            for i, prediction in enumerate(result.boxes):
                xyxy = prediction.xyxy[0].tolist()
                result = {
                    "id": str(i),
                    "from_name": self.from_name,
                    "to_name": self.to_name,
                    "type": "rectanglelabels",
                    "score": prediction.conf.item(),
                    "original_width": original_width,
                    "original_height": original_height,
                    "image_rotation": 0,
                    "value": {
                        "rotation": 0,
                        "x": xyxy[0] / original_width * 100,
                        "y": xyxy[1] / original_height * 100,
                        "width": (xyxy[2] - xyxy[0]) / original_width * 100,
                        "height": (xyxy[3] - xyxy[1]) / original_height * 100,
                        "rectanglelabels": [self.labels[int(prediction.cls.item())]]
                }}
                print(result)
                predictions.append(result)
                score += prediction.conf.item()

        print(f"Prediction Score is {score:.3f}.")

        # Dict with final dicts with predictions
        final_prediction = [{
            "result": predictions,
            "score": score / (i + 1),
            "model_version": "v8n"
        }]

        return final_prediction

    def fit(self, completions, workdir=None, **kwargs):
        """ 
        Dummy function to train model
        """
        return {'random': random.randint(1, 10)}

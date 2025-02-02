import torch
from pydantic import BaseModel
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image


class Detection(BaseModel):
    box: tuple[float, float, float, float]
    label: str


class Detections(BaseModel):
    objects: list[Detection]


class ObjectDetection:
    image_processor: YolosImageProcessor | None = None
    model: YolosForObjectDetection | None = None

    def load_model(self) -> None:
        """Loads the model"""
        model_name = "hustvl/yolos-tiny"
        self.image_processor = YolosImageProcessor.from_pretrained(model_name)
        self.model = YolosForObjectDetection.from_pretrained(model_name)

    def predict(self, image: Image.Image) -> Detections:
        """Runs a prediction"""
        if not self.image_processor or not self.model:
            raise RuntimeError("Model is not loaded")
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs,
                                                                     threshold=0.7,
                                                                     target_sizes=target_sizes)[0]
        objects: list[Detection] = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            if score > 0.7:
                box_values = box.tolist()
                label = self.model.config.id2label[label.item()]
                objects.append(Detection(box=box_values, label=label))
        return Detections(objects=objects)

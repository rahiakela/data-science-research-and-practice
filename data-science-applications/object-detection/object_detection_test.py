from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import YolosImageProcessor, YolosForObjectDetection

# Load an image from the disk using Pillow
root_directory = Path(__file__).parent.parent
picture_path = root_directory/"assets"/"coffee-shop.jpg"
image = Image.open(picture_path)

# Load a pretrained object detection model
model_name = "hustvl/yolos-tiny"
image_processor = YolosImageProcessor.from_pretrained(model_name)
model = YolosForObjectDetection.from_pretrained(model_name)

# Run the model on our image
inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]

# Display the results by drawing rectangles around the detected objects
img_draw = ImageDraw.Draw(image)
font_path = root_directory/"assets"/"OpenSans-ExtraBold.ttf"
font = ImageFont.truetype(str(font_path), 24)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    if score > 0.7:
        box_values = box.tolist()
        label = model.config.id2label[label.item()]
        img_draw.rectangle(box_values, outline="red", width=5)
        img_draw.text(box_values[0:2], label, fill="red", font=font)
image.show()

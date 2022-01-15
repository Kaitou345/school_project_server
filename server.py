import base64
from io import BytesIO
from crypt import methods
from email import message
import json
from flask import Flask, request
from PIL import Image
import cita as ct
from cita import cita
from time import sleep

app = Flask(__name__)


ct.TOLERANCE = 0.5


def __convert_image_to_base64__(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str.decode()

@app.route("/check", methods=["POST"])
def check():
  cita_app = cita()
  resp = {"status": 405, "message": "Bad Request", "data": None }
  img = request.files.get("img_to_check")
  if not img:
    return json.dumps(resp)

  pil_img = Image.open(img)
  info = cita_app.check_entry(pil_img)

  if not info:
    resp["status"] = 404
    resp["message"] = "Not found"
    return json.dumps(resp)

  else:  
    image = info["image"]

    info["image"] = __convert_image_to_base64__(image)
    resp["status"] = 200
    resp["message"] = "Found"
    resp["data"] = info

  return json.dumps(resp)


@app.route("/register", methods=["POST"])
def register():
  return "Hello"


if __name__ == "__main__":
  app.run('0.0.0.0', 3000, debug=True)
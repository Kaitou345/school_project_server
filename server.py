import base64
from io import BytesIO
import json
from flask import Flask, request
from PIL import Image
import cita as ct
from cita import cita

app = Flask(__name__)


ct.TOLERANCE = 0.45


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
  cita_app = cita()
  resp = {"status": 405, "message": "Bad Request", "data": None }

  img1 = request.files.get("img1")
  img2 = request.files.get("img2")

  images = [Image.open(img1), Image.open(img2)]
  
  if not (img1 and img2):
    return json.dumps(resp)

  name = request.form.get("name")
  age = request.form.get("age")
  number = request.form.get("contact_number")
  email = request.form.get("email")
  address = request.form.get("email")


  if not (name and age and number, email, address):
    return json.dumps(resp)

  cita_app.register_entry(images, name, email, address, number, age)
  resp["status"] = 200
  resp["message"] = "Successfully registered"

  return json.dumps(resp)


@app.route("/delete", methods=["POST"])
def delete():
  cita_app = cita()
  resp = {"status": 405, "message": "Bad Request", "data": None }

  id = request.form.get("id")

  if not id:
    return json.dumps(resp)

  cita_app.delete_entry(id)

  resp["status"] = 200
  resp["message"] = "Successfully deleted"

  return json.dumps(resp)






if __name__ == "__main__":
  app.run('0.0.0.0', 3000, debug=True)
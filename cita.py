from genericpath import exists
from PIL import Image
from face_recognition.api import face_encodings
import numpy as np
import face_recognition
from numpy.lib.type_check import imag
import db
import os

MODEL = "hog"
TOLERANCE = 0.5
UPSAMPLE = 1
NUM_JITTERS = 5

def __convert_into_numpy_images__(pil_images):
  images = []

  for pil_image in pil_images:
    images.append(__get_encoding_of_pil_image__(pil_image))
  
  return images




def __get_encoding_of_pil_image__(pil_image):
  np_img = np.asarray(pil_image)
  location = face_recognition.face_locations(np_img, UPSAMPLE,MODEL)[0]
  return face_recognition.face_encodings(np_img, [location,],NUM_JITTERS, "large")[0]


def __compare_encodings__(encodings, encoding_to_compare):
  results = face_recognition.compare_faces(encodings, encoding_to_compare, tolerance=TOLERANCE)

  return any(results)

  

class cita:
  def __init__(self, ):
    self.person_db = db.person_db("db.db")
    self.encoding_db = db.encoding_db("db.db")
    self.images_path = "registered_images/"

    if not exists(self.images_path):
      os.mkdir(self.images_path)

  def register_entry(self, pil_images, name, email="Not Available", address="Not Available", contact_number="Not Available", age=0):

    # TODO save images in local storage

      

    uuid = self.person_db.insert_person(name, email, address, contact_number, age)


    path = f"{self.images_path}{uuid}"
    if not exists(path):
      os.mkdir(path)


    counter = 0

    for image in pil_images:
      image.save(f"{path}/{counter}.jpg")
      counter += 1


    numpy_images = __convert_into_numpy_images__(pil_images)
    self.encoding_db.insert_encodings(uuid, numpy_images)


  def check_entry(self, pil_image):

    ids = self.person_db.get_ids()

    image_to_compare = __get_encoding_of_pil_image__(pil_image)

    for id in ids:
      encodings =  self.encoding_db.get_encodings(id)

      if __compare_encodings__(encodings, image_to_compare):
        info = self.person_db.get_info(id)

        path = f"{self.images_path}{id}/"
        img_name = os.listdir(path)[0]

        info["image"] = Image.open(f"{path}{img_name}")

        return info


  def delete_entry(self, id):

    # TODO delete images from local storage

    self.encoding_db.delete_person(id)
    self.person_db.delete_person(id)


  def get_profiles(self):
    
    profiles = self.person_db.get_all_info()

    for profile in profiles:
      id = profile["id"]
      path = f"{self.images_path}{id}/"
      img_name = os.listdir(path)[0]
      profile["image"] = Image.open(f"{path}{img_name}")

    return profiles


  def get_image(self,id):
    """
    Get corresponding image for the ID as PIL Image
    """

  def __del__(self):
    self.encoding_db.disconnect()
    self.person_db.disconnect()



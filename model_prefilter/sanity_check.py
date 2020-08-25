import requests
from io import BytesIO
import base64
import json
from inference import Prefilter

medical_imgs = [
    "https://media.sciencephoto.com/image/c0371577/800wm/C0371577-Stroke,_MRI_brain_scan.jpg",
    "https://prod-images-static.radiopaedia.org/images/34839897/e0bfac31c00d077d18aca7ab33b495_gallery.jpeg",
    "https://prod-images-static.radiopaedia.org/images/157210/332aa0c67cb2e035e372c7cb3ceca2_jumbo.jpg",
    "https://www.mqmi.com.au/wp-content/uploads/2019/10/CT-CORONARY-ANGIOGRAM-Severe-1.jpg",
    "http://www.medicalradiation.com/wp-content/uploads/fluoroscopy.jpg",
    "https://image.freepik.com/photos-gratuite/technologie-rayon-chirurgie-x-ray-xray_1172-444.jpg",
    "https://prod-images-static.radiopaedia.org/images/51665621/badcab5dfbb1423245a3343156b347_big_gallery.jpeg",
]

nonmedical_imgs = [
    "https://i.pinimg.com/originals/e0/3d/5b/e03d5b812b2734826f76960eca5b5541.jpg",
    "https://i.pinimg.com/originals/82/61/79/826179defbbdbc3ec7fdc37e15ea6bab.jpg",
    "https://www.lifesavvy.com/thumbcache/0/0/31c7385df31261da25272193d5226120/p/uploads/2019/05/daf3eeae-3.jpg",
    "https://acumass.com/wp-content/uploads/2016/02/selfie-pay.jpeg",
]


prefilter = Prefilter()
requests_session = requests.Session()
server = "http://127.0.0.1:8000/prefilter"


print("Medical")
for medical_img in medical_imgs:
    response = requests.get(medical_img)
    img = BytesIO(response.content).getvalue()
    encoded_string = base64.b64encode(img).decode()

    data = prefilter.ask(encoded_string)
    print(data)

print("Nonmedical")
for non_medical_img in nonmedical_imgs:
    response = requests.get(non_medical_img)
    img = BytesIO(response.content).getvalue()
    encoded_string = base64.b64encode(img).decode()

    data = prefilter.ask(encoded_string)
    print(data)

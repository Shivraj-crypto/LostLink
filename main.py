import shutil
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Texture
from kivymd.app import MDApp
from tkinter import filedialog
import cv2
import face_recognition
import numpy as np
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from google.oauth2 import service_account
from google.oauth2 import service_account
from google.cloud import storage
from kivy.uix.filechooser import FileChooserIconView
import webbrowser
import requests

# databse code
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "capstone-project-5cd4a-firebase-adminsdk-rcagk-2dafde0ec0 (1).json"
credentials = service_account.Credentials.from_service_account_file(
    "capstone-project-5cd4a-firebase-adminsdk-rcagk-2dafde0ec0 (1).json")
client = storage.Client(credentials=credentials)
client = storage.Client()
bucket = client.get_bucket('capstone-project-5cd4a.appspot.com')


Window.size = (300, 500)

file_path = ''
file_new_path = ''


class PageOne(Screen):

    def hello_on(self):
        self.ids.my_image31.source = './Camera Roll./Untitled-21.png'

    def hello_off(self):
        self.ids.my_image31.source = './Camera Roll./Untitled-19  .png'

    def hello_on2(self):
        self.ids.my_image32.source = './Camera Roll./Untitled-23.png'

    def hello_off2(self):
        self.ids.my_image32.source = './Camera Roll./Untitled-20.png'

    def reset_img(self):
        global file_path
        file_path = ''
        self.ids.my3.source = file_path

    def open_phone_url(self):
        webbrowser.open_new("https://indianhelpline.com/")

    def on_enter(self):
        self.FaceRecoginiton()

    def FaceRecoginiton(self):
        image_dir = "Camera Roll/database"
        local_dir = "Camera Roll/database"
        information2 = "Camera Roll/information"
        local_dir2 = "Camera Roll/information"

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        if not os.path.exists(local_dir2):
            os.makedirs(local_dir2)

        global file_path
        global file_new_path
        bool_value = False

        for blob in bucket.list_blobs(prefix=image_dir):
            if blob.name.endswith('.jpg'):
                file_name = os.path.join(
                    local_dir, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

            if blob.name.endswith('.png'):
                file_name = os.path.join(
                    local_dir, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

        for blob in bucket.list_blobs(prefix=information2):
            if blob.name.endswith('.txt'):
                file_name = os.path.join(
                    local_dir2, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

        file_path = filedialog.askopenfilename()
        self.ids.my3.source = file_path
        given_image = cv2.imread(file_path)
        given_image = cv2.cvtColor(given_image, cv2.COLOR_BGR2RGB)
        given_face_locations = face_recognition.face_locations(given_image)
        given_face_encodings = face_recognition.face_encodings(
            given_image, given_face_locations)
        image_dir = './Camera Roll./database'
        database_images = os.listdir(image_dir)
        matching_image_names = []
        matching_image_locations = []

        for database_image in database_images:
            image = cv2.imread(os.path.join(image_dir, database_image))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(
                image, face_locations)
            if given_face_encodings and face_encodings:
                results = face_recognition.compare_faces(
                    face_encodings, given_face_encodings[0])
                # Print the results
                print("face matched")
                for i, result in enumerate(results):
                    if result:
                        bool_value = True
                        matching_image_names.append(database_image)
                        matching_image_locations.append(
                            os.path.join(image_dir, database_image))
            else:
                print("face not matched")

        if bool_value:
            for i, image_location in enumerate(matching_image_locations):
                self.ids.my2.source = image_location
            img = cv2.imread(file_path)
            file_name = os.path.basename(file_path)
            face_cascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                img, scaleFactor=1.3, minNeighbors=3)
            for i, (x, y, w, h) in enumerate(faces):
                crop_img = img[y-50:y + h+50, x-50:x + w+50]
                file_new_path = './Camera Roll./Trash./' + file_name
                cv2.imwrite(file_new_path, crop_img)
                print(file_new_path)
            self.ids.my3.source = file_new_path

            new_path = image_location.replace("database", "information")
            final_path = os.path.splitext(new_path)[0] + ".txt"
            # print(final_path)
            with open(final_path, 'r') as f:
                file_contents = f.read()
            self.ids.ml2.text = file_contents
        else:
            img = cv2.imread(file_path)
            file_name = os.path.basename(file_path)
            face_cascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                img, scaleFactor=1.3, minNeighbors=3)
            for i, (x, y, w, h) in enumerate(faces):
                crop_img = img[y - 50:y + h + 50, x - 50:x + w + 50]
                file_path = './Camera Roll./Trash./' + file_name
                cv2.imwrite(file_path, crop_img)
                print(file_path)
            self.manager.current = 'PageFour'


class PageTwo(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.web_cam = self.ids.web_cam
        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, *args):
        ret, self.frame = self.capture.read()
        if ret:  # Check if the frame was successfully read
            self.frame = self.frame[0:1500, 340:1500]
            buf = cv2.flip(self.frame, 0).tostring()
            texture = Texture.create(
                size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.web_cam.texture = texture
        else:
            print("Failed to capture a frame from the webcam.")

    def GetImage(self):
        self.file_name = 'input_image.jpg'
        img = cv2.imwrite(self.file_name, self.frame)

    def GetImagePath(self):
        self.file_path = os.path.join(os.getcwd()) + '\\' + self.file_name

    def Change_Res(self, width, height):
        self.capture.set(3, width)
        self.capture.set(4, height)


class PageThree(Screen):
    def hello_on(self):
        self.ids.my_image41.source = './Camera Roll./Untitled-21.png'

    def hello_off(self):
        self.ids.my_image41.source = './Camera Roll./Untitled-19  .png'

    def hello_on2(self):
        self.ids.my_image42.source = './Camera Roll./Untitled-23.png'

    def hello_off2(self):
        self.ids.my_image42.source = './Camera Roll./Untitled-20.png'

    def reset_img(self):
        global file_path
        file_path = ''
        self.ids.mye3.source = file_path

    def open_phone_url(self):
        webbrowser.open_new("https://indianhelpline.com/")

    def on_enter(self):
        self.MakePrediction()

    def MakePrediction(self):
        image_dir = "Camera Roll/database"
        local_dir = "Camera Roll/database"
        information2 = "Camera Roll/information"
        local_dir2 = "Camera Roll/information"

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        if not os.path.exists(local_dir2):
            os.makedirs(local_dir2)

        global file_path
        global file_new_path
        bool_value = False

        for blob in bucket.list_blobs(prefix=image_dir):
            if blob.name.endswith('.jpg'):
                file_name = os.path.join(
                    local_dir, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

            if blob.name.endswith('.png'):
                file_name = os.path.join(
                    local_dir, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

        for blob in bucket.list_blobs(prefix=information2):
            if blob.name.endswith('.txt'):
                file_name = os.path.join(
                    local_dir2, os.path.basename(blob.name))
                blob.download_to_filename(file_name)

        file_path = './input_image.jpg'
        self.ids.mye3.source = file_path
        given_image = cv2.imread(file_path)
        given_image = cv2.cvtColor(given_image, cv2.COLOR_BGR2RGB)
        given_face_locations = face_recognition.face_locations(given_image)
        given_face_encodings = face_recognition.face_encodings(
            given_image, given_face_locations)
        image_dir = './Camera Roll./database'
        database_images = os.listdir(image_dir)
        matching_image_names = []
        matching_image_locations = []

        for database_image in database_images:
            image = cv2.imread(os.path.join(image_dir, database_image))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(
                image, face_locations)
            if given_face_encodings and face_encodings:
                results = face_recognition.compare_faces(
                    face_encodings, given_face_encodings[0])
                # Print the results
                print("face matched")
                for i, result in enumerate(results):
                    if result:
                        bool_value = True
                        matching_image_names.append(database_image)
                        matching_image_locations.append(
                            os.path.join(image_dir, database_image))
            else:
                print("face not matched")

        if bool_value:
            for i, image_location in enumerate(matching_image_locations):
                self.ids.mye2.source = image_location
            img = cv2.imread(file_path)
            file_name = os.path.basename(file_path)
            face_cascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                img, scaleFactor=1.3, minNeighbors=3)
            for i, (x, y, w, h) in enumerate(faces):
                crop_img = img[y-50:y + h+50, x-50:x + w+50]
                file_new_path = './Camera Roll./Trash./' + file_name
                cv2.imwrite(file_new_path, crop_img)
                print(file_new_path)
            self.ids.mye3.source = file_new_path

            new_path = image_location.replace("database", "information")
            final_path = os.path.splitext(new_path)[0] + ".txt"
            # print(final_path)
            with open(final_path, 'r') as f:
                file_contents = f.read()
            self.ids.mle2.text = file_contents
        else:
            img = cv2.imread(file_path)
            file_name = os.path.basename(file_path)
            face_cascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                img, scaleFactor=1.3, minNeighbors=3)
            for i, (x, y, w, h) in enumerate(faces):
                crop_img = img[y - 50:y + h + 50, x - 50:x + w + 50]
                file_path = './Camera Roll./Trash./' + file_name
                cv2.imwrite(file_path, crop_img)
                print(file_path)
            self.manager.current = 'NotFoundPageScan'


class PageFour(Screen):

    def hello_on(self):
        self.ids.my_image2.source = './Camera Roll./Untitled-22.png'

    def hello_off(self):
        self.ids.my_image2.source = './Camera Roll./Untitled-16.png'

    def hello_on2(self):
        self.ids.my_image3.source = './Camera Roll./Untitled-23.png'

    def hello_off2(self):
        self.ids.my_image3.source = './Camera Roll./Untitled-20.png'

    def on_enter(self):
        global file_new_path
        print(file_path + "Hello")
        self.ids.my31.source = file_path


class NotFoundPageScan(Screen):
    def hello_on(self):
        self.ids.nfps2.source = './Camera Roll./Untitled-22.png'

    def hello_off(self):
        self.ids.nfps2.source = './Camera Roll./Untitled-16.png'

    def hello_on2(self):
        self.ids.nfps3.source = './Camera Roll./Untitled-23.png'

    def hello_off2(self):
        self.ids.nfps3.source = './Camera Roll./Untitled-20.png'

    def on_enter(self):
        global file_new_path
        print(file_path + "Hello")
        self.ids.nfps1.source = file_path


class LoginPage(Screen):
    pass


class RegisterPage(Screen):
    pass


class EnterLostChildDetails(Screen):
    new_path = None

    def __init__(self, **kwargs):
        super(EnterLostChildDetails, self).__init__(**kwargs)
        self.filechooser = FileChooserIconView()
        self.filechooser.bind(on_submit=self.on_file_select)
        self.popup = Popup(title="Choose file",
                           content=self.filechooser, size_hint=(0.9, 0.9))
        self.filechooser.bind(on_submit=self.on_file_select)

    def show_file_chooser(self, *args):
        self.filechooser.path = '/'
        self.filechooser.filters = ['*.jpg', '*.jpeg', '*.png']
        self.filechooser.show_hidden = True
        self.filechooser.choose_dir = False
        self.popup.open()

    def on_file_select(self, *args):
        global new_path
        image_path = args[1][0]
        self.ids.Pg3im1.source = image_path
        self.popup.dismiss()
        destination_dir = "./Camera Roll./NewInfo./"

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Copy the selected file to the destination directory
        new_path = shutil.copy(image_path, destination_dir)
        new_path = shutil.copy(image_path, "./Camera Roll./NewInfo./")

    def pff_change(self):
        self.show_file_chooser()

    def save_data(self, instance):
        global new_path

        name = self.ids.name_input.text
        age = self.ids.age_input.text
        date = self.ids.date_input.text
        mobile_no = self.ids.mobile_input.text
        address = self.ids.address_input.text
        filename = os.path.basename(new_path)
        file_extension = os.path.splitext(filename)[1]
        new_path1 = new_path.replace(filename, name)
        dir_path = "Camera Roll/NewInfo/"
        old_name = filename
        new_name = os.path.splitext(name)[0]
        new_name = new_name + file_extension
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        file_name = "Camera Roll/NewInfo/" + name + ".txt"
        file_name_2 = name + ".txt"
        New2 = os.path.basename(new_path)
        print(New2)
        print(new_path)
        print(file_name)

        with open(file_name, "w") as f:
            f.write(f"Name: {name}\n")
            f.write(f"Age: {age}\n")
            f.write(f"Missing Since Date: {date}\n")
            f.write(f"Guardian's mobile no: {mobile_no}\n")
            f.write(f"Address: {address}\n")

        new_dir_img = "Camera Roll/database/" + New2
        new_dir_txt = "Camera Roll/information/" + file_name_2

        local_file_path = new_path
        remote_file_path = new_dir_img
        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)
        print(blob.public_url)

        local_file_path2 = file_name
        remote_file_path2 = new_dir_txt
        blob = bucket.blob(remote_file_path2)
        blob.upload_from_filename(local_file_path2)
        print(blob.public_url)


class Demo(Screen):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

    def hello_on(self):
        self.ids.my_image.source = './Camera Roll./Untitled-6.png'

    def hello_off(self):
        self.ids.my_image.source = './Camera Roll./Untitled-3.png'

    def hello_on2(self):
        self.ids.my_image2.source = './Camera Roll./Untitled-5.png'

    def hello_off2(self):
        self.ids.my_image2.source = './Camera Roll./Untitled-4.png'

    def NearestPoliceStation(self):
        webbrowser.open_new(
            "https://goo.gl/maps/hG7ntU32THuPHVPk9?coh=178573&entry=tt")

    def NearestHospital(self):
        webbrowser.open_new("https://indianhelpline.com/")

    def EmergencyCall(self):
        webbrowser.open_new("https://indianhelpline.com/")


class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file("My.kv")
        screen = ScreenManager(transition=FadeTransition())
        screen.add_widget(Demo(name='Demo'))
        screen.add_widget(PageOne(name='PageOne'))
        screen.add_widget(PageTwo(name='PageTwo'))
        screen.add_widget(PageThree(name='PageThree'))
        screen.add_widget(PageFour(name='PageFour'))
        screen.add_widget(LoginPage(name='LoginPage'))
        screen.add_widget(RegisterPage(name='RegisterPage'))
        screen.add_widget(NotFoundPageScan(name='NotFoundPageScan'))
        screen.add_widget(EnterLostChildDetails(name='EnterLostChildDetails'))
        return screen


Main().run()

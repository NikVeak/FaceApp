import datetime
import os.path
from time import sleep
from tkinter import messagebox
import cv2
import tkinter as tk
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self, window, window_title):
        self.btn_exit = None
        self.btn_capture = None
        self.right_frame = None
        self.root = window
        # self.folder_images = "photos" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        # os.mkdir(self.folder_images)
        self.images_index = 0
        self.window = window
        self.window.title(window_title)
        self.create_menu()

        # --------------------------------------
        self.video_source = 0  # Используйте 0 для встроенной камеры, или укажите путь к видеофайлу

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # ----------------------------------------
        self.label_find_face = tk.Label(text="Распознано: 0", font=11)
        self.label_find_face.pack(anchor=tk.CENTER, expand=True)

        self.delay = 10
        self.capture_face = False
        self.update()
        self.window.mainloop()

    def validate_input(self,*args):
        # Проверка введенных символов
        value = self.entry.get()
        if value and not value.isdigit():
            messagebox.showerror("Ошибка", "Пожалуйста, введите только числа.")
            self.entry.delete(0, tk.END)

    def on_arrow_up(self,event):
        # Увеличение значения при нажатии клавиши вверх
        current_value = self.entry.get()
        if current_value.isdigit():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(int(current_value) + 1))

    def on_arrow_down(self,event):
        # Уменьшение значения при нажатии клавиши вниз
        current_value = self.entry.get()
        if current_value.isdigit():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(int(current_value) - 1))
    def create_menu(self):
        self.right_frame = tk.Frame(self.window)
        self.btn_capture = tk.Button(self.right_frame, text="Начать",
                                     command=self.toggle_capture,
                                     fg="white", bd=2, bg="#09794c",
                                     relief=tk.RAISED, borderwidth='0')
        self.btn_capture.pack(pady=10,expand=True)

        self.btn_exit = tk.Button(self.right_frame, text="Выход", command=self.exit,
                                  fg="black", bd=2, bg="#b4b6de",
                                  borderwidth='0')
        self.btn_exit.pack(pady=10, expand=True)

        self.expandable_frame = tk.Frame(self.right_frame)
        self.label_expandable = tk.Label(self.expandable_frame, text="Параметры")
        self.label_expandable.pack(pady=10)
        self.entry = tk.Entry(self.expandable_frame, validate="key")
        # Устанавливаем обработчики событий для проверки введенных символов и для клавиш со стрелками
        self.entry.bind('<Key>', self.validate_input)
        self.entry.bind('<Up>', self.on_arrow_up)
        self.entry.bind('<Down>', self.on_arrow_down)
        self.entry.pack()

        self.btn_toggle = tk.Button(self.right_frame, text="Настройки",
                                    command=self.toggle_visibility)
        self.btn_toggle.pack(pady=10, expand=True)


        self.right_frame.pack(side="right")

    def toggle_visibility(self):
        if self.expandable_frame.winfo_ismapped():
            self.expandable_frame.pack_forget()
        else:
            self.expandable_frame.pack()

    def exit(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из приложения?"):
            self.root.destroy()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            if self.capture_face:
                self.detect_and_capture_faces(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def toggle_capture(self):
        self.btn_capture.config(text="Остановить", bg="#790916")
        self.capture_face = not self.capture_face

        if not self.capture_face:
            self.images_index = 0
            self.btn_capture.config(text="Начать", bg="#09794c")

    def detect_and_capture_faces(self, frame):
        # Используем каскадный классификатор для обнаружения лица
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print("Лица не обнаружены")
        else:
            print("Обнаружено лиц:", len(faces))
            self.images_index += 1
            self.label_find_face.config(text="Распознано: " + str(self.images_index))

        # Перебираем обнаруженные лица и выделяем их на изображении
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Сохраняем фотографию лица
            face_img = frame[y:y + h, x:x + w]

            name_photo = f"{self.folder_images}/captured_face" + str(
                datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + ".jpg"
            print(name_photo)
            full_path = os.path.join(os.path.expanduser("~"), "Images", name_photo)
            print(full_path)

            # face_img.save(name_photo)
            # cv2.imshow("Images",face_img)
            # cv2.waitKey(0)  # Ждем, пока пользователь не нажмет клавишу
            # sleep(5)
            is_written = cv2.imwrite(name_photo,
                                     face_img)
            if not is_written:
                print("Error save !")
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def preload_window():
    # Создаем окно предзагрузки
    preload = tk.Tk()
    preload.title("Окно предзагрузки")

    # Добавляем текст или индикатор загрузки
    label = tk.Label(preload, text="Пожалуйста, подождите, идет загрузка...")
    label.pack(padx=20, pady=20)

    # Отображаем окно предзагрузки
    preload.update()

    # Это имитация загрузки. Здесь вы можете добавить вашу реальную логику предзагрузки,
    # например, загрузку ресурсов или выполнение каких-то операций.
    # Представим, что загрузка занимает 3 секунды
    sleep(3)

    # Закрываем окно предзагрузки
    preload.destroy()

def main():
    preload_window()
    # Создаем окно приложения
    root = tk.Tk()
    app = CameraApp(root, "Распознование лица")
    root.mainloop()


if __name__ == "__main__":
    main()

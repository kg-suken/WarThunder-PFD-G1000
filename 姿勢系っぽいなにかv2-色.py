import tkinter as tk
from PIL import Image, ImageTk
import math
from WarThunder import telemetry

class GyroscopeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gyroscope App")

        self.canvas = tk.Canvas(root, width=500, height=400, bg='white')
        self.canvas.pack()

        self.roll_label = tk.Label(root, text="Roll: 0 degrees")
        self.roll_label.pack()

        self.telem = telemetry.TelemInterface()

        # 地平線画像を読み込む
        self.horizon_image = Image.open("地平線.png")

        # 画像を回転して事前に生成
        self.rotated_horizon = self.horizon_image.rotate(0)
        self.horizon_photo = ImageTk.PhotoImage(self.rotated_horizon)

        # 別の画像を読み込んで50x50に縮小
        self.center_image = Image.open("飛行機.png")
        self.center_image = self.center_image.resize((50, 50))
        self.center_photo = ImageTk.PhotoImage(self.center_image)

        self.headingIcon_image = Image.open("HeadingIcon.png")
        self.headingIcon_image = self.headingIcon_image.resize((30, 30))
        self.headingIcon_photo = ImageTk.PhotoImage(self.headingIcon_image)

        self.pitch_image = Image.open("ピッチ角-v2.png")
        self.pitch_image = self.pitch_image.resize((250, 900))

        # 画像を回転して事前に生成
        self.rotated_pitch = self.pitch_image.rotate(0)
        self.pitch_photo = ImageTk.PhotoImage(self.rotated_pitch)

        # 方位画像を読み込む（適切なファイル名に変更してください）
        self.heading_image = Image.open("方位.png")
        self.heading_image = self.heading_image.resize((100, 100))

        # 画像を回転して事前に生成
        self.rotated_heading = self.heading_image.rotate(0)
        self.heading_photo = ImageTk.PhotoImage(self.rotated_heading)

        # Canvasサイズをキャッシュ
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.root.after(0, self.update_gyroscope)
        self.root.bind('<Key>', self.on_key_press)

    def update_gyroscope(self):
        if self.telem.get_telemetry():
            roll = self.telem.basic_telemetry.get('roll', 0)
            altitude = self.telem.basic_telemetry.get('altitude', 0)
            ias = self.telem.basic_telemetry.get('IAS', 0)
            pitch = self.telem.basic_telemetry.get('pitch', 0)
            heading = self.telem.basic_telemetry.get('heading', 0)

            self.draw_gyroscope(roll, altitude, ias)
            self.draw_pitch_indicator(-pitch, roll)
            self.draw_heading_indicator(heading)

            self.roll_label.config(text=f"Roll: {int(roll)} degrees")

        self.root.after(1, self.update_gyroscope)

    def draw_gyroscope(self, roll, altitude, ias):
        self.canvas.delete("all")

        roll_angle = math.radians(roll)
        line_length = min(self.canvas.winfo_width(), self.canvas.winfo_height()) - 20

        x_center = self.canvas.winfo_width() // 2
        y_center = self.canvas.winfo_height() // 2

        # 回転した地平線画像を表示
        self.rotated_horizon = self.horizon_image.rotate(roll)
        self.horizon_photo = ImageTk.PhotoImage(self.rotated_horizon)
        self.canvas.create_image(x_center, y_center, image=self.horizon_photo)

        # 別の画像の右側にaltitudeの数字を表示
        altitude_text = f"{int(altitude)} m"
        self.canvas.create_rectangle(x_center + 160, y_center - 15, x_center + 240, y_center + 15, fill='black')
        self.canvas.create_text(x_center + 160, y_center, text=altitude_text, anchor='w', font=('Arial', 12, 'bold'), fill='white')

        ias_text = f"{int(ias)} km/h"
        self.canvas.create_rectangle(x_center - 240, y_center - 15, x_center - 160, y_center + 15, fill='black')
        self.canvas.create_text(x_center - 160, y_center, text=ias_text, anchor='e', font=('Arial', 12, 'bold'), fill='white')

    def draw_pitch_indicator(self, pitch, roll):
        # Canvas上のピッチ角度に基づいて画像の位置を計算
        x_center = self.canvas.winfo_width() // 2
        y_center = self.canvas.winfo_height() // 2
        pitch_offset = int((pitch) * (-4.5))

        # ピッチ角の画像を表示
        self.rotated_pitch = self.pitch_image.rotate(roll, center=(250 / 2,450 + (pitch * 4)))
        self.pitch_photo = ImageTk.PhotoImage(self.rotated_pitch)
        self.canvas.create_image(x_center, y_center + pitch_offset, image=self.pitch_photo)

    def draw_heading_indicator(self, heading):
        x_center = self.canvas.winfo_width() // 2
        y_center = self.canvas.winfo_height() // 2

        # 画面下部に方位画像を描画
        rotated_heading = self.heading_image.rotate(heading)
        self.rotated_heading = rotated_heading
        self.heading_photo = ImageTk.PhotoImage(rotated_heading)
        self.canvas.create_image(x_center + 180, y_center + 100, image=self.heading_photo)
        self.canvas.create_image(x_center + 180, y_center + 100, image=self.headingIcon_photo)


        # 画面中央に縮小した別の画像を描画
        self.canvas.create_image(x_center, y_center, image=self.center_photo)

    def on_key_press(self, event):
        if event.char == 'q':
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = GyroscopeApp(root)
    root.mainloop()

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
from tkinter import messagebox

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DU LỊCH NHA TRANG")

        self.selected_image_index = 0
        self.selected_image_path = None

        # Load large image
        large_image_path = "./assets/nha-trang.jpg"
        self.large_image = Image.open(large_image_path)

        # Split large image into 8 sections
        self.small_images = self.split_large_image(self.large_image)

        image_frame = tk.Frame(root, bg="#f2f2f2")
        image_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.original_images = [ImageTk.PhotoImage(image.resize((100, 100))) for image in self.small_images]

        row, col = 0, 0
        for index, image in enumerate(self.original_images, start=1):
            label = tk.Label(image_frame, image=image, borderwidth=1, relief="solid")
            label.grid(row=row, column=col, padx=5, pady=5)

            number_label = tk.Label(image_frame, text=str(index), font=("Helvetica", 13), bg="#4CAF50", fg="white")
            number_label.grid(row=row, column=col, sticky="ne", padx=5, pady=5)

            number_label.bind("<Button-1>", lambda event, index=index: self.on_number_click(index))

            col += 1
            if col > 3:
                col = 0
                row += 1

        function_frame = tk.Frame(root, bg="#e6e6e6")
        function_frame.grid(row=row + 1, column=0, pady=10, columnspan=4)

        self.result_label = tk.Label(function_frame, text="Kết quả in ra", font=("Helvetica", 12), bg="#e6e6e6")
        self.result_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.selected_location_label = tk.Label(function_frame, text="Vui lòng chọn một địa điểm!", font=("Helvetica", 10), bg="#e6e6e6")
        self.selected_location_label.grid(row=1, column=0, pady=5, columnspan=4)

        self.parameters_label = tk.Label(function_frame, text="Địa điểm du lich được chọn là: ", font=("Helvetica", 10), bg="#e6e6e6")
        self.parameters_label.grid(row=2, column=0, pady=5, columnspan=4)

        numbers_frame = tk.Frame(function_frame, bg="#e6e6e6")
        numbers_frame.grid(row=3, column=0, pady=5, columnspan=4)

        self.number_labels = []
        for i in range(1, 9):
            number_label = tk.Label(numbers_frame, text=str(i), font=("Helvetica", 10), bg="#4CAF50", fg="white", padx=10, pady=5)
            number_label.grid(row=0, column=i - 1, padx=5)
            number_label.bind("<Button-1>", lambda event, index=i: self.on_number_click(index))
            self.number_labels.append(number_label)

        self.contrast_stretching_button = tk.Label(function_frame, text="Contrast Stretching", font=("Helvetica", 10), bg="#e6e6e6")
        self.contrast_stretching_button.grid(row=4, column=0, pady=5)
        self.contrast_stretching_button = tk.Button(function_frame, text="Apply Contrast Stretching", command=self.apply_contrast_stretching,
                                          font=("Helvetica", 10), bg="#4CAF50", fg="white")
        self.contrast_stretching_button.grid(row=4, column=2, pady=5)

        self.dilation_label = tk.Label(function_frame, text="Dilation (iterations)", font=("Helvetica", 10), bg="#e6e6e6")
        self.dilation_label.grid(row=5, column=0, pady=5)
        self.dilation_entry = tk.Entry(function_frame, font=("Helvetica", 10))
        self.dilation_entry.grid(row=5, column=1, pady=5)
        self.dilation_button = tk.Button(function_frame, text="Apply Dilation", command=self.apply_dilation,
                                          font=("Helvetica", 10), bg="#4CAF50", fg="white")
        self.dilation_button.grid(row=5, column=2, pady=5)

        self.reset_button = tk.Button(function_frame, text="Reset", command=self.reset_image, font=("Helvetica", 10),
                                      bg="#f44336", fg="white")
        self.reset_button.grid(row=6, column=0, pady=5, columnspan=4)

    def on_number_click(self, index):
        print(f"Nhấp vào số {index}, mở ảnh: {index}")

        self.selected_image_index = index

        selected_image = self.small_images[index - 1]
        selected_image = selected_image.resize((100, 100))
        selected_image = ImageTk.PhotoImage(selected_image)
        self.selected_location_label.config(image=selected_image)
        self.selected_location_label.image = selected_image

        parameters_text = f"Địa điểm du lich được chọn với số {index}"
        self.parameters_label.config(text=parameters_text)

        for i, label in enumerate(self.number_labels):
            if i + 1 == index:
                label.config(bg="#FFD700", fg="#000000", relief="solid")
            else:
                label.config(bg="#4CAF50", fg="white", relief="flat")

    def apply_contrast_stretching(self):
        if self.selected_image_index == 0:
            messagebox.showerror("Thông báo", "Vui lòng chọn một hình ảnh trước khi áp dụng Contrast Stretching.")
            return

        selected_image = self.selected_location_label.image
        original_image = self.small_images[self.selected_image_index - 1]

        stretched_image = ImageEnhance.Contrast(original_image).enhance(2.0)
        stretched_image = stretched_image.resize((100, 100))
        stretched_image_tk = ImageTk.PhotoImage(stretched_image)
        self.selected_location_label.config(image=stretched_image_tk)
        self.selected_location_label.image = stretched_image_tk

        parameters_text = "Áp dụng Contrast Stretching"
        self.parameters_label.config(text=parameters_text)

    def apply_dilation(self):
        if self.selected_image_index == 0:
            messagebox.showerror("Thông báo", "Vui lòng chọn một hình ảnh trước khi áp dụng Dilation.")
            return

        try:
            iterations = int(self.dilation_entry.get())
        except ValueError:
            messagebox.showerror("Thông báo", "Vui lòng nhập một số nguyên hợp lệ cho Dilation.")
            return

        selected_image = self.selected_location_label.image
        original_image = self.small_images[self.selected_image_index - 1]

        dilated_image = original_image.filter(ImageFilter.MinFilter(size=3))
        for _ in range(iterations - 1):
            dilated_image = dilated_image.filter(ImageFilter.MinFilter(size=3))
        dilated_image = dilated_image.resize((100, 100))
        dilated_image_tk = ImageTk.PhotoImage(dilated_image)
        self.selected_location_label.config(image=dilated_image_tk)
        self.selected_location_label.image = dilated_image_tk

        parameters_text = f"Áp dụng Dilation với {iterations} lần lặp"
        self.parameters_label.config(text=parameters_text)

    def reset_image(self):
        if self.selected_image_index == 0:
            messagebox.showerror("Thông báo", "Vui lòng chọn một hình ảnh trước khi reset.")
            return

        selected_image = self.small_images[self.selected_image_index - 1]
        selected_image = selected_image.resize((100, 100))
        selected_image_tk = ImageTk.PhotoImage(selected_image)
        self.selected_location_label.config(image=selected_image_tk)
        self.selected_location_label.image = selected_image_tk

        parameters_text = f"Địa điểm du lich được chọn với số {self.selected_image_index}"
        self.parameters_label.config(text=parameters_text)

        for label in self.number_labels:
            label.config(bg="#4CAF50", fg="white", relief="flat")

    def split_large_image(self, large_image):
        width, height = large_image.size
        small_width = width // 4
        small_height = height // 4

        small_images = []

        for row in range(2):
            for col in range(4):
                left = col * small_width
                top = row * small_height
                right = left + small_width
                bottom = top + small_height

                small_image = large_image.crop((left, top, right, bottom))
                small_images.append(small_image)

        return small_images[:8]

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

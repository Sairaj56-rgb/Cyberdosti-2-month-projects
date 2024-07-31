import tkinter as tk
from tkinter import filedialog, messagebox
from email_spoofing_detector import is_email_spoofed

class EmailSpoofingDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spoofing Detector")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="Select an email file to check for spoofing:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="red")
        self.result_label.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Email files", "*.eml"), ("All files", "*.*")]
        )
        if file_path:
            self.check_spoofing(file_path)

    def check_spoofing(self, email_path):
        try:
            if is_email_spoofed(email_path):
                self.result_label.config(text="Spoofing detected!", fg="red")
                messagebox.showwarning("Result", "Spoofing detected!")
            else:
                self.result_label.config(text="No spoofing detected.", fg="green")
                messagebox.showinfo("Result", "No spoofing detected.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    gui = EmailSpoofingDetectorGUI(root)
    root.mainloop()

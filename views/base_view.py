from abc import ABC, abstractmethod
from tkinter import ttk, messagebox

class BaseView(ABC):
    def __init__(self, master=None):
        self.frame = ttk.Frame(master)
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        pass

    @abstractmethod
    def clear_fields(self):
        pass

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Información", message)

    def show_warning(self, message):
        messagebox.showwarning("Advertencia", message)
    
    def show_question(self, message):
        return messagebox.askyesno("Confirmar", message)
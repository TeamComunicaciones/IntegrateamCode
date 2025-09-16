import customtkinter as ctk

class CTkSpinbox(ctk.CTkFrame):
    def __init__(self, parent, from_=1, to=60, default=5, step=1, **kwargs):
        super().__init__(parent, **kwargs)

        self.from_ = from_
        self.to = to
        self.step = step
        self.var = ctk.StringVar(value=str(default))

        # Botón decrementar
        self.btn_minus = ctk.CTkButton(self, text="-", width=30, command=self.decrement)
        self.btn_minus.grid(row=0, column=0, padx=2, pady=2)

        # Entry central
        self.entry = ctk.CTkEntry(self, textvariable=self.var, justify="center")
        self.entry.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        # Botón incrementar
        self.btn_plus = ctk.CTkButton(self, text="+", width=30, command=self.increment)
        self.btn_plus.grid(row=0, column=2, padx=2, pady=2)

        # Que la columna del entry se expanda
        self.grid_columnconfigure(1, weight=1)

    def get_value(self):
        try:
            value = int(self.var.get())
        except ValueError:
            return self.from_
        
        if value < self.from_:
            return self.from_
        elif value > self.to:
            return self.to
        return value

    def increment(self):
        value = self.get_value()
        if value < self.to:
            self.var.set(str(value + self.step))

    def decrement(self):
        value = self.get_value()
        if value > self.from_:
            self.var.set(str(value - self.step))
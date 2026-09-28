"""
Ventana de credenciales de Poliedro, compartida por los módulos que usan Poliedro
(PRE-SIM, PRE-EQUIPOS, PORTAS, LEGALIZADOR, LEG. SIMCARD y LEG. KIT CONTADO).

Cada módulo tiene el botón CREDENCIALES en su submenú; todos abren la misma
ventana y comparten el perfil activo (funcionalidad/perfiles_credenciales.py).
"""

import threading

import customtkinter as ctk

from funcionalidad import perfiles_credenciales as perfiles
from funcionalidad.otp_correo import ProveedorOtpCorreo, ErrorOtpCorreo
from recursos import colors

_colores = colors.Colors()
_modal_abierto = None  # una sola ventana para toda la app

_ETIQUETAS_METODO = {
    perfiles.METODO_CORREO: "Correo",
    perfiles.METODO_MYSMS: "MySMS",
    perfiles.METODO_GOOGLE: "Google Messages",
}


def abrir_modal(parent):
    """Abre la ventana de credenciales o, si ya está abierta, la trae al frente."""
    global _modal_abierto
    if _modal_abierto is not None:
        try:
            if _modal_abierto.winfo_exists():
                _modal_abierto.deiconify()
                _modal_abierto.lift()
                _modal_abierto.focus_force()
                return _modal_abierto
        except Exception:
            pass
    _modal_abierto = ModalCredenciales(parent)
    return _modal_abierto


def credenciales_listas(parent, ventana_informacion=None):
    """
    Devuelve una copia del perfil activo si está completo. Si falta algo, lo dice
    en la ventana de avance, abre el modal y devuelve None.

    Llamar desde el hilo de la interfaz (callbacks de botones), no desde un hilo de trabajo.
    """
    perfil = perfiles.perfil_activo()
    faltan = perfiles.campos_faltantes(perfil)
    if not faltan:
        return perfil
    if ventana_informacion is not None:
        ventana_informacion.write(
            f"⚠️ Faltan datos en CREDENCIALES: {', '.join(faltan)}. Complételos y pulse Guardar."
        )
    abrir_modal(parent)
    return None


class ModalCredenciales(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Credenciales de Poliedro")
        self.geometry("470x560")
        self.resizable(False, False)
        try:
            self.transient(parent)
        except Exception:
            pass

        perfil = perfiles.perfil_activo()
        try:
            recordados = perfiles.listar()
            self._almacen_ok = True
        except perfiles.ErrorAlmacenCredenciales:
            recordados = []
            self._almacen_ok = False

        self.var_usuario = ctk.StringVar(value=perfil["usuario_poliedro"])
        self.var_clave = ctk.StringVar(value=perfil["clave_poliedro"])
        self.var_metodo = ctk.StringVar(value=perfil["metodo_otp"])
        self.var_usuario_correo = ctk.StringVar(value=perfil["usuario_correo"])
        self.var_clave_correo = ctk.StringVar(value=perfil["clave_correo"])
        self.var_recordar = ctk.BooleanVar(value=self._almacen_ok)

        self.grid_columnconfigure(1, weight=1)
        fila = 0

        # --- Poliedro ---
        self._titulo("POLIEDRO", fila); fila += 1
        self._etiqueta("Usuario", fila)
        self.combo_usuario = ctk.CTkComboBox(self, values=recordados, variable=self.var_usuario,
                                             command=self._elegir_perfil)
        self.combo_usuario.grid(row=fila, column=1, padx=(0, 20), pady=4, sticky="ew"); fila += 1
        self._etiqueta("Clave", fila)
        ctk.CTkEntry(self, textvariable=self.var_clave).grid(row=fila, column=1, padx=(0, 20), pady=4, sticky="ew")
        fila += 1

        # --- Método OTP ---
        self._titulo("EL CÓDIGO OTP LLEGA POR", fila); fila += 1
        marco_metodo = ctk.CTkFrame(self, fg_color="transparent")
        marco_metodo.grid(row=fila, column=0, columnspan=2, padx=20, pady=4, sticky="w"); fila += 1
        for i, metodo in enumerate(perfiles.METODOS):
            ctk.CTkRadioButton(marco_metodo, text=_ETIQUETAS_METODO[metodo], variable=self.var_metodo,
                               value=metodo, command=self._actualizar_visibilidad).grid(row=0, column=i, padx=(0, 14))

        # --- Correo ---
        self.marco_correo = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_correo.grid(row=fila, column=0, columnspan=2, sticky="ew"); fila += 1
        self.marco_correo.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.marco_correo, text="CORREO", font=("Bold", 15)).grid(
            row=0, column=0, columnspan=2, padx=20, pady=(12, 4), sticky="w")
        ctk.CTkLabel(self.marco_correo, text="Usuario").grid(row=1, column=0, padx=(20, 10), pady=4, sticky="w")
        ctk.CTkEntry(self.marco_correo, textvariable=self.var_usuario_correo,
                     placeholder_text="cedula@teamcomunicaciones.com.co").grid(
            row=1, column=1, padx=(0, 20), pady=4, sticky="ew")
        ctk.CTkLabel(self.marco_correo, text="Clave").grid(row=2, column=0, padx=(20, 10), pady=4, sticky="w")
        ctk.CTkEntry(self.marco_correo, textvariable=self.var_clave_correo).grid(
            row=2, column=1, padx=(0, 20), pady=4, sticky="ew")
        self.boton_probar = ctk.CTkButton(self.marco_correo, text="Probar correo", fg_color=_colores.team,
                                          text_color="white", command=self._probar_correo)
        self.boton_probar.grid(row=3, column=1, padx=(0, 20), pady=(6, 0), sticky="w")
        self.resultado_prueba = ctk.CTkLabel(self.marco_correo, text="", wraplength=330, justify="left")
        self.resultado_prueba.grid(row=4, column=1, padx=(0, 20), pady=(0, 4), sticky="w")

        # --- Recordar ---
        self.casilla_recordar = ctk.CTkCheckBox(self, text="Recordar este perfil en este equipo",
                                                variable=self.var_recordar)
        self.casilla_recordar.grid(row=fila, column=0, columnspan=2, padx=20, pady=(14, 4), sticky="w"); fila += 1
        if not self._almacen_ok:
            self.casilla_recordar.configure(state="disabled")

        # --- Estado y botones ---
        self.estado = ctk.CTkLabel(self, text="", wraplength=420, justify="left")
        self.estado.grid(row=fila, column=0, columnspan=2, padx=20, pady=4, sticky="w"); fila += 1
        marco_botones = ctk.CTkFrame(self, fg_color="transparent")
        marco_botones.grid(row=fila, column=0, columnspan=2, padx=20, pady=(8, 16), sticky="ew")
        ctk.CTkButton(marco_botones, text="Olvidar este perfil", fg_color="gray40",
                      command=self._olvidar, width=140).pack(side="left")
        ctk.CTkButton(marco_botones, text="Cancelar", fg_color="gray40",
                      command=self.destroy, width=90).pack(side="right")
        ctk.CTkButton(marco_botones, text="Guardar", fg_color=_colores.team, text_color="white",
                      command=self._guardar, width=90).pack(side="right", padx=(0, 8))

        if not self._almacen_ok:
            self._mostrar_estado("No se puede recordar en este equipo: los datos valen solo mientras la aplicación esté abierta.")

        self._actualizar_visibilidad()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(150, self._tomar_foco)

    # ------------------------------ interfaz ------------------------------ #
    def _titulo(self, texto, fila):
        ctk.CTkLabel(self, text=texto, font=("Bold", 15)).grid(
            row=fila, column=0, columnspan=2, padx=20, pady=(14, 4), sticky="w")

    def _etiqueta(self, texto, fila):
        ctk.CTkLabel(self, text=texto).grid(row=fila, column=0, padx=(20, 10), pady=4, sticky="w")

    def _tomar_foco(self):
        try:
            self.lift()
            self.focus_force()
            self.grab_set()
        except Exception:
            pass

    def _actualizar_visibilidad(self):
        if self.var_metodo.get() == perfiles.METODO_CORREO:
            self.marco_correo.grid()
        else:
            self.marco_correo.grid_remove()

    def _mostrar_estado(self, texto, error=False):
        self.estado.configure(text=texto, text_color=_colores.team if error else ("black", "white"))

    def _perfil_de_campos(self):
        return perfiles.normalizar_perfil({
            "usuario_poliedro": self.var_usuario.get(),
            "clave_poliedro": self.var_clave.get(),
            "metodo_otp": self.var_metodo.get(),
            "usuario_correo": self.var_usuario_correo.get(),
            "clave_correo": self.var_clave_correo.get(),
        })

    # ------------------------------ acciones ------------------------------ #
    def _elegir_perfil(self, usuario):
        try:
            perfil = perfiles.cargar(usuario)
        except perfiles.ErrorAlmacenCredenciales:
            perfil = None
        if not perfil:
            return
        self.var_clave.set(perfil["clave_poliedro"])
        self.var_metodo.set(perfil["metodo_otp"])
        self.var_usuario_correo.set(perfil["usuario_correo"])
        self.var_clave_correo.set(perfil["clave_correo"])
        self.var_recordar.set(True)
        self.resultado_prueba.configure(text="")
        self._actualizar_visibilidad()
        self._mostrar_estado(f"Perfil de {usuario} cargado.")

    def _probar_correo(self):
        usuario = self.var_usuario_correo.get().strip()
        clave = self.var_clave_correo.get()
        if not usuario or not clave:
            self.resultado_prueba.configure(text="Escriba usuario y clave del correo.", text_color=_colores.team)
            return
        self.boton_probar.configure(state="disabled")
        self.resultado_prueba.configure(text="Probando...", text_color=("black", "white"))

        def probar():
            try:
                cantidad = ProveedorOtpCorreo(usuario, clave).probar()
                texto, error = f"✓ Conexión correcta ({cantidad} correos en la bandeja).", False
            except ErrorOtpCorreo as e:
                texto, error = e.mensaje_usuario, True
            except Exception as e:  # no debería pasar; se muestra algo entendible
                texto, error = f"No se pudo probar el correo ({type(e).__name__}).", True
            try:
                self.after(0, lambda: self._fin_prueba(texto, error))
            except Exception:
                pass  # la ventana se cerró mientras se probaba

        threading.Thread(target=probar, daemon=True).start()

    def _fin_prueba(self, texto, error):
        if not self.winfo_exists():
            return
        self.boton_probar.configure(state="normal")
        self.resultado_prueba.configure(text=texto, text_color=_colores.team if error else ("black", "white"))

    def _guardar(self):
        perfil = self._perfil_de_campos()
        faltan = perfiles.campos_faltantes(perfil)
        if faltan:
            self._mostrar_estado(f"Falta: {', '.join(faltan)}.", error=True)
            return
        perfiles.fijar_perfil_activo(perfil)
        if self.var_recordar.get() and self._almacen_ok:
            try:
                perfiles.guardar(perfil)
            except perfiles.ErrorAlmacenCredenciales:
                self._mostrar_estado(
                    "Se guardó para esta sesión, pero no se pudo recordar en este equipo.", error=True)
                self.after(2500, self.destroy)
                return
        self.destroy()

    def _olvidar(self):
        usuario = self.var_usuario.get().strip()
        if not usuario:
            self._mostrar_estado("Elija el usuario de Poliedro que quiere olvidar.", error=True)
            return
        try:
            if usuario not in perfiles.listar():
                self._mostrar_estado(f"{usuario} no está recordado en este equipo.")
                return
            perfiles.olvidar(usuario)
            self.combo_usuario.configure(values=perfiles.listar())
        except perfiles.ErrorAlmacenCredenciales:
            self._mostrar_estado("No se pudo borrar el perfil de este equipo.", error=True)
            return
        self.var_recordar.set(False)
        self._mostrar_estado(f"Perfil de {usuario} olvidado en este equipo.")

    def destroy(self):
        global _modal_abierto
        if _modal_abierto is self:
            _modal_abierto = None
        try:
            self.grab_release()
        except Exception:
            pass
        super().destroy()

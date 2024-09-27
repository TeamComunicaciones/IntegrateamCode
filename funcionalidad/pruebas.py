class Ejemplo:
    def __init__(self) -> None:
        num_variables = 2
        base_nombre = "boton"

        def prin1(texto):
            print(texto)

        def prin2(texto):
            print(texto)

        funciones = [prin1,prin2]

        for i in range(1, num_variables + 1):
            nombre_variable = base_nombre + "_" + str(i)
            valor = lambda nv=nombre_variable: funciones[i-1](nv)
            setattr(self, nombre_variable, valor)

        # Verificar las variables creadas
        self.boton_1('boton_1')
        self.boton_2('boton_2')


cc = '9013175760'

print(cc)
print(cc[:9])

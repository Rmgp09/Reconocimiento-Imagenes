# user_management.py

import mysql.connector
import bcrypt

class UserManager:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="renzo",
                database="sistema_dental"
            )
            self.cursor = self.conexion.cursor()
            print("Conexión a MySQL exitosa")
        except mysql.connector.Error as err:
            print(f"Error de conexión a MySQL: {err}")
            raise

    def agregar_usuario(self, nombres, apellidos, correo, telefono, fecha_nacimiento, contrasena, rol):
        try:
            contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            consulta = """
            INSERT INTO usuarios (nombres, apellidos, correo, telefono, fecha_nacimiento, contrasena, rol) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(consulta, (nombres, apellidos, correo, telefono, fecha_nacimiento, contrasena_encriptada, rol))
            self.conexion.commit()
            print("Usuario registrado exitosamente.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al agregar usuario: {err}")
            return False

    def verificar_usuario(self, correo, contrasena):
        try:
            consulta = "SELECT correo, contrasena, rol, nombres, apellidos, telefono, fecha_nacimiento FROM usuarios WHERE correo = %s"
            self.cursor.execute(consulta, (correo,))
            resultado = self.cursor.fetchone()

            if resultado:
                correo_almacenado, contrasena_almacenada, rol, nombres, apellidos, telefono, fecha_nacimiento = resultado
                if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_almacenada.encode('utf-8')):
                    return {
                        "correo": correo_almacenado,
                        "rol": rol,
                        "first_name": nombres,
                        "last_name": apellidos,
                        "phone_number": telefono,
                        "fecha_nacimiento": fecha_nacimiento.strftime('%Y-%m-%d') if fecha_nacimiento else "N/A"
                    }
            return None
        except mysql.connector.Error as err:
            print(f"Error al verificar usuario: {err}")
            return None

    def update_user(self, email, first_name, last_name, phone):
        try:
            consulta = """
            UPDATE usuarios 
            SET nombres = %s, apellidos = %s, telefono = %s 
            WHERE correo = %s
            """
            self.cursor.execute(consulta, (first_name, last_name, phone, email))
            self.conexion.commit()
            print("Perfil de usuario actualizado exitosamente.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al actualizar usuario: {err}")
            return False

    def cerrar_conexion(self):
        if self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()
            print("Conexión a MySQL cerrada.")

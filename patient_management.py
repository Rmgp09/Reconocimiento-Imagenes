class PatientManager:
    def __init__(self):
        self.diagnosis_history = []

    def store_diagnosis(self, diagnosis, conclusion=None):
        # Almacenar el diagnóstico junto con una conclusión
        self.diagnosis_history.append({"details": diagnosis, "conclusion": conclusion})
        print("Diagnóstico almacenado en el historial.")

    def show_latest_conclusion(self):
        # Mostrar la conclusión del último diagnóstico
        if self.diagnosis_history:
            latest_diagnosis = self.diagnosis_history[-1]
            print("Última conclusión del diagnóstico:", latest_diagnosis["conclusion"])
            return latest_diagnosis["conclusion"]
        else:
            print("No hay diagnósticos en el historial.")
            return None

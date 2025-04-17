from datetime import datetime

class Reclamo:
    

    def __init__(self, id,fecha,servicio, detalle, socio, estado,operador_id):
        
        self.id = id
        self.fecha =        fecha 
        self.servicio= servicio
        self.detalle = detalle
        self.socio = socio
        estados_validos = ["Pendiente", "En progreso", "Resuelto", "Cancelado"]
        if estado not in estados_validos:
            raise ValueError(f"Estado inválido: {estado}. Debe ser uno de {estados_validos}")
        self.estado = estado
        self.operador_id= operador_id

    def __str__(self):
        return f"ID: {self.id}, Fecha: {self.fecha}, Tipo: {self.tipo}, socio: {self.socio}, Detalle: {self.detalle}, Estado: {self.estado}, Operador:{self.operador_id}"

    def a_diccionario(self):
        if isinstance(self.fecha, str):
            fecha_datetime = datetime.datetime.fromisoformat(self.fecha)
            return {
                "id": self.id,
                "fecha": self.fecha,
                "servicio": self.servicio,
                "socio": self.socio,
                "detalle": self.detalle,
                "estado": self.estado,
                "operador_id": self.operador_id
                
            }
        else:
            return {
                "id": self.id,
                "fecha": self.fecha,
                "servicio": self.servicio,
                "socio": self.socio,   
                "detalle": self.detalle,
                "estado": self.estado,
                "operador_id": self.operador_id
        }
from sqlalchemy.orm import Session
from app.models.ReservasBD import ReservasDB
from datetime import datetime, timedelta
from typing import List


class FechasRepository:
    def reservas_que_se_cruzan(self, db: Session, inicio: datetime, fin: datetime):
        return (
            db.query(ReservasDB)
            .filter(ReservasDB.check_in < fin, ReservasDB.check_out > inicio)
            .all()
        )
    
    def generar_fechas_rango(self, inicio: datetime, fin: datetime) -> List[datetime]:
        fechas = []
        cur = inicio
        while cur < fin:
            fechas.append(cur)
            cur = cur + timedelta(days=1)
        return fechas
    
    def encontrar_fechas_libres_por_dia(self, db: Session, inicio: datetime, fin: datetime) -> List[str]:
        ocupadas = self.reservas_que_se_cruzan(db, inicio, fin)
        ocupados_set = set()
        for r in ocupadas:
            start = r.check_in
            end = r.check_out
            cur = datetime.combine(start, datetime.min.time()) if isinstance(start, datetime) == False else start
            if isinstance(start, datetime):
                cur = start
            else: 
                cur = datetime(start.year, start.month, start.day)
            while cur < (end if isinstance(end, datetime) else datetime(end.year, end.month, end.day)):
                ocupados_set.add(cur.date())
                cur = cur + timedelta(days=1)

        dias = self.generar_fechas_rango(inicio, fin)
        libres_iso = []
        for d in dias:
            if d.date() not in ocupados_set:
                libres_iso.append(d.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z")
        return libres_iso
    
    def sugerencias_proximas(self, db: Session, inicio: datetime, fin: datetime, dias_adelante: int = 30, max_sugerencias: int = 5):
        delta = fin - inicio
        sugerencias = []
        for shift in range(1, dias_adelante + 1):
            nuevo_inicio = inicio + timedelta(days=shift)
            nuevo_fin = nuevo_inicio + delta
            libres = self.encontrar_fechas_libres_por_dia(db, nuevo_inicio, nuevo_fin)
            total_dias = (nuevo_fin - nuevo_inicio).days
            if total_dias == 0:
                continue
            if len([f for f in libres if self.is_date_in_range(f, nuevo_inicio, nuevo_fin)]) == total_dias:
                sugerencias.append({"fecha": nuevo_inicio.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"})
            else:
                if len(libres) > 0:
                    sugerencias.append({"fechas": nuevo_inicio.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"})

            if len(sugerencias) >= max_sugerencias:
                break
        return sugerencias
    
    def is_date_in_range(self, fecha_iso_str: str, inicio: datetime, fin: datetime) -> bool:
        from dateutil.parser import isoparse
        try:
            d = isoparse(fecha_iso_str)
            return inicio <= d < fin
        except Exception:
            return False

            
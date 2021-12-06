from typing import List
from .models import Symptom
from .models import Molecule
from django.db import connection

class detectionByUmbralService:

    def __init__(self):
        self.experiment_id=0

    def search_anomaly(self,experiment_id):
        self.experiment_id=experiment_id
        rows_susars, susars = self.check_susars(self)
        rows_general = self.check_general_umbral(self,list(susars))
        rows_general.extend(rows_susars)
        result = self.modify_rows(rows_general)
        return result
    
    #Este metodo estandariza los sintomas que salen de susar y del general 
    def modify_rows(rows):
        for row in rows:
            if ('molecule_molecule_id' not in row):
                row['molecule_molecule_id']='none'
                row['molecule_name']= 'none'
            else:
                row['molecule_name']=Molecule.objects.get(pk=row['molecule_molecule_id']).molecule_name
            row['symptom_title']=Symptom.objects.get(pk=row['symptom_symptom_id']).symptom_title
            row['symptom_code']=Symptom.objects.get(pk=row['symptom_symptom_id']).symptom_code
        return rows
   
    #Este metodo devuelve los sintomas que no estan asociados 
    # a una molecula y que han superado el umbral general
    def check_general_umbral(self, susars):
        rows=self.get_symptom_general_sql(self,susars)
        rowfilter =[]
        for row in rows:
            row=self.compare_frequencies(self, row, rowfilter)
        return rowfilter

    #Este metodo devuelve los sintomas que estan asociados 
    # a una molecula y que han superado el umbral de su susar
    def check_susars(self):
        rows= self.get_symptom_susars_sql(self)
        rowfilter=[]
        symptoms =[]
        for row in rows:
            symptoms.append(row['symptom_symptom_id'])
            row=self.compare_frequencies(self, row,rowfilter)
        return rowfilter,symptoms

    #Este metodo devuelve un listado de los sintomas que estan registrados en un experimento y que tambien tienen asociado un umbral de la molecula
    #Devuelve la molecula a la que esta asociada el sintoma reportado
    #El sintoma reportado
    #El umbral especifico para ese sintoma en esa molecula (Susar)
    #El contador, la cantidad de personas que han presentado el sintoma para ese experimento join
    def get_symptom_susars_sql(self):
        cursor = connection.cursor()
        query = ("select t2.molecule_molecule_id, t2.symptom_symptom_id, t2.assesment_level, t1.counter " +
        "from (select symptom_symptom_id, counter from experiment_symptom_register " +
        "where experiment_experiment_id= %s) as t1 join (select symptom_symptom_id, assesment_level, molecule_molecule_id "+
        "from susars where molecule_molecule_id in(select molecule_molecule_id "+
        "from experiment_molecule_composition where experiment_experiment_id=%s)) as t2 " +
        "on t1.symptom_symptom_id=t2.symptom_symptom_id")
        cursor.execute(query,[self.experiment_id, self.experiment_id])
        rows=self.dictfetchall(cursor)
        return rows

    #Este metodo devuelve un listado de los sintomas que estan registrados en un experimento y que no  tienen asociado ningun sintoma asociado a una molecula
    #El sintoma reportado
    #El umbral especifico para ese sintoma (el general)
    #El contador, la cantidad de personas que han presentado el sintoma para ese experimento join
    def get_symptom_general_sql(self, susars):
        cursor = connection.cursor()
        query=''
        if(len(susars)>0):
            query = ("select t1.symptom_symptom_id, t2.assesment_level, t1.counter " +
           "from experiment_symptom_register as t1 join symptom as t2 " +
            "on t1.symptom_symptom_id=t2.symptom_id "+
           "where experiment_experiment_id=%s and t1.symptom_symptom_id not in {} "%(self.experiment_id)).format(tuple(susars))
        else:
            query = ("select t1.symptom_symptom_id, t2.assesment_level, t1.counter " +
           "from experiment_symptom_register as t1 join symptom as t2 " +
            "on t1.symptom_symptom_id=t2.symptom_id "+
           "where experiment_experiment_id=%s"%(self.experiment_id))
        cursor.execute(query)
        rows=self.dictfetchall(cursor)
        return rows
    
    #Este metodo trae todos los eventos de un experimento que tengan el mismo sintoma
    def get_events_by_symptom_experitment(self, symptom_id):
        cursor = connection.cursor()
        query = ("select e.date_reported, co.name, e.age, e.weight, e.height, e.gender, symp.symptom_title  " +
        "from \"event\" as e join symptom_event_register as sympre on e.event_id=sympre.event_event_id " +
        "join country as co on e.country_country_id= co.country_id join symptom as symp on symp.symptom_id=sympre.symptom_symptom_id "+
        "where e.report_report_id in(select  re.report_id from experiment as ex "+
        "join report as re on ex.experiment_id = re.experiment_experiment_id where ex.experiment_id=%s) " +
        "and sympre.symptom_symptom_id=%s")
        cursor.execute(query,[self.experiment_id, symptom_id])
        rows=self.dictfetchall(cursor)
        return rows

    #Este metodo formatea en un diccionario el resultado de las consultas sql nativas
    def dictfetchall(cursor):
         columns = [col[0] for col in cursor.description]
         return [
             dict(zip(columns, row))
             for row in cursor.fetchall()
            ]

    #Este metodo verifica que la frecuencia de un sintoma sean igual o mayor a la del umbral (limite)
    #lo agrega a los sintomas a mostrar en la alarma por la list rowfilter
    def compare_frequencies(self, row,rowfilter):
        if(row['assesment_level']<=row['counter']):
                events =self.get_events_by_symptom_experitment(self, row['symptom_symptom_id'])
                row['events']=events
                self.get_statistical_data(self, row, events)
                rowfilter.append(row)

    #Este metodo calcula los datos estadisticos de las personas que presentan un mismo sintoma en un experimento
    def get_statistical_data(self, row, events):
        total_weight=0
        total_height=0
        total_age=0
        total_male=0
        total_female=0
        numberevents = len(events)
        for i in events:
            total_weight=total_weight+i['weight']
            total_height=total_height+i['height']
            total_age=total_age+i['age']
            if(i['gender']=='Hombre'):
                total_male=total_male+1
            else:
                total_female=total_female+1
        row['average_weight']=round(total_weight/numberevents,2)
        row['average_height']=round(total_height/numberevents,2)
        row['average_age']=round(total_age/numberevents)
        row['percentage_male']=str(round(total_male/numberevents*100))+'%'
        row['percentage_female']=str(round(total_female/numberevents*100))+'%'
        
   

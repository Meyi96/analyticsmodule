from django.views import View
from django.http import JsonResponse
import json
from anomaly_detection_api.models import Experiment
from .services import detectionByUmbralService
#from django.forms.models import model_to_dict
#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt



class checkAnomalyUmbral(View):

    def get(self, request, experiment_id):
        experiment_id =str(experiment_id)
        responsedb=detectionByUmbralService.search_anomaly(detectionByUmbralService,experiment_id)
        if(len(responsedb)>0):
            protocol = Experiment.objects.get(pk=experiment_id).protocol
            header = {'experiment_id': experiment_id, 'protocol': protocol, 'detect_anomaly': True, 'detections_number': len(responsedb) }
            header['detections']= responsedb
        else:
           header = {'experiment_id': experiment_id, 'detect_anomaly': False, }

        return JsonResponse(header, safe=False)


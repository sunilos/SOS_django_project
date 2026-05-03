from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Marksheet
from service.Serializers import MarksheetSerializers


class MarksheetCtl(BaseRestCtl):
    def get_model(self):
        return Marksheet

    def get_serializer_class(self):
        return MarksheetSerializers

    def get(self, request, id=None):
        if id:
            try:
                obj = Marksheet.objects.get(id=id)
            except Marksheet.DoesNotExist:
                return self.not_found()
            data = dict(MarksheetSerializers(obj).data)
            data["total"] = obj.total
            data["percentage"] = obj.percentage
        else:
            objs = Marksheet.objects.all()
            data = []
            for obj, item in zip(objs, MarksheetSerializers(objs, many=True).data):
                entry = dict(item)
                entry["total"] = obj.total
                entry["percentage"] = obj.percentage
                data.append(entry)
        return self.ok(data)

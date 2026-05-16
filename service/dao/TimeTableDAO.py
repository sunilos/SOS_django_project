from service.models import TimeTable
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class TimeTableDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("exam_date")
        if DataValidator.isNotNull(val):
            q = q.filter(exam_date=val)

        val = params.get("exam_time")
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(exam_time=val)

        val = params.get("semester")
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(semester=val)

        val = params.get("course_id")
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(course_id=val)

        val = params.get("subject_id")
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(subject_id=val)

        return q

    def get_model(self):
        return TimeTable

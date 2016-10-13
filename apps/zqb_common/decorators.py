# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json


def json_data(func):
    def _func(*argv, **kwargs):
        result = func(*argv, **kwargs)
        return HttpResponse(json.dumps(result), content_type="application/json")
    return _func

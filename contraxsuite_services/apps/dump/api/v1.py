"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-

# Standard imports
import io
import json
import traceback
import coreapi
import coreschema
from rest_framework import schemas


from tempfile import NamedTemporaryFile

# Django imports
from django.conf.urls import url
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.http import HttpResponse

# Third-party imports
from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

# Project imports
from apps.dump.app_dump import get_full_dump, get_field_values_dump,\
    get_model_fixture_dump, load_fixture_from_dump, download


__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2018, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.1.4/LICENSE"
__version__ = "1.1.4"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class DumpConfigView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Dump all users, roles, email addresses, review statuses, review status groups, app vars,
        document types, fields and field detectors to json.

        """
        return HttpResponse(get_full_dump(), content_type='Application/json')

    def put(self, request, *args, **kwargs):
        data = request.data  # type: dict
        buf = io.StringIO()

        try:
            with NamedTemporaryFile(mode='w+', suffix='.json') as f:
                json.dump(data, f)
                f.seek(0)
                call_command('loadnewdata', f.name, stdout=buf, interactive=False)
                buf.seek(0)
            return HttpResponse(content=get_full_dump(),
                                content_type='Application/json',
                                status=200)
        except:
            log = buf.read()
            tb = traceback.format_exc()
            data = {
                'log': log,
                'exception': tb
            }
            return HttpResponse(content=json.dumps(data),
                                content_type='Application/json',
                                status=400)


class FieldValuesDumpAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Download field values
        """
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.{}.{}"'.format(
            Site.objects.get_current(), 'field-values', 'json')
        json_data = get_field_values_dump()
        response.write(json_data)
        return response

    def put(self, request, *args, **kwargs):
        """
        Upload field values
        """
        file_ = request.FILES.dict().get('file')
        data = file_.read()
        try:
            with NamedTemporaryFile(mode='w+b', suffix='.json') as f:
                f.write(data)
                f.flush()
                call_command('loaddata', f.name, interactive=False)
            return Response("OK")
        except Exception as e:
            tb = traceback.format_exc()
            data = {
                'log': str(e),
                'exception': tb
            }
            return HttpResponse(content=json.dumps(data),
                                content_type='Application/json',
                                status=400)


class DumpFixtureSerializer(serializers.Serializer):
    app_name = serializers.CharField(required=True)
    model_name = serializers.CharField(required=True)
    file_name = serializers.CharField(required=True)
    filter_options = serializers.JSONField()


class DumpFixtureAPIView(generics.CreateAPIView):

    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "app_name",
            required=True,
            location="form",
            schema=coreschema.String(max_length=10)
        ),
        coreapi.Field(
            "model_name",
            required=True,
            location="form",
            schema=coreschema.String(max_length=50)
        ),
        coreapi.Field(
            "filter_options",
            required=False,
            location="form",
            schema=coreschema.Object()
        ),
        coreapi.Field(
            "file_name",
            required=True,
            location="form",
            schema=coreschema.String(max_length=50)
        ),
    ])

    def post(self, request, *args, **kwargs):
        """
        Download model fixture
        """
        serializer = DumpFixtureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response('Data is not valid')
        form_data = serializer.data
        file_name = form_data.pop('file_name')
        json_data = get_model_fixture_dump(**form_data)
        return download(json_data, file_name)


class LoadFixtureSerializer(serializers.Serializer):
    fixture_file = serializers.FileField(required=True)


class LoadFixtureAPIView(generics.CreateAPIView):
    serializer_class = LoadFixtureSerializer
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        """
        Install model fixtures
        """
        file_ = request.FILES.dict().get('file')
        data = file_.read()
        mode = request.POST.get('mode', 'default')
        res = load_fixture_from_dump(data, mode)
        status = 200 if res['status'] == 'success' else 400
        return Response(res, status=status)


urlpatterns = [
    url(r'dump/', DumpConfigView.as_view(), name='dump'),
    url(r'field-values/', FieldValuesDumpAPIView.as_view(), name='field-values'),
    url(r'dump-fixture/', DumpFixtureAPIView.as_view(), name='dump-fixture'),
    url(r'load-fixture/', LoadFixtureAPIView.as_view(), name='load-fixture'),
]

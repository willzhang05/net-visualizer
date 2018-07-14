from django.db import models
import json

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from netdiff.exceptions import NetdiffException
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import get_object_or_404
from .parsers import TextParser
from .serializers import NetworkGraphSerializer

class BaseReceiveNodeView(APIView):
    """
    This views allow nodes to send topology data using the RECEIVE strategy.
    Required query string parameters:
        * key
    Allowed content-types:
        * text/plain
    """
    parser_classes = (TextParser,)

    def post(self, request, pk, format=None):
        node = get_object_or_404(self.model, pk, strategy='receive')
        key = request.query_params.get('key')
        # wrong content type: 415
        if request.content_type != 'text/plain':
            return Response({'detail': _('expected content type "text/plain"')},
                            status=415)
        # missing key: 400
        if not key:
            return Response({'detail': _('missing required "key" parameter')},
                            status=400)
        # wrong key 403
        if node.key != key:
            return Response({'detail': _('wrong key')},
                            status=403)
        try:
            node.receive(request.data)
        except NetdiffException as e:
            error = _('Supplied data not recognized as %s, '
                      'got exception of type "%s" '
                      'with message "%s"') % (node.get_parser_display(),
                                              e.__class__.__name__, e)
            return Response({'detail': error}, status=400)
        return Response({'detail': _('data received successfully')})

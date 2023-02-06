from rest_framework.renderers import JSONRenderer


class ElevatorServiceRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        request = renderer_context['request']
        request_data = renderer_context['kwargs']
        request_data.update(request.GET.dict())
        if status_code / 100 != 2:
            data.update({'request_data': request_data})
            return super(
                ElevatorServiceRender,
                self).render(
                data,
                accepted_media_type,
                renderer_context)
        else:
            data = {
                'status': 'success',
                'data': data,
                'request_data': request_data}
            return super(
                ElevatorServiceRender,
                self).render(
                data,
                accepted_media_type,
                renderer_context)

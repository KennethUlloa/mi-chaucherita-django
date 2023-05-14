from django.http import HttpResponse


class RequestHandler:
    def handle(self, request):
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)
        elif request.method == "PUT":
            return self.put(request)
        elif request.method == "DELETE":
            return self.delete(request)

    def get(self, request):
        return self.default(request)

    def post(self, request):
        return self.default(request)

    def put(self, request):
        return self.default(request)

    def delete(self, request):
        return self.default(request)

    def default(self, request):
        return HttpResponse(content=b"Not implemented", status=501)

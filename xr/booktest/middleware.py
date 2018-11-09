from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
class mid(MiddlewareMixin):

    # def __init__(self,response):
    #     super().__init__(response)
    #     print ('--------------init')
    # def __call__(self,request):
    #     response=self.get_response(request)
    #     return response



    def process_request(self,request):
        print ('--------------request')
        #发现是非正常的访问
        # return HttpResponse('别爬了')



    def process_view(self,request, view_func, *view_args, **view_kwargs):
        print( '--------------view')


    def process_response(self,request, response):
        print ('--------------response')
        # return HttpResponse('我改内容了')
        return response
class my_mid(MiddlewareMixin):
    def process_exception(self,request,exception):

        return HttpResponse('报错了')
class my_mid1(MiddlewareMixin):
    def process_exception(self,request,exception):

        return HttpResponse('def')

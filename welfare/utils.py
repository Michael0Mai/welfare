from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from rest_framework.pagination import PageNumberPagination

def custom_exception_handler(exc, context): # 异常处理
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

class customrenderer(JSONRenderer): #自定义正常返回
    def render(self, data, accepted_media_type=None, renderer_context=None): # 重构render方法    
        if data == None:
            data = {}
            data["results"] = None
        
        if renderer_context:
            if isinstance(data, list):              
                temp = {}
                temp["results"] = data
                data = temp
                # data["results"] = data
            
            status_code = renderer_context["response"].status_code
            data['status_code'] = status_code

            # 返回JSON数据
            return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)

class MyPageNumberPagination(PageNumberPagination): # 分页器
    page_size = 10   # default page size
    page_size_query_param = 'size'  # ?page=xx&size=??
    max_page_size = 30 # max page size

# class customrenderer(JSONRenderer): #自定义正常返回
#     def render(self, data, accepted_media_type=None, renderer_context=None): # 重构render方法
#         if renderer_context:
#             if isinstance(data, dict):
#                 # message = data.pop('msg', 'success') # 删除字典 data 里的 key “message”, 并返回 'success'
#                 status_code = data.pop('code', renderer_context["response"].status_code)
#             else:
#                 #message = 'success'
#                 status_code = renderer_context["response"].status_code

#             #data['message'] = message
#             if data != None:
#                 data['status_code'] = status_code
#             else:
#                 data = {}
#                 data['status_code'] = status_code
            
#             # 返回JSON数据
#             return super().render(data, accepted_media_type, renderer_context)
#         else:
#             return super().render(data, accepted_media_type, renderer_context)

from django.utils.deprecation import MiddlewareMixin

class RecordModifiedByMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("process_view")
        print(request)
        print(request.body)
        print(request.POST)
        print( hasattr(request, 'obj'))
        print( request.user.is_authenticated)
        if request.user.is_authenticated and hasattr(request, 'obj'):
            obj = request.post
            print(obj)
            # if hasattr(obj, 'modified_by') and not obj.modified_by:
            if hasattr(obj, 'modified_by'):
                obj.modified_by = request.user
                obj.save()
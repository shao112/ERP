from django.utils.deprecation import MiddlewareMixin

class RecordModifiedByMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("process_view")
        if request.user.is_authenticated and hasattr(request, 'obj'):
            obj = request.obj
            print(obj)
            # if hasattr(obj, 'modified_by') and not obj.modified_by:
            if hasattr(obj, 'modified_by'):
                obj.modified_by = request.user
                obj.save()
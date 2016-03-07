from Module import Module

class builtin(Module):

### REQUEST rendering

    def render_greeting(self, request):
        request.raw = 'greeting'

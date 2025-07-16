from typing import Callable, Any


class CodeMender:
    """Main class."""

    type Function = Callable[..., Any]
    """Function type."""


    class MethodPatch:
        """Represents a method patch. This class can only be used with *class methods*."""

        def _default(self):
            pass

        def __init__(self, patch_id: str, target: Any, func_name: str):
            self.original: CodeMender.Function = self._default
            self.target: Any = target
            self.func_name = func_name
            self.id: str = patch_id
        

        def prefix(self, target, *orig_args, **orig_kwds):
            """This is called before the original function executed."""
            return orig_args, orig_kwds


        def postfix(self, target, call_res: Any, *orig_args, **orig_kwds):
            """This is called after the original function executed."""
            return call_res
        

        def apply(self):
            """Apply the current patch the targeted class method."""
            
            method: CodeMender.Function = getattr(self.target, self.func_name, self._default)
            self.original = method
            self.target = self.target
            setattr(self.target, self.func_name, self)
        

        def __call__(self, *args, **kwds):
            """Replaces the original class method."""

            new_args, new_kwds = self.prefix(self.target, *args, **kwds)
            result: Any = self.original(*new_args, **new_kwds)
            return self.postfix(self.target, result, *args, **kwds)


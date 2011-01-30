class PrototypeException(Exception):
    pass

class PrototypeSwitcher(object):
    def __init__(self, delegate, extend=False):
        self._delegate = delegate
        self._replacement = None
        self._extend = extend

    def _delegate_call(self, key):
        def delegator(eat_self, *args, **kwargs):
            bound_fn = getattr(self._delegate, key)
            if bound_fn:
                return bound_fn(*args, **kwargs)
        return delegator

    def _decorate(self, cls):
        old_getattr = cls.__getattr__ if '__getattr__' in cls.__dict__ else None
        delegate_bind = self._delegate #for speed
        def __getattr__(self, name):
            if old_getattr:
                try:
                    print "using old getattr"
                    return old_getattr(self, name)
                except AttributeError:
                    pass
            return getattr(delegate_bind, name)
        cls.__getattr__ = __getattr__
        cls.__call__ = self._delegate_call('__call__')
        return cls

    @property
    def new(self):
        if not self._replacement:
            @self._decorate
            class PrototypeChild(object):
                pass
            self._replacement = PrototypeChild()
        return self._replacement

    def __call__(self, cls):
        if getattr(self._delegate, '__call__', False) and not self._extend:
            raise PrototypeException("You attempted to use a prototype as a decorator, but the object you're extending already has a __call__ method.  You will need to explicitly use the .extend syntax like this: @prototype(obj, True) in this case.  You will see this error on multi-level prototypes")
        return self._decorate(cls)

    def __getattr__(self, name):
        if getattr(self._delegate, 'new', False):
            raise PrototypeException("You are using a raw prototype as a clone, but the parent defined a new attribute.  You must explicitly instantiate using @prototype(obj).new in this case.  You will see this error on multi-level prototypes.")
        return getattr(self.new, name)


def prototype(delegate, extend=False):
    """
    Implement javascript prototypal inheritance in python.  This
    implementation will allow you to create new prototypes on the fly,
    or set prototypes for classes.

    Usage:

    You can use it to make lightweight children from an existing object.

    obj = Parent()
    obj_child = prototype(obj)

    You can use it to make static prototypes for classes.

    obj = Parent()
    
    @prototype(obj)
    class Child(object):
        pass

    obj2 = Child()

    In some rare cases you must explicitly force a clone or a
    decorator to be created.  If the object contains a `new` property
    you must explicitly call .new to force a clone to be made.

    obj = Parent()
    obj.new = 1

    obj_child = prototype(obj).new


    If the object contains a `__call__` property, you must explicitly
    create a decorator with the extend=True keyword argument.
    
    obj = Parent()
    obj.__call__ = 1

    @prototype(obj, extend=True)
    class Child(object):
        pass

    Prototypes can extend prototypes as many levels as you want.  One note,
    prototypes extending prototypes must use .new and extend=True.

    obj = Parent()
    child = prototype(obj)
    grandchild = prototype(obj).new
    """
    return PrototypeSwitcher(delegate, extend)
                


import unittest

from prototype import prototype, PrototypeException, PrototypeSwitcher

class BaseClass(object):
    def __init__(self, base_list):
        print "in base ctr"
        self.base_list = base_list
        self.base_test = True
        self.base_list.append('init')

    def __getattr__(self, name):
        print "in base getattr", name
        if name in ('new',) or name.startswith('__'):
            #this magic is to make BaseClass not trigger 
            # 'new' or '__call__' checks
            print "caight new and call"
            raise AttributeError(name)
        self.base_list.append(name)
        return name

class SimpleBase(object):
    pass


class TestingHowPythonWorks(unittest.TestCase):
    def test_what_python_lets_us_set(self):
        """ 
        this is a long and tedious test to find out what python
        will let us hack, apparently __doc__ and __subclasscheck__ are
        all broken
        """
        class Foo(object):
            pass

        #Foo.__doc__ = 1 #raises
        Foo.__new__ = 1
        Foo.__init__ = 1
        Foo.__del__ = 1
        Foo.__repr__ = 1
        Foo.__str__ = 1
        Foo.__lt__ = 1
        Foo.__le__ = 1
        Foo.__eq__ = 1
        Foo.__ne__ = 1
        Foo.__gt__ = 1
        Foo.__ge__ = 1
        Foo.__cmp__ = 1
        Foo.__rcmp__ = 1
        Foo.__hash__ = 1
        Foo.__nonzero__ = 1
        Foo.__unicode__ = 1
        Foo.__getattr__ = 1
        Foo.__setattr__ = 1
        Foo.__delattr__ = 1
        Foo.__getattribute__ = 1
        Foo.__get__ = 1
        Foo.__set__ = 1
        Foo.__delete__ = 1
        Foo.__slots__ = 1
        Foo.__metaclass__ = 1
        Foo.__isinstancecheck__ = 1
        # Foo.__subclasscheck__ = 1 #raises
        Foo.__call__ = 1
        Foo.__len__ = 1
        Foo.__getitem__ = 1
        Foo.__setitem__ = 1
        Foo.__delitem__ = 1
        Foo.__iter__ = 1
        Foo.__reversed__ = 1
        Foo.__contains__ = 1
        Foo.__getslice__ = 1
        Foo.__setslice__ = 1
        Foo.__delslice__ = 1
        Foo.__add__ = 1
        Foo.__sub__ = 1
        Foo.__mul__ = 1
        Foo._floordiv__ = 1
        Foo.__mod__ = 1
        Foo.__divmod__ = 1
        Foo.__pow__ = 1
        Foo.__lshift__ = 1
        Foo.__rshift__ = 1
        Foo.__and__ = 1
        Foo.__xor__ = 1
        Foo.__or__ = 1
        Foo.__div__ = 1
        Foo.__truediv__ = 1

        Foo.__radd__ = 1
        Foo.__rsub__ = 1
        Foo.__rmul__ = 1
        Foo.__rdiv__ = 1
        Foo.__rtruediv__ = 1
        Foo.__rfloordiv__ = 1
        Foo.__rmod__ = 1
        Foo.__rdivmod__ = 1
        Foo.__rpow__ = 1
        Foo.__rlshift__ = 1
        Foo.__rrshift__ = 1
        Foo.__rand__ = 1
        Foo.__rxor__ = 1
        Foo.__ror__ = 1
        
        Foo.__iadd__ = 1
        Foo.__isub__ = 1
        Foo.__imul__ = 1
        Foo.__idiv__ = 1
        Foo.__itruediv__ = 1
        Foo.__ifloordiv__ = 1
        Foo.__imod__ = 1
        Foo.__ipow__ = 1
        Foo.__ilshift__ = 1
        Foo.__irshift__ = 1
        Foo.__iand__ = 1
        Foo.__ixor__ = 1
        Foo.__ior__ = 1

        Foo.__neg__ = 1
        Foo.__pos__ = 1
        Foo.__abs__ = 1
        Foo.__invert__ = 1
        
        Foo.__complex__ = 1
        Foo.__int__ = 1
        Foo.__long__ = 1
        Foo.__float__ = 1
        Foo.__oct__ = 1
        Foo.__hex__ = 1
        Foo.__index__ = 1
        Foo.__coerce__ = 1
        
        Foo.__enter__ = 1
        Foo.__exit__ = 1
        

class TestInstanceProperties(unittest.TestCase):

    def setUp(self):
        self.base = BaseClass([])
        self.simple_base = SimpleBase()

    def test_pass(self):
        pass
        
    def test_instance(self):
        base = self.base
        base.base_test = 0

        extend = prototype(base)
        extend.test = 1

        assert extend.base_test == base.base_test == 0, "testing fallback"
        assert extend.test == 1, "testing basic setting"
        assert extend.test2 == 'test2', "testing fallback"
        assert base.test == 'test', "ensuring property didn't propagate up"
        assert base.base_list == ['init', 'test2', 'test']

    def test_instance_is_dynamic(self):
        base = self.base
        base.test = 0
        extend = prototype(base)
        assert extend.test == base.test == 0, "testing basic fallback"

        base.test = 1
        assert extend.test == base.test == 1, "testing dynamic fallback"
        assert base.base_list == ['init']


    def test_instance_not_defined(self):
        base = self.simple_base
        base.test = 5
        extend = prototype(base)
        extend.extend_test = 42

        assert base.test == extend.test == 5, "simple fallback"
        try:
            extend.foo
            assert False, "extend.foo should raise an exception"
        except AttributeError:
            pass

        assert extend.extend_test == 42, "basic setting"
        try:
            base.extend_test
            assert False, "base.extend_test shouldn't be set (propagation)"
        except AttributeError:
            pass

    def test_functions_work(self):
        import new
        base = self.base
        def id(self, x):
            return x

        base.id = new.instancemethod(id, base)
        base.id(5)
    
        extend = prototype(base)
        
        extend.incr = lambda x: x + 1 #try adding a classmethod

        def incr2(self, x):
            return x + 2
        
        extend.incr2 = new.instancemethod(incr2, extend) #and a bound method
        
        assert base.id(5) == extend.id(5) == 5, "fallback instance methods work"
        assert extend.incr(5) == 6, "bound class methods work"
        assert extend.incr2(5) == 7, "bound instance methods work"


    def test_existing_new_works(self):
        base = self.base
        base.new = 5
        base.bar = 6
        extend = prototype(base)
        try:
            extend.bar
            assert False, "you can't use magic new removal if base has a new"
        except PrototypeException:
            pass

        assert isinstance(extend, PrototypeSwitcher), "prototype switching"
        extend2 = extend.new
        assert not isinstance(extend2, PrototypeSwitcher), "switch worked"
        assert extend2.bar == base.bar == 6, "switched instance prototypes corerctly"
        extend3 = extend.new
        assert id(extend2) == id(extend3), "news are singletons"

    def test_multi_level(self):
        base = self.simple_base
        base.a = 1
        
        extend = prototype(base).new
        extend.b = 2

        further = prototype(extend).new
        further.c = 3
        
        sibling = prototype(extend).new
        sibling.d = 4

        baby = prototype(sibling).new
        baby.e = 5
        
        assert base.a == extend.a == further.a == sibling.a == baby.a == 1
        assert extend.b == further.b == sibling.b == baby.b == 2
        assert further.c == 3
        try:
            sibling.c
            assert False
        except:
            pass
        try:
            baby.c
        except:
            pass

        assert sibling.d == baby.d == 4
        assert baby.e == 5


class TestClassProperties(unittest.TestCase):
    def setUp(self):
        self.base = BaseClass([])

        @prototype(self.base)
        class ExtendBase(object):
            extend_marker = 5

            def __init__(self):
                self.member_extend = 6
            
            @classmethod
            def add5(cls, x):
                return x + 5
            
            def add3(self, x):
                return x + 3

        self.extend = ExtendBase

    def test_class_extension(self):
        extend = self.extend()
        base = self.base
        
        assert extend.test == base.test == 'test', "base getattr works"
        base.foo = 1
        assert extend.foo == base.foo == 1, "base setting works"
        extend.bar = 2
        assert extend.bar == 2, "extend setting works"
        assert base.bar == 'bar', "propagation didn't happen"
        assert extend.extend_marker == 5, "class variables work"
        assert base.extend_marker == 'extend_marker', "propagation didn't happen"
        assert extend.member_extend == 6, "member variables work"
        assert extend.add3(5) == 8, "methods work"
        assert extend.add5(5) == 10, "classmethods work"
        assert self.extend.add5(6) == 11, "classmethods work on the class"
        print base.base_list
        assert base.base_list == extend.base_list == ['init', 'test', 'test', 'bar', 'extend_marker'], "correct calls were made to base.getattr"

    def test_class_extension_with_call_set(self):
        class Callable(object):
            def __call__(self, x):
                return x + 5

        base = Callable()
        assert base(5) == 10, "call correctly written"
        
        try:
            @prototype(base)
            class ShouldFail(object):
                pass
            assert False, "Required extend when call overwritten"
        except PrototypeException:
            pass

        @prototype(base, extend=True)
        class ShouldPass(object):
            pass

        extend = ShouldPass()
        print extend
        print getattr(extend, '__call__')
        print getattr(extend, '__call__'), "should have __call__"
        assert hasattr(extend, '__call__'), "should have __call__"
        assert callable(extend), "should be callable"
        assert getattr(extend, '__call__', False), "__call__ progates correctly"
        
        print base(7)
        print extend(8)
        assert extend(6) == base(6) == 11, "call works correctly on classical prototypes"

    def test_docs_work(self):
        class Docs(object):
            """testing docs"""
            pass

        base = Docs()
        assert base.__doc__ == "testing docs", "docs stuck"

        @prototype(base)
        class OK(object):
            pass

        extend = OK()
        print extend.__doc__
        assert extend.__doc__ == None, "You can't set __doc__ wtf python"


from test_helper import FullyPython

class TestCrazyPython(unittest.TestCase):
    def setUp(self):
        self.base = FullyPython()

    def test_mock(self):
        assert self.base

        sub = prototype(self.base)
        return #TODO: make this work
        print len(sub)

        assert len(sub) == len(self.base)
        
if __name__ == '__main__':
    unittest.main()

#Prototypal Inheritance for Python

Implement javascript prototypal inheritance in python.  This
implementation will allow you to create new prototypes on the fly, or
set prototypes for classes.

## Usage

You can use it to make lightweight children from an existing object.

    obj = Parent()
    obj_child = prototype(obj)

You can use it to make static prototypes for classes.

    obj = Parent()
    
    @prototype(obj)
    class Child(object):
        pass

    obj2 = Child()

## Explicit Generation

In some rare cases you must explicitly force a clone or a decorator to
be created.  If the object contains a `new` property you must
explicitly call .new to force a clone to be made.

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

##Nested Prototypes

Prototypes can extend prototypes as many levels as you want.  One
note, prototypes extending prototypes must use .new and extend=True.

    obj = Parent()
    child = prototype(obj)
    grandchild = prototype(child).new

*(c) 2011 Sauce Labs*

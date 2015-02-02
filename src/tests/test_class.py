# ===========================================================================
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
# ===========================================================================
from System.Collections import Hashtable
from Python.Test import ClassTest
import sys, os, string, unittest, types
import Python.Test as Test
import System


class ClassTests(unittest.TestCase):
    """Test CLR class support."""

    def testBasicReferenceType(self):
        """Test usage of CLR defined reference types."""
        String = System.String
        self.assertEquals(String.Empty, "")


    def testBasicValueType(self):
        """Test usage of CLR defined value types."""
        Int32 = System.Int32
        self.assertEquals(Int32.MaxValue, 2147483647)


    def testClassStandardAttrs(self):
        """Test standard class attributes."""
        self.assertTrue(ClassTest.__name__ == 'ClassTest')
        self.assertTrue(ClassTest.__module__ == 'Python.Test')
        self.assertTrue(type(ClassTest.__dict__) == types.DictProxyType)
        self.assertTrue(len(ClassTest.__doc__) > 0)


    def testClassDocstrings(self):
        """Test standard class docstring generation"""
        value = 'Void .ctor()'
        self.assertTrue(ClassTest.__doc__ == value)


    def testClassDefaultStr(self):
        """Test the default __str__ implementation for managed objects."""
        s = System.String("this is a test")
        self.assertTrue(str(s) == "this is a test")


    def testClassDefaultRepr(self):
        """Test the default __repr__ implementation for managed objects."""
        s = System.String("this is a test")
        self.assertTrue(repr(s).startswith("<System.String object"))


    def testNonPublicClass(self):
        """Test that non-public classes are inaccessible."""
        from Python import Test

        def test():
            from Python.Test import InternalClass

        self.assertRaises(ImportError, test)

        def test():
            x = Test.InternalClass

        self.assertRaises(AttributeError, test)


    def testBasicSubclass(self):
        """Test basic subclass of a managed class."""

        class MyTable(Hashtable):
            def howMany(self):
                return self.Count

        table = MyTable()

        self.assertTrue(table.__class__.__name__.endswith('MyTable'))
        self.assertTrue(type(table).__name__.endswith('MyTable'))
        self.assertTrue(len(table.__class__.__bases__) == 1)
        self.assertTrue(table.__class__.__bases__[0] == Hashtable)

        self.assertTrue(table.howMany() == 0)
        self.assertTrue(table.Count == 0)

        table.set_Item('one', 'one')
        
        self.assertTrue(table.howMany() == 1)
        self.assertTrue(table.Count == 1)

        MyTable = None


    def testSubclassWithNoArgConstructor(self):
        """Test subclass of a managed class with a no-arg constructor."""
        from Python.Test import ClassCtorTest1
        
        class SubClass(ClassCtorTest1):
            def __init__(self, name):
                self.name = name

        # This failed in earlier versions
        inst = SubClass('test')

    def testSubclassWithVariousConstructors(self):
        """Test subclass of a managed class with various constructors."""
        from Python.Test import ClassCtorTest2
        
        class SubClass(ClassCtorTest2):
            def __init__(self, v):
                ClassCtorTest2.__init__(self)
                self.value = v

        inst = SubClass('test')
        self.assertTrue(inst.value == 'test')

        class SubClass2(ClassCtorTest2):
            def __init__(self, v):
                ClassCtorTest2.__init__(self)
                self.value = v

        inst = SubClass2('test')
        self.assertTrue(inst.value == 'test')


    def testStructConstruction(self):
        """Test construction of structs."""
        from System.Drawing import Point

        p = Point()
        self.assertTrue(p.X == 0)
        self.assertTrue(p.Y == 0)

        p = Point(0, 0)
        self.assertTrue(p.X == 0)
        self.assertTrue(p.Y == 0)

        p.X = 10
        p.Y = 10

        self.assertTrue(p.X == 10)
        self.assertTrue(p.Y == 10)



    # test strange __new__ interactions
    
    # test weird metatype
    # test recursion
    # test 


    def testIEnumerableIteration(self):
        """Test iteration over objects supporting IEnumerable."""
        list = Test.ClassTest.GetArrayList()

        for item in list:
            self.assertTrue((item > -1) and (item < 10))

        dict = Test.ClassTest.GetHashtable()

        for item in dict:
            cname = item.__class__.__name__
            self.assertTrue(cname.endswith('DictionaryEntry'))


    def testIEnumeratorIteration(self):
        """Test iteration over objects supporting IEnumerator."""
        chars = Test.ClassTest.GetEnumerator()

        for item in chars:
            self.assertTrue(item in 'test string')




    def testOverrideGetItem(self):
        """Test managed subclass overriding __getitem__."""

        class MyTable(Hashtable):
                
            def __getitem__(self, key):
                value = Hashtable.__getitem__(self, key)
                return 'my ' + str(value)

        table = MyTable()
        table['one'] = 'one'
        table['two'] = 'two'
        table['three'] = 'three'

        self.assertTrue(table['one'] == 'my one')
        self.assertTrue(table['two'] == 'my two')
        self.assertTrue(table['three'] == 'my three')

        self.assertTrue(table.Count == 3)                    


    def testOverrideSetItem(self):
        """Test managed subclass overriding __setitem__."""

        class MyTable(Hashtable):
                
            def __setitem__(self, key, value):
                value = 'my ' + str(value)
                Hashtable.__setitem__(self, key, value)

        table = MyTable()
        table['one'] = 'one'
        table['two'] = 'two'
        table['three'] = 'three'

        self.assertTrue(table['one'] == 'my one')
        self.assertTrue(table['two'] == 'my two')
        self.assertTrue(table['three'] == 'my three')

        self.assertTrue(table.Count == 3)                    



class ClassicClass:
    def kind(self):
        return 'classic'

class NewStyleClass(object):
    def kind(self):
        return 'new-style'



def test_suite():
    return unittest.makeSuite(ClassTests)

def main():
    unittest.TextTestRunner().run(test_suite())

if __name__ == '__main__':
    main()


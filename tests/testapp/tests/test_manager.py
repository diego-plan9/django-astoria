import ast
from django.test.testcases import TestCase

from testapp.models import AstoriaNode

FUNCTION_1 = '''
def f(a, b, c=[]):
    print 1+2*3/4**5
    x = [6,'foo', a.bar]
    return x[:-1]
'''


class ManagerTestCase(TestCase):
    '''
    Tests from AST
    '''
    @classmethod
    def setUpTestData(cls):
        pass

    def test_001_roundtrip_1(self):
        '''
        Test the roundtrip of a small function.
        '''
        ast_tree = ast.parse(FUNCTION_1)
        root = AstoriaNode.objects.create_from_ast(ast_tree)

        db_tree = root.as_ast()
        self.assertEqual(ast.dump(ast_tree), ast.dump(db_tree))

    def test_002_roundtrip_2(self):
        '''
        Test the roundtrip of this file.
        '''
        f = open(__file__, 'r')
        contents = f.read()
        ast_tree = ast.parse(contents)
        f.close()

        root = AstoriaNode.objects.create_from_ast(ast_tree)
        db_tree = root.as_ast()
        self.assertEqual(ast.dump(ast_tree), ast.dump(db_tree))

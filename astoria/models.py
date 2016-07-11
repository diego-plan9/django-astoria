from django.db import models
from jsonfield import JSONField
from lsapling.models import OrderedTree, OrderedTreeQuerySet

from util import AstToAstoriaGenerator, AstoriaToAstGenerator


class NodeQuerySet(OrderedTreeQuerySet):
    '''
    Custom manager implementing the AST related methods.
    '''
    def create_from_ast(self, ast_tree, parent=None):
        generator = AstToAstoriaGenerator(self)
        root = generator.visit(node=ast_tree, parent=parent)
        return root

    def as_ast(self, root=None):
        generator = AstoriaToAstGenerator()
        return generator.visit(root)


class Node(OrderedTree):
    '''
    Node on the database. Can be an AST node, or a helper node.
    '''
    _id = models.CharField(max_length=1024)
    _value = JSONField(null=True)
    _is_helper = models.BooleanField(default=False)
    _is_list = models.BooleanField(default=False)

    objects = NodeQuerySet.as_manager()

    def as_ast(self):
        return self.__class__.objects.as_ast(root=self)

    def __unicode__(self):
        return '[%s%s%s=%s]' % ('@' if self._is_helper else ' ',
                                self._id,
                                '*' if self._is_list else '',
                                str(self._value))

    class Meta:
        abstract = True

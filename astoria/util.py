import ast


class AstToAstoriaGenerator(object):
    '''
    AST -> Astoria.Node
    '''
    def __init__(self, objects, root_id='ROOT'):
        self.objects = objects
        self.root_id = root_id

    def visit(self, node, field=None, parent=None, in_list=False):
        '''
        Visit a node.
        '''
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, field, parent, in_list)

    def generic_visit(self, node, field=None, parent=None, in_list=False):
        '''
        Called if no explicit visitor function exists for a node.
        '''
        # add Node to Tree
        method = parent.add_child if parent else self.objects.add_root
        _id = field if field else self.root_id
        if not parent:
            method = self.objects.add_root
        else:
            method = parent.add_child

        tree_node = method(_id=_id,
                           _value=node.__class__.__name__,
                           _is_helper=False,
                           _is_list=in_list)

        for f, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item,
                                   field=f,
                                   parent=tree_node,
                                   in_list=True)
                    else:  # pragma: no cover
                        # TODO: review documentation to find out if this case
                        # is actually possible
                        tree_node.add_child(_id=f,
                                            _value=value,
                                            _is_helper=True,
                                            _is_list=True)
                # fix for empty lists
                if len(value) == 0:
                    tree_node.add_child(_id=f,
                                        _value=[],
                                        _is_helper=True,
                                        _is_list=False)

            elif isinstance(value, ast.AST):
                self.visit(value, field=f, parent=tree_node, in_list=False)
            else:
                tree_node.add_child(_id=f,
                                    _value=value,
                                    _is_helper=True,
                                    _is_list=False)
        return tree_node


class AstoriaToAstGenerator(object):
    '''
    Astoria.Node -> AST
    '''
    def __init__(self):
        self.ast = None

    def visit(self, node):
        '''
        Visit a node.
        '''
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        '''
        Called if no explicit visitor function exists for a node.
        '''
        # get the constructor
        if not node._is_helper:
            method = 'construct_' + node._value
            constructor = getattr(self, method, self.generic_constructor)

        # iterate through children recursively
        children = list(node.get_children())
        if children:
            kwargs = {}
            for child in children:
                if child._is_list:
                    kwargs.setdefault(child._id, []).append(self.visit(child))
                else:
                    kwargs[child._id] = self.visit(child)

            if node._is_helper:  # pragma: no cover
                # TODO: review documentation to find out if this case
                # is actually possible
                pass
            else:
                return constructor(node, **kwargs)
        else:
            if node._is_helper:
                # TODO: revise unicode conversion. Currently all literals are
                # forced to str, even if the source AST included unicode Str()
                if isinstance(node._value, unicode):
                    return str(node._value)
                else:
                    return node._value
            else:
                return constructor(node)

    def generic_constructor(self, node, **kwargs):
        '''
        Called if no explicit constructor exists for a node. If a method with
        the name "construct_CLASSNAME" exists it will be used instead.
        '''
        return getattr(ast, node._value)(**kwargs)

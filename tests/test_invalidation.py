#!/usr/bin/env python
# coding:utf-8
from meshroom.core.graph import Graph
from meshroom.core import desc, registerNodeType


class SampleNode(desc.Node):
    """ Sample Node for unit testing """
    internalFolder = '{cache}/{nodeType}/{uid0}/'
    inputs = [
        desc.File(name='input', label='Input', description='', value='', uid=[0],),
        desc.StringParam(name='paramA', label='ParamA', description='', value='', uid=[])  # No impact on UID
    ]
    outputs = [
        desc.File(name='output', label='Output', description='', value='{cache}/{nodeType}/{uid0}/', uid=[])
    ]


registerNodeType(SampleNode)


def test_output_invalidation():
    graph = Graph('')
    n1 = graph.addNewNode('SampleNode', input='/tmp')
    n2 = graph.addNewNode('SampleNode')
    n3 = graph.addNewNode('SampleNode')

    graph.addEdges(
        (n1.output, n2.input),
        (n1.output, n3.input)
    )

    # N1.output ----- N2.input
    #                \
    #                 N3.input

    # Compare UIDs of similar attributes on different nodes
    n2inputUid = n2.input.uid()
    n3inputUid = n3.input.uid()
    assert n3inputUid == n2inputUid      # => UIDs are equal

    # Change a parameter outside UID
    n1.paramA.value = 'a'
    assert n2.input.uid() == n2inputUid  # => same UID as before

    # Change a parameter impacting UID
    n1.input.value = "/a/path"
    assert n2.input.uid() != n2inputUid      # => UID has changed
    assert n2.input.uid() == n3.input.uid()  # => UIDs on both node are still equal


def test_inputLinkInvalidation():
    """
    Input links should not change the invalidation.
    """
    graph = Graph('')
    n1 = graph.addNewNode('SampleNode')
    n2 = graph.addNewNode('SampleNode')

    graph.addEdges((n1.input, n2.input))
    assert n1.input.uid() == n2.input.uid()
    assert n1.output.value == n2.output.value



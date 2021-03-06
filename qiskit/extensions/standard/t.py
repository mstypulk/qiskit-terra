# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,arguments-differ

"""
T=sqrt(S) phase gate or its inverse.
"""
import numpy
from qiskit.circuit import CompositeGate
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.circuit.decorators import _op_expand, _to_bits
from qiskit.qasm import pi
from qiskit.extensions.standard.u1 import U1Gate


class TGate(Gate):
    """T Gate: pi/4 rotation around Z axis."""

    def __init__(self):
        """Create new T gate."""
        super().__init__("t", 1, [])

    def _define(self):
        """
        gate t a { u1(pi/4) a; }
        """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (U1Gate(pi/4), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate."""
        return TdgGate()

    def to_matrix(self):
        """Return a Numpy.array for the S gate."""
        return numpy.array([[1, 0],
                            [0, (1+1j) / numpy.sqrt(2)]], dtype=complex)


class TdgGate(Gate):
    """T Gate: -pi/4 rotation around Z axis."""

    def __init__(self):
        """Create new Tdg gate."""
        super().__init__("tdg", 1, [])

    def _define(self):
        """
        gate t a { u1(pi/4) a; }
        """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (U1Gate(-pi/4), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate."""
        return TGate()

    def to_matrix(self):
        """Return a Numpy.array for the S gate."""
        return numpy.array([[1, 0],
                            [0, (1-1j) / numpy.sqrt(2)]], dtype=complex)


@_to_bits(1)
@_op_expand(1)
def t(self, q):
    """Apply T to q."""
    return self.append(TGate(), [q], [])


@_to_bits(1)
@_op_expand(1)
def tdg(self, q):
    """Apply Tdg to q."""
    return self.append(TdgGate(), [q], [])


QuantumCircuit.t = t
QuantumCircuit.tdg = tdg
CompositeGate.t = t
CompositeGate.tdg = tdg

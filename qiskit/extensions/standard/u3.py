# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name
"""
Two-pulse single-qubit gate.
"""
import numpy
from qiskit.circuit import CompositeGate
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.circuit.decorators import _op_expand, _to_bits
from qiskit.extensions.standard.ubase import UBase


class U3Gate(Gate):
    """Two-pulse single-qubit gate."""

    def __init__(self, theta, phi, lam):
        """Create new two-pulse single qubit gate."""
        super().__init__("u3", 1, [theta, phi, lam])

    def _define(self):
        definition = []
        q = QuantumRegister(1, "q")
        rule = [(UBase(self.params[0], self.params[1], self.params[2]), [q[0]],
                 [])]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate.

        u3(theta, phi, lamb)^dagger = u3(-theta, -lam, -phi)
        """
        return U3Gate(-self.params[0], -self.params[2], -self.params[1])

    def to_matrix(self):
        """Return a Numpy.array for the U3 gate."""
        theta, phi, lam = self.params
        return numpy.array(
            [[
                numpy.cos(theta / 2),
                -numpy.exp(1j * lam) * numpy.sin(theta / 2)
            ],
             [
                 numpy.exp(1j * phi) * numpy.sin(theta / 2),
                 numpy.exp(1j * (phi + lam)) * numpy.cos(theta / 2)
             ]],
            dtype=complex)


@_to_bits(1)
@_op_expand(1)
def u3(self, theta, phi, lam, q):
    """Apply u3 to q."""
    return self.append(U3Gate(theta, phi, lam), [q], [])


QuantumCircuit.u3 = u3
CompositeGate.u3 = u3

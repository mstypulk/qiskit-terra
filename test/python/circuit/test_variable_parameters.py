# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.


"""Test circuits with variable parameters."""
import numpy

from qiskit import BasicAer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Gate, Parameter
from qiskit.transpiler import transpile
from qiskit.compiler import assemble
from qiskit.test import QiskitTestCase


class TestVariableParameters(QiskitTestCase):
    """QuantumCircuit Operations tests."""

    def test_gate(self):
        """Test instantiating gate with variable parmeters"""
        theta = Parameter('θ')
        theta_gate = Gate('test', 1, params=[theta])
        self.assertEqual(theta_gate.name, 'test')
        self.assertIsInstance(theta_gate.params[0], Parameter)

    def test_compile_quantum_circuit(self):
        """Test instantiating gate with variable parmeters"""
        theta = Parameter('θ')
        qr = QuantumRegister(1)
        qc = QuantumCircuit(qr)
        qc.rx(theta, qr)
        backend = BasicAer.get_backend('qasm_simulator')
        qc_aer = transpile(qc, backend)
        qobj = assemble(qc_aer)
        self.assertIn(theta, qobj.experiments[0].instructions[0].params)

    def test_get_variables(self):
        """Test instantiating gate with variable parmeters"""
        from qiskit.extensions.standard.rx import RXGate
        theta = Parameter('θ')
        qr = QuantumRegister(1)
        qc = QuantumCircuit(qr)
        rxg = RXGate(theta)
        qc.append(rxg, [qr[0]], [])
        vparams = qc.variable_table
        self.assertEqual(len(vparams), 1)
        self.assertIs(theta, next(iter(vparams)))
        self.assertIs(rxg, vparams[theta][0][0])

    def test_fix_variable(self):
        """Test setting a varaible to a constant value"""
        theta = Parameter('θ')
        qr = QuantumRegister(1)
        qc = QuantumCircuit(qr)
        qc.rx(theta, qr)
        qc.u3(0, theta, 0, qr)
        qc.variable_table[theta] = 0.5
        self.assertEqual(qc.variable_table[theta][0][0].params[0], 0.5)
        self.assertEqual(qc.variable_table[theta][1][0].params[1], 0.5)
        qc.variable_table[theta] = 0.6
        self.assertEqual(qc.variable_table[theta][0][0].params[0], 0.6)
        self.assertEqual(qc.variable_table[theta][1][0].params[1], 0.6)

    def test_multiple_variables(self):
        """Test setting multiple variables"""
        theta = Parameter('θ')
        x = Parameter('x')
        qr = QuantumRegister(1)
        qc = QuantumCircuit(qr)
        qc.rx(theta, qr)
        qc.u3(0, theta, x, qr)
        self.assertEqual(qc.variables, {theta, x})

    def test_circuit_generation(self):
        """Test creating a series of circuits parametrically"""
        theta = Parameter('θ')
        qr = QuantumRegister(1)
        qc = QuantumCircuit(qr)
        qc.rx(theta, qr)
        backend = BasicAer.get_backend('qasm_simulator')
        qc_aer = transpile(qc, backend)

        # generate list of circuits
        circs = []
        theta_list = numpy.linspace(0, numpy.pi, 20)
        for theta_i in theta_list:
            circs.append(qc_aer.assign_variables({theta: theta_i}))
        qobj = assemble(circs)
        for index, theta_i in enumerate(theta_list):
            self.assertEqual(qobj.experiments[index].instructions[0].params[0],
                             theta_i)

    def test_circuit_composition(self):
        """Test preservation of variables when combining circuits."""
        theta = Parameter('θ')
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        qc1 = QuantumCircuit(qr)
        qc1.rx(theta, qr)

        phi = Parameter('phi')
        qc2 = QuantumCircuit(qr, cr)
        qc2.ry(phi, qr)
        qc2.h(qr)
        qc2.measure(qr, cr)

        qc3 = qc1 + qc2
        self.assertEqual(qc3.variables, {theta, phi})

    def test_composite_instruction(self):
        """Test preservation of variables when combining circuits."""
        theta = Parameter('θ')
        qr1 = QuantumRegister(1, name='qr1')
        qc1 = QuantumCircuit(qr1)
        qc1.rx(theta, qr1)
        qc1.rz(numpy.pi/2, qr1)
        qc1.ry(theta, qr1)
        gate = qc1.to_instruction()
        self.assertEqual(gate.params, [theta, numpy.pi/2, theta])

        phi = Parameter('phi')
        qr2 = QuantumRegister(3, name='qr2')
        qc2 = QuantumCircuit(qr2)
        qc2.ry(phi, qr2[0])
        qc2.h(qr2)
        qc2.append(gate, qargs=[qr2[1]])
        self.assertEqual(qc2.variables, {theta, phi})

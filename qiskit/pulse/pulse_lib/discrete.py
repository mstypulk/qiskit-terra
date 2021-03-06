# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=missing-return-doc, invalid-name

"""Module for builtin discrete pulses.

Note the sampling strategy use for all discrete pulses is `left`.
"""

from qiskit.pulse.commands import SamplePulse
from qiskit.pulse.pulse_lib import continuous
from qiskit.pulse import samplers


_sampled_constant_pulse = samplers.left(continuous.constant)


def constant(duration: int, amp: complex) -> SamplePulse:
    """Generates constant-sampled `SamplePulse`.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Complex pulse amplitude.
    """
    return _sampled_constant_pulse(duration, amp)


_sampled_zero_pulse = samplers.left(continuous.zero)


def zero(duration: int) -> SamplePulse:
    """Generates zero-sampled `SamplePulse`.

    Args:
        duration: Duration of pulse. Must be greater than zero.
    """
    return _sampled_zero_pulse(duration)


_sampled_square_pulse = samplers.left(continuous.square)


def square(duration: int, amp: complex, period: float = None, phase: float = 0) -> SamplePulse:
    """Generates square wave `SamplePulse`.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude. Wave range is [-amp, amp].
        period: Pulse period, units of dt. If `None` defaults to single cycle.
        phase: Pulse phase.
    """
    if period is None:
        period = duration

    return _sampled_square_pulse(duration, amp, period, phase=phase)


_sampled_sawtooth_pulse = samplers.left(continuous.sawtooth)


def sawtooth(duration: int, amp: complex, period: float = None, phase: float = 0) -> SamplePulse:
    """Generates sawtooth wave `SamplePulse`.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude. Wave range is [-amp, amp].
        period: Pulse period, units of dt. If `None` defaults to single cycle.
        phase: Pulse phase.
    """
    if period is None:
        period = duration

    return _sampled_sawtooth_pulse(duration, amp, period, phase=phase)


_sampled_triangle_pulse = samplers.left(continuous.triangle)


def triangle(duration: int, amp: complex, period: float = None, phase: float = 0) -> SamplePulse:
    """Generates triangle wave `SamplePulse`.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude. Wave range is [-amp, amp].
        period: Pulse period, units of dt. If `None` defaults to single cycle.
        phase: Pulse phase.
    """
    if period is None:
        period = duration

    return _sampled_triangle_pulse(duration, amp, period, phase=phase)


_sampled_cos_pulse = samplers.left(continuous.cos)


def cos(duration: int, amp: complex, freq: float = None, phase: float = 0) -> SamplePulse:
    """Generates cosine wave `SamplePulse`.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude.
        freq: Pulse frequency, units of 1/dt. If `None` defaults to single cycle.
        phase: Pulse phase.
    """
    if freq is None:
        freq = 1/duration

    return _sampled_cos_pulse(duration, amp, freq, phase=phase)


_sampled_sin_pulse = samplers.left(continuous.sin)


def sin(duration: int, amp: complex, freq: float = None, phase: float = 0) -> SamplePulse:
    """Generates sine wave `SamplePulse`.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude.
        freq: Pulse frequency, units of 1/dt. If `None` defaults to single cycle.
        phase: Pulse phase.
    """
    if freq is None:
        freq = 1/duration

    return _sampled_sin_pulse(duration, amp, freq, phase=phase)


_sampled_gaussian_pulse = samplers.left(continuous.gaussian)


def gaussian(duration: int, amp: complex, sigma: float) -> SamplePulse:
    r"""Generates unnormalized gaussian `SamplePulse`.

    Centered at `duration/2` and zeroed at `t=-1` to prevent large initial discontinuity.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Integrated area under curve is $\Omega_g(amp, sigma) = amp \times np.sqrt(2\pi \sigma^2)$

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude at `duration/2`.
        sigma: Width (standard deviation) of pulse.
    """
    center = duration/2
    zeroed_width = duration + 2
    return _sampled_gaussian_pulse(duration, amp, center, sigma,
                                   zeroed_width=zeroed_width, rescale_amp=True)


_sampled_gaussian_deriv_pulse = samplers.left(continuous.gaussian_deriv)


def gaussian_deriv(duration: int, amp: complex, sigma: float) -> SamplePulse:
    r"""Generates unnormalized gaussian derivative `SamplePulse`.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude at `center`.
        sigma: Width (standard deviation) of pulse.
    """
    center = duration/2
    return _sampled_gaussian_deriv_pulse(duration, amp, center, sigma)


_sampled_gaussian_square_pulse = samplers.left(continuous.gaussian_square)


def gaussian_square(duration: int, amp: complex, sigma: float, risefall: int) -> SamplePulse:
    """Generates gaussian square `SamplePulse`.

    Centered at `duration/2` and zeroed at `t=-1` and `t=duration+1` to prevent
    large initial/final discontinuities.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude.
        sigma: Width (standard deviation) of gaussian rise/fall portion of the pulse.
        risefall: Number of samples over which pulse rise and fall happen. Width of
            square portion of pulse will be `duration-2*risefall`.
    """
    center = duration/2
    width = duration-2*risefall
    zeroed_width = duration + 2
    return _sampled_gaussian_square_pulse(duration, amp, center, width, sigma,
                                          zeroed_width=zeroed_width)


_sampled_drag_pulse = samplers.left(continuous.drag)


def drag(duration: int, amp: complex, sigma: float, beta: float) -> SamplePulse:
    r"""Generates Y-only correction DRAG `SamplePulse` for standard nonlinear oscillator (SNO) [1].

    Centered at `duration/2` and zeroed at `t=-1` to prevent large initial discontinuity.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    [1] Gambetta, J. M., Motzoi, F., Merkel, S. T. & Wilhelm, F. K.
        Analytic control methods for high-fidelity unitary operations
        in a weakly nonlinear oscillator. Phys. Rev. A 83, 012308 (2011).


    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude at `center`.
        sigma: Width (standard deviation) of pulse.
        beta: Y correction amplitude. For the SNO this is $\beta=-\frac{\lambda_1^2}{4\Delta_2}$.
            Where $\lambds_1$ is the relative coupling strength between the first excited and second
            excited states and $\Delta_2$ is the detuning between the resepective excited states.
    """
    center = duration/2
    zeroed_width = duration + 2
    return _sampled_drag_pulse(duration, amp, center, sigma, beta,
                               zeroed_width=zeroed_width, rescale_amp=True)

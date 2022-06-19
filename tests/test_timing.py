import time
from joelsutilities import timing


def test_timing_registrar():
    # create registrar with sample delayer function
    reg = timing.TimingRegistrar()

    @reg.register_function
    def sample_func(x: float):
        time.sleep(x)

    # run function twice
    sample_func(0.1)
    sample_func(0.2)

    # check function exists in registrar and 2 instances exist
    assert 'sample_func' in reg.timings
    assert len(reg['sample_func']) == 2

    # check timings are correct
    t0 = reg['sample_func'][0].total_seconds()
    t1 = reg['sample_func'][1].total_seconds()

    assert t0 >= 0.09
    assert t1 >= 0.19

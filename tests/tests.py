import unittest
import time
from datetime import datetime
from datetime import timedelta
from joelutilities import dates, registrar, timing, dictionaries


class UtilsTesting(unittest.TestCase):
    def test_date_formatting(self):
        td = timedelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6)
        for x in [{
            'formatter': '{d:02}:{h:02}:{m:02}:{s:02}:{ms:03}',
            'expected': "02:03:04:05:006"
        }, {
            'formatter': '{d:02}:{h:02}:{m:02}:{s:02}:{u:06}',
            'expected': "02:03:04:05:006000"
        }]:
            formatted = dates.format_timedelta(td, x['formatter'])
            self.assertTrue(formatted == x['expected'], f'expected "{x["expected"]}", got "{formatted}"')

    def test_localist(self):
        dates.localise(datetime.now()).tzinfo == dates.TZ_LONDON

    def test_timing_registrar(self):
        # create registrar with sample delayer function
        reg = timing.TimingRegistrar()
        @reg.register_function
        def sample_func(x: float):
           time.sleep(x)

        # run function twice
        sample_func(0.1)
        sample_func(0.2)

        # check function exists in registrar and 2 instances exist
        self.assertTrue('sample_func' in reg.timed_functions())
        self.assertTrue(len(reg['sample_func']) == 2)

        # check timings are correct
        self.assertTrue(reg['sample_func'][0].total_seconds() > 0.1)
        self.assertTrue(reg['sample_func'][1].total_seconds() > 0.2)

    def test_dict_subset(self):
        T = lambda inner, outer: self.assertTrue(dictionaries.is_dict_subset(inner, outer))
        F = lambda inner, outer: self.assertFalse(dictionaries.is_dict_subset(inner, outer))

        T(
            {'a': 1},
            {'a': 1, 'b': 2}
        )
        T(
            {},
            {'a': 1}
        )
        T(
            {},
            {}
        )
        F(
            {'a': {}},
            {}
        )
        F(
            {'a': {'b':2}},
            {'a': {'b': 3}}
        )
        T(
            {'a': {'b': {'c': 1}}},
            {'a': {'b': {'c': 1, 'd': 2}}}
        )

    def test_dict_update(self):
        x = {'a': 1, 'b':2}
        dictionaries.dict_update({'b': {'c': 1}}, x)
        self.assertTrue(x == {'a': 1, 'b': {'c': 1}})


if __name__ == "__main__":
    unittest.main(verbosity=2)

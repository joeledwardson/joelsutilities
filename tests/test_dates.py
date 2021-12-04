from datetime import datetime
from datetime import timedelta
import pytz
from joelsutilities import dates


def test_date_formatting():
    td = timedelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6)
    for x in [{
        'formatter': '{d:02}:{h:02}:{m:02}:{s:02}:{ms:03}',
        'expected': "02:03:04:05:006"
    }, {
        'formatter': '{d:02}:{h:02}:{m:02}:{s:02}:{u:06}',
        'expected': "02:03:04:05:006000"
    }]:
        formatted = dates.format_timedelta(td, x['formatter'])
        assert formatted == x['expected']


def test_localise():
    assert dates.localise(datetime.now()).tzinfo == datetime.now(pytz.timezone('Europe/London')).tzinfo

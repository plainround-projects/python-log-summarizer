from logsum.infrastructure.clock import SystemClock
from logsum.infrastructure.memory import TracemallocMeter


def test_the_system_clock_never_goes_backwards():
    clock = SystemClock()
    first = clock.monotonic()
    assert clock.monotonic() >= first


def test_the_meter_reports_a_peak_that_covers_a_large_allocation():
    meter = TracemallocMeter()
    meter.start()
    block = bytearray(5_000_000)
    del block
    peak = meter.stop()
    assert peak >= 5_000_000


def test_the_meter_can_be_used_twice_and_forgets_the_first_run():
    meter = TracemallocMeter()
    meter.start()
    big = bytearray(5_000_000)
    del big
    meter.stop()
    meter.start()
    small = bytearray(1000)
    peak = meter.stop()
    assert len(small) == 1000
    assert peak < 1_000_000

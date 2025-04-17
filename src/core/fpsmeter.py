import time 

class FPSMeter:
    """Simple FPS meter class"""

    def __init__(self, avg_len: int = 100):
        """Constructor

        avg_len - number of samples to average
        """
        self._avg_len = avg_len
        self.reset()

    def reset(self):
        """Reset accumulators"""
        self._timestamp_ns = -1
        self._duration_ns = -1
        self._count = 0

    def record(self) -> float:
        """Record timestamp and update average duration.

        Returns current average FPS"""
        t = time.time_ns()
        if self._timestamp_ns > 0:
            cur_dur_ns = t - self._timestamp_ns
            self._count = min(self._count + 1, self._avg_len)
            self._duration_ns = (
                self._duration_ns * (self._count - 1) + cur_dur_ns
            ) // self._count
        self._timestamp_ns = t
        return self.fps()

    def fps(self) -> float:
        """Return current average FPS"""
        return 1e9 / self._duration_ns if self._duration_ns > 0 else 0

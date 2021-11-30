import random
import time


START_TIME = int(time.time()*1000)


def make_identifier():
    # Source:
    # https://stackoverflow.com/a/37605582/7899348

	t = int(time.time()*1000) - START_TIME
	u = random.SystemRandom().getrandbits(23)
	return (t << 23) | u


def reverse_identifier(identifier):
	t = identifier >> 23
	return t + START_TIME

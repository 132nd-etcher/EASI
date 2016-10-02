# coding=utf-8

import time

import ntplib

epoch_timer = None
epoch_cache = None


# TODO: expoch needs to be a class with static method to instantiate online and online cached, and easy conversion to time with the pendulum module

def epoch_cached_online(ttl=300):
    now = time.time()
    global epoch_timer, epoch_cache
    if epoch_timer is None:
        epoch_timer = now
        epoch_cache = epoch_online()
    elif now - epoch_timer > ttl:
        epoch_cache = epoch_online()
    return epoch_cache


def epoch_online(pool=None):
    """
    Gets the epoch from the first available NTP server
    :return: online epoch
    """
    if pool is None:
        pool = [
            '0.fr.pool.ntp.org',
            '1.fr.pool.ntp.org',
            '2.fr.pool.ntp.org',
            '3.fr.pool.ntp.org',
            '2.be.pool.ntp.org',
            '3.europe.pool.ntp.org',
            '2.europe.pool.ntp.org',
            '0.ca.pool.ntp.org',
            '1.ca.pool.ntp.org',
            '2.ca.pool.ntp.org',
            '3.ca.pool.ntp.org',
            'pool.ntp.org',
        ]
    client = ntplib.NTPClient()
    try:
        server = pool.pop()
        resp = client.request(server)
        epoch = resp.tx_time
        return epoch
    except ntplib.NTPException:
        if len(pool) > 0:
            return epoch_online(pool)
        else:
            raise


def epoch_to_time(epoch, fmt_str='%Y-%m-%d %HH:%MM:%SS'):
    """Convert epoch to readable string"""
    return time.strftime(fmt_str, time.localtime(epoch))

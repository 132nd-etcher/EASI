# coding=utf-8

import time
import pendulum

import ntplib

epoch_timer = None
epoch_cache = None


# TODO: expoch needs to be a class with static method to instantiate online and online cached,
# and easy conversion to time with the pendulum module


class Epoch:
    epoch_timer = None
    epoch_cache = None
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

    @staticmethod
    def epoch_online(pool=None):
        """
        Gets the epoch from the first available NTP server
        :return: online epoch
        """
        if pool is None:
            pool = [x for x in Epoch.pool]
        client = ntplib.NTPClient()
        try:
            server = pool.pop()
            resp = client.request(server)
            epoch = resp.tx_time
            return epoch
        except ntplib.NTPException:
            if len(pool) > 0:
                return Epoch.epoch_online(pool)
            else:
                raise

    @staticmethod
    def epoch_cached_online(ttl=60):
        now = time.time()
        if Epoch.epoch_timer is None:
            Epoch.epoch_timer = now
            Epoch.epoch_cache = Epoch.epoch_online()
        elif now - Epoch.epoch_timer > ttl:
            Epoch.epoch_cache = Epoch.epoch_online()
        return Epoch.epoch_cache

    @staticmethod
    def now(refresh=False) -> pendulum.Pendulum:
        if refresh:
            return pendulum.from_timestamp(Epoch.epoch_online())
        return pendulum.from_timestamp(Epoch.epoch_cached_online())

    @staticmethod
    def datetime_string(refresh=False) -> str:
        return Epoch.now(refresh).to_datetime_string()

    @staticmethod
    def to_iso8601(refresh=False) -> str:
        return Epoch.now(refresh).to_iso8601_string()

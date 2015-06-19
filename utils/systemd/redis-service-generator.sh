#!/bin/sh -e

FSROOTDIR="$INSTALLROOT"

/usr/lib/redis/systemd-confd-generator.sh  "${FSROOTDIR}/etc/redis/server.conf.d" "${FSROOTDIR}/usr/lib/systemd/system/redis-server-instance@.service" "${FSROOTDIR}/usr/lib/systemd/system/redis-server.wants"

exec /usr/lib/redis/systemd-confd-generator.sh  "${FSROOTDIR}/etc/redis/sentinel.conf.d" "${FSROOTDIR}/usr/lib/systemd/system/redis-sentinel-instance@.service" "${FSROOTDIR}/usr/lib/systemd/system/redis-sentinel.wants"


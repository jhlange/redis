Name:		redis
Release:	1%{?dist}
Summary:	A persistent key-value database
Group:		Applications/Databases
License:	BSD
URL:		http://redis.io/
%if "%{tarfile}" != ""
%define tarbasename() %(echo %tarfile )
%else
%define tarbasename() %(echo %name-%release )
%endif
%define untardirectoryname() %(tar -tzf %{SOURCE0} |head -1 |sed s#\/.*##)
Source:		%tarbasename.tar.gz
Version:	%(tar -xzf  %{SOURCE0} %{tarbasename}/src/version.h -O | sed -n "s#.*REDIS_VERSION.*\"\(.*\)\".*#\1#p")

BuildRequires:	gcc, make
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(post):	systemd

%description
Redis is an open source, BSD licensed, advanced key-value cache and store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets, sorted sets, bitmaps and hyperloglogs.

You can run atomic operations on these types, like appending to a string; incrementing the value in a hash; pushing an element to a list; computing set intersection, union and difference; or getting the member with highest ranking in a sorted set.

In order to achieve its outstanding performance, Redis works with an in-memory dataset. Depending on your use case, you can persist it either by dumping the dataset to disk every once in a while, or by appending each command to a log. Persistence can be optionally disabled, if you just need a feature-rich, networked, in-memory cache.

Redis also supports trivial-to-setup master-slave asynchronous replication, with very fast non-blocking first synchronization, auto-reconnection with partial resynchronization on net split.

%prep
%setup -n %untardirectoryname

%build
make %{?_smp_mflags}

%install
make install PREFIX=%{buildroot}/usr
mkdir -m 755 -p %{buildroot}/etc/redis/server.conf.d/
mkdir -m 755 -p %{buildroot}/etc/redis/sentinel.conf.d/
mkdir -m 755 -p %{buildroot}/etc/redis/sentinel.conf.d/
mkdir -m 755 -p %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/rpm/redis-server-instance@.service %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/rpm/redis-sentinel-instance@.service %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/rpm/redis-server.target %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/rpm/redis-sentinel.target %{buildroot}/usr/lib/systemd/system/
mkdir -m 755 -p %{buildroot}/usr/lib/redis/
install -m 755 utils/rpm/systemd-confd-generator.sh %{buildroot}/usr/lib/redis/
mkdir -m 755 -p %{buildroot}/usr/lib/systemd/system-generators/
install -m 755 utils/rpm/redis-service-generator.sh %{buildroot}/usr/lib/systemd/system-generators/ 
install -m 755 utils/rpm/redis-createconfig %{buildroot}/usr/bin
mkdir -m 755 -p %{buildroot}/usr/share/redis/
install -m 644 redis.conf %{buildroot}/usr/share/redis/
install -m 644 sentinel.conf %{buildroot}/usr/share/redis/
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/run/%{name}

%files
%defattr(-,root,root)
/usr/bin/redis-benchmark
/usr/bin/redis-check-aof
/usr/bin/redis-check-rdb
/usr/bin/redis-cli
/usr/bin/redis-sentinel
/usr/bin/redis-server
/etc/redis/server.conf.d
/etc/redis/sentinel.conf.d
/usr/lib/systemd/system/redis-server-instance@.service
/usr/lib/systemd/system/redis-sentinel-instance@.service
/usr/lib/systemd/system/redis-server.target
/usr/lib/systemd/system/redis-sentinel.target
/usr/lib/redis
/usr/lib/systemd/system-generators/redis-service-generator.sh
/usr/share/redis
/usr/bin/redis-createconfig
%dir %attr(0750, redis, redis) %{_sharedstatedir}/%{name}
%dir %attr(0750, redis, redis) %{_localstatedir}/log/%{name}
%dir %attr(0750, redis, redis) %{_localstatedir}/run/%{name}

%pre
/usr/bin/getent group redis || /usr/sbin/groupadd -r redis

/usr/bin/getent passwd redis || /usr/sbin/useradd -r -d /var/run/redis -m  -s /sbin/nologin -g redis redis

%post
systemctl daemon-reload
systemctl enable redis-server.target
systemctl enable redis-sentinel.target
echo ""
echo "You must generate a redis configuration post install if you wish to use a server."
echo "You may do so now with: sudo redis-createconfig --type redis default"
echo ""

%changelog
* Fri Jun 19 2015 - josh (at) joshlange.net
- Initial packaging or redis into a modern RPM spec.

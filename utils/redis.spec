Name:		redis
Version:	1.0.0
#Release:	1%{?dist}
Release:	unstable
Summary:	The Redis client and server

Group:		Applications/Databases
License:	BSD
URL:		http://redis.io/
Source:		%name-%release.tar.gz

BuildRequires:	gcc, sh, make
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires:	sh, systemd

%description
A light weight in memory database

%prep
%setup -q


%build
#%configure
make %{?_smp_mflags}


%install
make install PREFIX=%{buildroot}/usr
mkdir -m 755 -p %{buildroot}/etc/redis/server.conf.d/
mkdir -m 755 -p %{buildroot}/etc/redis/sentinel.conf.d/
mkdir -m 755 -p %{buildroot}/etc/redis/sentinel.conf.d/
install -m 644 utils/systemd/redis-server-instance@.service %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/systemd/redis-sentinel-instance@.service %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/systemd/redis-server.target %{buildroot}/usr/lib/systemd/system/
install -m 644 utils/systemd/redis-sentinel.target %{buildroot}/usr/lib/systemd/system/
mkdir -m 755 -p %{buildroot}/usr/lib/redis/
install -m 755 utils/systemd/systemd-confd-generator.sh %{buildroot}/usr/lib/redis/
install -m 755 utils/systemd/redis-service-generator.sh %{buildroot}/usr/lib/systemd/system-generators/ 
install -m 755 utils/systemd/redis-createconfig %{buildroot}/usr/bin
mkdir -m 755 -p %{buildroot}/usr/share/redis/
install -m 644 redis.conf %{buildroot}/usr/share/redis/
install -m 644 sentinel.conf %{buildroot}/usr/share/redis/

%files
%defattr(-,root,root)
/usr/bin/redis-benchmark(755,root,root)
/usr/bin/redis-check-aof(755,root,root)
/usr/bin/redis-check-rdb(755,root,root)
/usr/bin/redis-cli(755,root,root)
/usr/bin/redis-sentinel(755,root,root)
/usr/bin/redis-server(755,root,root)
/etc/redis/server.conf.d(755,root,root)
/etc/redis/sentinel.conf.d(755,root,root)
/usr/lib/systemd/system/redis-server-instance@.service(644,root,root)
/usr/lib/systemd/system/redis-sentinel-instance@.service(644,root,root)
/usr/lib/systemd/system/redis-server.target(644,root,root)
/usr/lib/systemd/system/redis-sentinel.target(644,root,root)
/usr/lib/redis(755,root,root)
/usr/lib/redis/systemd-confd-generator.sh(755,root,root)
/usr/lib/systemd/system-generators/redis-service-generator.sh(755,root,root)
/usr/share/redis(755,root,root)
/usr/share/redis/redis.conf(644,root,root)
/usr/share/redis/sentinel.conf(644,root,root)

%pre
/usr/bin/getent group redis || /usr/sbin/groupadd -r redis
/usr/bin/getent passwd redis || /usr/sbin/useradd -r -d /var/lib/redis -m  -s /sbin/nologin redis

%post
systemctl daemon-reload
systemctl enable redis-server.target
systemctl enable redis-sentinel.target

%changelog


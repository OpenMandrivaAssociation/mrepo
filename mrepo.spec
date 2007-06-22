# $Id$
# Upstream: Dag Wieers <dag$wieers,com>

Summary: Tool to set up a Yum/Apt mirror from various sources (ISO, RHN, rsync, http, ftp, ...)
Name: mrepo
Version: 0.8.4
Packager: Bruno Cornec <bcornec@mandriva.org>
Release: %mkrel 1
License: GPL
Group: System/Configuration/Packaging
URL: http://dag.wieers.com/home-made/mrepo/
Source: http://dag.wieers.com/home-made/mrepo/mrepo-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)

BuildArch: noarch
Requires: python >= 2.0, createrepo

%description
mrepo builds a local Apt/Yum RPM repository from local ISO files,
downloaded updates and extra packages from RHN and 3rd party
repositories.

It can download all updates and extras automatically, creates
the repository structure and meta-data, enables HTTP access to
the repository and creates a directory-structure for remote
network installations using PXE/TFTP.

mrepo supports ftp, http, sftp, rsync, rhn and other download methods.

With mrepo, you can enable your laptop or a local server to provide
updates for the whole network and provide the proper files to
allow installations via the network.

%prep
%setup

%{__perl} -pi.orig -e 's|^(VERSION)\s*=\s*.+$|$1 = "%{version}"|' mrepo

%{__cat} <<EOF >config/mrepo.cron
### Enable this if you want mrepo to daily synchronize
### your distributions and repositories at 2:30am.
#30 2 * * * root /usr/bin/mrepo -q -ug
EOF

%{__cat} <<EOF >config/mrepo.conf
### Configuration file for mrepo

### The [main] section allows to override mrepo's default settings
### The mrepo-example.conf gives an overview of all the possible settings
[main]
srcdir = /var/mrepo
wwwdir = /var/www/mrepo
confdir = /etc/mrepo.conf.d
arch = i386

mailto = root@localhost
smtp-server = localhost

#rhnlogin = username:password

### Any other section is considered a definition for a distribution
### You can put distribution sections in /etc/mrepo.conf.d/
### Examples can be found in the documentation at:
###     %{_docdir}/%{name}-%{version}/dists/.
EOF

%build

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%preun
if [ $1 -eq 0 ]; then
	/etc/init.d/mrepo stop &>/dev/null || :
	/sbin/chkconfig --del mrepo
fi

%post
/sbin/chkconfig --add mrepo

#%postun
#/sbin/service mrepo condrestart &>/dev/null || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README THANKS TODO WISHLIST config/*.conf config/dists/ docs/
%config(noreplace) %{_sysconfdir}/cron.d/mrepo
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mrepo.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/mrepo
%config(noreplace) %{_sysconfdir}/mrepo.conf
%config(noreplace) %{_sysconfdir}/mrepo.conf.d/
%config %{_initrddir}/mrepo
%{_bindir}/gensystemid
%{_bindir}/rhnget
%{_bindir}/mrepo
%{_datadir}/mrepo/
#%{_localstatedir}/cache/mrepo/
#%{_localstatedir}/www/mrepo/
#%{_localstatedir}/mrepo/
/var/cache/mrepo/
/var/www/mrepo/
/var/mrepo/

# $Id$
# Upstream: Dag Wieers <dag$wieers,com>

Summary: Tool to set up a Yum/Apt mirror from various sources
Name: mrepo
Version: 0.8.7
Packager: Bruno Cornec <bcornec@mandriva.org>
Release: 2
License: GPL
Group: System/Configuration/Packaging
URL: http://dag.wieers.com/home-made/mrepo/
Source: http://dag.wieers.com/home-made/mrepo/%{name}-%{version}.tar.bz2

BuildArch: noarch
Requires: python >= 2.0, createrepo

%description
Tool to set up a Yum/Apt mirror from various sources 
(ISO, RHN, rsync, http, ftp, ...).

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
arch = i386 x86_64

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
%{_bindir}/youget
%{_datadir}/mrepo/
#%{_localstatedir}/lib/cache/mrepo/
#%{_localstatedir}/lib/www/mrepo/
#%{_localstatedir}/lib/mrepo/
/var/cache/mrepo/
/var/www/mrepo/
/var/mrepo/


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8.6-3mdv2011.0
+ Revision: 620409
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 0.8.6-2mdv2010.0
+ Revision: 440152
- rebuild

* Fri Nov 28 2008 Bruno Cornec <bcornec@mandriva.org> 0.8.6-1mdv2009.1
+ Revision: 307416
- Fix another rpmlint error
- Fix rpmlint warnings
- youget is now part of files installed
- Add mrepo 0.8.6 sources
- Update to mrepo 0.8.6

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.8.4-3mdv2009.0
+ Revision: 241049
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 22 2007 Bruno Cornec <bcornec@mandriva.org> 0.8.4-1mdv2008.0
+ Revision: 43073
- Update from original DAG spec file to mandriva specificities
- Import mrepo



* Wed Dec 13 2006 Dag Wieers <dag@wieers.com> - 0.8.4-1 - +/
- Updated to release 0.8.4.
- Package renamed from yam to mrepo.

* Sat Oct 21 2006 Dag Wieers <dag@wieers.com> - 0.8.3-2
- Get rid of specific createrepo version now that Yam works with upstream.

* Sun Oct 15 2006 Dag Wieers <dag@wieers.com> - 0.8.3-1
- Updated to release 0.8.3.

* Wed Sep 20 2006 Dag Wieers <dag@wieers.com> - 0.8.2-1
- Updated to release 0.8.2.

* Fri Mar 10 2006 Dag Wieers <dag@wieers.com> - 0.8.0-2
- Added gensystemid to installation. (Ian Forde)

* Thu Mar 09 2006 Dag Wieers <dag@wieers.com> - 0.8.0-1
- Updated to release 0.8.0.

* Fri Mar 25 2005 Dag Wieers <dag@wieers.com> - 0.7.3-1
- Updated to release 0.7.3.

* Fri Jan 07 2005 Dag Wieers <dag@wieers.com> - 0.7.2-2
- Add %%post and %%postun scripts. (Bert de Bruijn)

* Fri Dec 31 2004 Dag Wieers <dag@wieers.com> - 0.7.2-1
- Updated to release 0.7.2.

* Sun Nov 07 2004 Dag Wieers <dag@wieers.com> - 0.7.1-1
- Updated to release 0.7.1.

* Sun Oct 10 2004 Dag Wieers <dag@wieers.com> - 0.7-1
- Updated to release 0.7.

* Fri Aug 27 2004 Dag Wieers <dag@wieers.com> - 0.6.1-1
- Updated to release 0.6.1.

* Wed Aug 25 2004 Dag Wieers <dag@wieers.com> - 0.6-2
- Updated to release 0.6.
- Fix a version problem.

* Thu Aug 19 2004 Dag Wieers <dag@wieers.com> - 0.5-1
- Updated to release 0.5.

* Wed May 19 2004 Dag Wieers <dag@wieers.com> - 0.3-1
- Updated to release 0.3.

* Fri May 14 2004 Dag Wieers <dag@wieers.com> - 0.2-1
- Initial package. (using DAR)


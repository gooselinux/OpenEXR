
%if 0%{?fedora} > 7 || 0%{?rhel} >= 6
# make -libs subpkg
%define libs 1
%endif

Name:	 OpenEXR
Version: 1.6.1
Release: 8.1%{?dist}
Summary: A high dynamic-range (HDR) image file format

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/openexr-%{version}.tar.gz
Source1: http://download.savannah.nongnu.org/releases/openexr/openexr-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: openexr < %{version}-%{release}
Provides:  openexr = %{version}-%{release}

Patch1: OpenEXR-1.6.1-pkgconfig.patch
Patch2: openexr-1.6.1-gcc43.patch

## upstream patches
Patch100: openexr-1.6.1-CVE-2009-1720-1.patch 
Patch101: openexr-1.6.1-CVE-2009-1720-2.patch
Patch102: openexr-1.6.1-CVE-2009-1721.patch

BuildRequires:  automake libtool
BuildRequires:  ilmbase-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig

%if 0%{?libs}
Requires: %{name}-libs = %{version}-%{release}
%else
Obsoletes: %{name}-libs < %{version}-%{release}
Provides:  %{name}-libs = %{version}-%{release}
%endif

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Group:	 Development/Libraries
Obsoletes: openexr-devel < %{version}-%{release}
Provides:  openexr-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ilmbase-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries
%description libs
%{summary}.


%prep
%setup -q -n openexr-%{version}

%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .gcc43

%patch100 -p1 -b .CVE-2009-1720-1
%patch101 -p1 -b .CVE-2009-1720-2
%patch102 -p1 -b .CVE-2009-1721

# work to remove rpaths, recheck on new releases
aclocal -Im4
libtoolize --force
rm -f configure
autoconf


%build
%configure --disable-static

# hack to omit unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la

# prepare docs
mkdir -p rpmdocs
cp -a IlmImfExamples rpmdocs/examples
rm -rf rpmdocs/examples/.deps


%check
# Not enabled, by default, takes a *very* long time. -- Rex
%{?_with_check:make check}


%clean
rm -rf $RPM_BUILD_ROOT


%post %{?libs:libs} -p /sbin/ldconfig

%postun %{?libs:libs}  -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*

%if 0%{?libs}
%files libs
%defattr(-,root,root,-)
%endif
%doc AUTHORS ChangeLog LICENSE NEWS README
%{_libdir}/libIlmImf.so.6*

%files devel
%defattr(-,root,root,-)
#omit for now, they're mostly useless, and include multilib conflicts (#342781)
#doc rpmdocs/examples 
%{_datadir}/aclocal/openexr.m4
%{_includedir}/OpenEXR/*
%{_libdir}/libIlmImf.so
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.6.1-8.1
- Fix conditional for RHEL

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-8
- CVE-2009-1720 OpenEXR: Multiple integer overflows (#513995)
- CVE-2009-1721 OpenEXR: Invalid pointer free by image decompression (#514003)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Caolán McNamara <caolanm@redhat.com> 1.6.1-5
- rebuild to get provides pkgconfig(OpenEXR)

* Fri May 09 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-4
- drop: Obsoletes: OpenEXR-utils (see OpenEXR_Viewers review, bug #428228c3)

* Fri Feb 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- gcc43 patch
- purge rpaths

* Wed Jan 09 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-2
- hack to omit unused-direct-shlib-dependencies
- conditionalize -libs (f8+)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-1
- openexr-1.6.1

* Mon Oct 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-5
- multiarch conflicts in OpenEXR (#342781)
- don't own %%_includedir/OpenEXR (leave that to ilmbase)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-4
- -libs: %%post/%%postun -p /sbin/ldconfig

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-2
- openexr-1.6.0

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-6
- libs: -Requires: %%name

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-5
- -libs: new subpkg to be multilib friendly
- -utils: package exrdisplay separately (separate fltk dep)

* Sat Oct 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-4
- Obsoletes/Provides: openexr(-devel) (rpmforge compatibility)

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-3
- pkgconfig patch to use Libs.private

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-2
- -devel: +Requires: pkgconfig

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-1
- openexr-1.4.0a

* Sat Feb 18 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-7
- Further zlib fixes (#165729)

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-6
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-5
- Remove *.a from %%files devel

* Tue Aug 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-4
- Removed -devel dep on zlib-devel (#165729)
- Added --disable-static to %%configure
- Fixed build with GCC 4.0.1
- Added .so links to -devel

* Wed May 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-3
- Add zlib-devel to BR
- Delete all .la files (#157652)

* Mon May  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Add disttag

* Sun May  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Fix BuildRequires
- Fix Requires on -devel
- Add %%post[un] scriptlets
- Fix ownership in -devel
- Don't have .deps files in %%doc

* Wed Mar 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-1
- Initial RPM release

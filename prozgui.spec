#
# TODO:
# - waiting for "stable" tarball
# - build fails on:
#   /usr/lib/gcc/i686-pld-linux/4.2.0/include/stddef.h:152: error: declaration does not declare anything
#
Summary:	A GUI advanced Linux download manager
Summary(pl.UTF-8):	Zaawansowany program do ściągania plików z interfejsem graficznym
Name:		prozgui
Version:	2.0.5
%define	bver	beta
Release:	0.%{bver}.1
License:	GPL
Group:		Applications/Networking
Source0:	http://prozilla.genesys.ro/downloads/prozgui/tarballs/%{name}-%{version}%{bver}.tar.bz2
# Source0-md5:	b501ecce2844d411ba39be761027ac4e
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-po.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-include.patch
Patch3:		%{name}-gcc4.patch
URL:		http://prozilla.genesys.ro/?p=prozgui
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fltk-devel >= 1.1.0
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the GUI version of Prozilla. It uses libprozilla and the the
GUI is created and designed with The Fast Light Tool Kit (fltk).

ProZilla is a download accellerator program written for Linux to speed
up the normal file download process. It often gives speed increases of
around 200% to 300%. It supports both FTP and HTTP protocols, and the
theory behind it is very simple. The program opens multiple
connections to a server, and each of the connections downloads a part
of the file, thus defeating existing internet congestion prevention
methods which slow down a single connection based download.

%description -l pl.UTF-8
ProZilla jest programem typu "download accellerator" dla Linuksa
napisanym, aby przyspieszyć proces ściągania plików. Często daje
zwiększenie prędkości do 200-300%. Wspiera protokoły HTTP i FTP, a
jego teoretyczne działanie jest bardzo proste. Program otwiera wiele
połączeń do serwera i każde z nich ściąga tylko część pliku. Dzięki
temu możliwe jest ominięcie ograniczeń transferu nakładanych na
pojedyncze połączenie.

Interface został zaprojektowany i zbudowany w oparciu o bibliotekę
FLTK.

%package devel
Summary:	Header files for prozilla library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki prozilli
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for prozilla library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki prozilli.

%package static
Summary:	prozilla static library
Summary(pl.UTF-8):	Statyczna biblioteka prozilli
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
prozilla static library.

%description static -l pl.UTF-8
Statyczna biblioteka prozilli.

%prep
%setup -q -n %{name}-%{version}%{bver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

head -n 98 acinclude.m4 > acinclude.m4.tmp
mv -f acinclude.m4.tmp acinclude.m4
cp -f acinclude.m4 libprozilla

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd libprozilla
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--with-fltk-includes=%{_includedir} \
	--with-fltk-libs=%{_libdir} \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_includedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

mv -f man/prozgui.1 .
mv -f libprozilla/TODO libprozilla/TODO-devel
mv -f libprozilla/README libprozilla/README-devel
mv -f libprozilla/src/{prozilla.h,netrc.h} $RPM_BUILD_ROOT%{_includedir}

mv -f libprozilla/docs/HACKING libprozilla

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CREDITS* ChangeLog NEWS README TODO docs/FAQ
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libprozilla.so.*.*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/*.png
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc libprozilla/{TODO-devel,README-devel,HACKING}
%attr(755,root,root) %{_libdir}/libprozilla.so
%{_libdir}/libprozilla.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libprozilla.a

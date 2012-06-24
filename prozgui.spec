#
# TODO:
#
# waiting for "stable" tarball
#
Summary:	An GUI advanced Linux download manager
Summary(pl):	Zaawansowany program do �ci�gania plik�w z interfejsem graficznym
Name:		prozgui
Version:	2.0.4
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://prozilla.delrom.ro/packages/prozgui/tarballs/%{name}-%{version}beta3.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-acinclude.m4.patch
URL:		http://prozilla.delrom.ro/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fltk-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man

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

%description -l pl
ProZilla jest programem typu "download accellerator" dla Linuksa
napisanym, aby przyspieszy� proces �ci�gania plik�w. Cz�sto daje
zwi�kszenie pr�dko�ci do 200-300%. Wspiera protoko�y HTTP i FTP, a
jego teoretyczne dzia�anie jest bardzo proste. Program otwiera wiele
po��cze� do servera i ka�de z nich �ci�ga tylko cz�� pliku. Dzi�ki
temu mozliwe jest omini�cie ogranicze� transferu nak�adanych na
pojedyncze po��czenie.

Interface zosta� zaprojektowany i zbudowany w oparciu o bibliotek�
FLTK.

%package devel
Summary:	prozilla development files
Summary(pl):	Narz�dzia programistyczne dla prozilli
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
prozilla development files.

%description devel -l pl
Narz�dzia programistyczne dla prozilli.

%package static
Summary:	prozilla static library
Summary(pl):	Bilbioteka prozilli linkowana statycznie
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
prozilla static library.

%description static -l pl
Biblioteka prozilli linkowana statycznie.

%prep
%setup -q -n %{name}-%{version}beta3
%patch0 -p1

%build
rm -f missing acinclude.m4
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
cd libprozilla
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
cd ..
%configure \
    --with-fltk-includes=%{_includedir} \
    --with-fltk-libs=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Network/FTP} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_includedir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT prefix=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/FTP/%{name}.desktop
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

mv -f man/prozgui.1 .
mv -f libprozilla/TODO libprozilla/TODO-devel
mv -f libprozilla/README libprozilla/README-devel
mv -f libprozilla/src/{prozilla.h,netrc.h} $RPM_BUILD_ROOT%{_includedir}
mv -f $RPM_BUILD_ROOT/share/locale/ $RPM_BUILD_ROOT%{_datadir}

gzip -9nf AUTHORS CREDITS* ChangeLog NEWS README TODO docs/FAQ

mv -f libprozilla/docs/HACKING ./libprozilla/

gzip -9nf libprozilla/{TODO-devel,README-devel,HACKING}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/locale/*
%{_applnkdir}/Network/FTP/%{name}.desktop
%{_pixmapsdir}/*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc libprozilla/*.gz
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libprozilla*

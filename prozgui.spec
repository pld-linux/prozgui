#
# TODO:
#
# waiting for "stable" tarball
#
Summary:	An GUI advanced Linux download manager
Summary(pl):	Zaawansowany program do ¶ci±gania plików z interfejsem graficznym.
Name:		prozgui
Version:	2.0.4
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://prozilla.delrom.ro/packages/prozgui/tarballs/%{name}-%{version}beta3.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		http://prozilla.delrom.ro/
BuildRequires:	fltk-devel
Requires:	fltk
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
ProZilla jest programem typu "download accellerator" dla Linuxa
napisanym, aby przyspieszyæ proces ¶ci±gania plików. Czêsto daje
zwiêkszenie prêdko¶ci do 200-300%. Wspiera protoko³y HTTP i FTP, a
jego teoretyczne dzia³anie jest bardzo proste. Program otwiera wiele
po³±czeñ do servera i ka¿de z nich ¶ci±ga tylko czê¶æ programu. Dziêki
temu mozliwe jest ominiêcie ograniczeñ transferu nak³adanych na
pojedyncze po³±czenie.

Interface jest zaprojektowany i zbudowany z FLTK.

%package devel
Summary:	prozilla development files
Summary(pl):	Narzêdzia programistyczne dla prozilli
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
prozilla development files.

%description -l pl devel
Narzêdzia programistyczne dla prozilli.

%package static
Summary:	prozilla static library
Summary(pl):	Bilbioteka prozilli linkowana statycznie
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
prozilla static library.

%description -l pl static
Biblioteka prozilli linkowana statycznie.

%prep
%setup -q -n %{name}-%{version}beta3

%build
%configure2_13 \
    --with-fltk-includes=%{_includedir} \
    --with-fltk-libs=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Network/FTP} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_includedir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT prefix=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/FTP/%{name}.desktop
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/

mv man/prozgui.1 ./
mv libprozilla/TODO libprozilla/TODO-devel
mv libprozilla/README libprozilla/README-devel
mv libprozilla/src/{prozilla.h,netrc.h} $RPM_BUILD_ROOT%{_includedir}/
mv -f $RPM_BUILD_ROOT/share/locale/ $RPM_BUILD_ROOT%{_datadir}/

gzip -9nf AUTHORS CREDITS* ChangeLog NEWS README TODO docs/FAQ

mv libprozilla/docs/HACKING ./libprozilla/

gzip -9nf libprozilla/{TODO-devel,README-devel,HACKING}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc libprozilla/*.gz
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libprozilla*

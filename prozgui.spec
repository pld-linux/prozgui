#
# TODO:
#
# descriptions, summaries, cleanups, adapterize,
#
Summary:	An GUI advanced Linux download manager
Name:		prozgui
Version:	2.0.4
Release:	0.1
License:	GNU
Group:		Applications/Networking
Source0:	http://prozilla.delrom.ro/packages/prozgui/tarballs/%{name}-%{version}beta3.tar.gz
Source1:	%{name}.desktop
Url:		http://prozilla.delrom.ro/
Icon:		prozgui48.xpm
BuildRequires:	fltk-devel
Requires:	fltk
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package devel
Summary:	development files
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
prozilla headers

%package static
Summary:	static files
Group:		Development/Libraries
Requires:       %{name}-devel = %{version}

%description static
prozilla static libraries

%prep
%setup -q -n %{name}-%{version}beta3

%build
%configure2_13 \
    --with-fltk-includes=/usr/X11R6/include \
    --with-fltk-libs=/usr/X11R6/lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT prefix=$RPM_BUILD_ROOT install


# Mandrake Menu entry
install -d $RPM_BUILD_ROOT/usr/X11R6/share/{pixmaps,applnk/Network/FTP}
install -d $RPM_BUILD_ROOT/usr/X11R6/include
install %{SOURCE1} $RPM_BUILD_ROOT/usr/X11R6/share/applnk/Network/FTP/%{name}.desktop
cp src/images/Pz12.xpm $RPM_BUILD_ROOT/usr/X11R6/share/pixmaps/prozgui.xpm

mv docs/FAQ ./
mv man/prozgui.1 ./
mv libprozilla/TODO libprozilla/TODO-devel
mv libprozilla/README libprozilla/README-devel
mv libprozilla/src/{prozilla.h,netrc.h} $RPM_BUILD_ROOT/usr/X11R6/include/
mv -f $RPM_BUILD_ROOT/share/locale/ $RPM_BUILD_ROOT/usr/X11R6/share/

gzip -9nf {ABOUT-NLS,AUTHORS,COPYING,CREDITS*,ChangeLog,INSTALL,NEWS,README,TODO,FAQ,prozgui.1}

mv libprozilla/docs/HACKING ./libprozilla/
gzip -9nf libprozilla/{TODO-devel,README-devel,HACKING}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/bin/
/usr/X11R6/share/
%doc *.gz

%files devel
/usr/X11R6/include/*.h
%doc libprozilla/*.gz

%files static
/usr/X11R6/lib/libprozilla*

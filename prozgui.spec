Summary:	An GUI advanced Linux download manager
Name:		prozgui
Version:	2.0.4beta3
Release:	1
License:	GNU
Group:		Applications/Internet
######		Unknown group!
######		Unknown group!
Source0:	http://prozilla.delrom.ro/packages/prozgui/tarballs/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Url:		http://prozilla.delrom.ro/
Icon:		%{name}48.xpm
BuildRequires:	fltk-devel
Requires:	fltk
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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


%prep

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install


# Mandrake Menu entry
install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/Internet
install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps


bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/Internet/%{name}.desktop
cp src/images/Pz12.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/prozgui.xpm


%clean
rm -rf $RPM_BUILD_ROOT/%{name}-%{version}
rm -rf $RPM_BUILD_DIR/*

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/prozgui
%{_includedir}/prozilla*
%{_libdir}/libprozilla*
%{_datadir}/locale/*/*/*
%doc COPYING
%doc ChangeLog
%doc CREDITS*
%doc INSTALL
%doc README
%doc TODO
%doc docs/FAQ
%doc libprozilla/docs/HACKING
%{_sysconfdir}/X11/applnk/Internet/*
%{_datadir}/pixmaps/*

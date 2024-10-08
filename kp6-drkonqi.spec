#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.0
%define		qtver		5.15.2
%define		kpname		drkonqi
Summary:	drkonqi
Name:		kp6-%{kpname}
Version:	6.2.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	f04c1f832254cbe6f5b12a4046ee598f
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	hardlink >= 1.0-3
BuildRequires:	kf6-attica-devel
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-frameworkintegration-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kcodecs-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kcrash-devel
BuildRequires:	kf6-kguiaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kstatusnotifieritem-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	kf6-syntax-highlighting-devel
BuildRequires:	kp6-kdecoration-devel
BuildRequires:	kuserfeedback-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	polkit-qt6-1-devel
BuildRequires:	polkit-qt6-1-gui-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-qmake
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	systemd
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	python3-psutil
Requires:	python3-pygdbmi
Requires:	python3-sentry-sdk
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plasma crash handler, gives the user feedback if a program crashed.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DWITH_PYTHON_VENDORING=OFF
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_iconsdir}/{breeze-dark,breeze}
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%ninja_install -C build

mv $RPM_BUILD_ROOT%{_prefix}%{systemdunitdir}/drkonqi-coredump-processor@.service $RPM_BUILD_ROOT%{systemdunitdir}/

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/drkonqi
%{_datadir}/drkonqi
%{_desktopdir}/org.kde.drkonqi.desktop
%{_datadir}/qlogging-categories6/drkonqi.categories
%{systemdunitdir}/drkonqi-coredump-processor@.service
%{systemduserunitdir}/drkonqi-coredump-cleanup.service
%{systemduserunitdir}/drkonqi-coredump-cleanup.timer
%{systemduserunitdir}/drkonqi-coredump-launcher.socket
%{systemduserunitdir}/drkonqi-coredump-launcher@.service
%dir %{_libdir}/qt6/plugins/drkonqi
%attr(755,root,root) %{_libdir}/qt6/plugins/drkonqi/KDECoredumpNotifierTruck.so
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-cleanup
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-launcher
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-processor
%attr(755,root,root) %{_bindir}/drkonqi-coredump-gui
%{_desktopdir}/org.kde.drkonqi.coredump.gui.desktop
%attr(755,root,root) %{_bindir}/drkonqi-sentry-data
%{_prefix}%{systemdunitdir}/systemd-coredump@.service.wants/drkonqi-coredump-processor@.service
%{systemduserunitdir}/default.target.wants/drkonqi-coredump-cleanup.service
%{systemduserunitdir}/default.target.wants/drkonqi-sentry-postman.path
%{systemduserunitdir}/drkonqi-coredump-pickup.service
%{systemduserunitdir}/drkonqi-sentry-postman.path
%{systemduserunitdir}/drkonqi-sentry-postman.service
%{systemduserunitdir}/drkonqi-sentry-postman.timer
%{systemduserunitdir}/plasma-core.target.wants/drkonqi-coredump-pickup.service
%{systemduserunitdir}/plasma-core.target.wants/drkonqi-sentry-postman.path
%{systemduserunitdir}/plasma-core.target.wants/drkonqi-sentry-postman.timer
%{systemduserunitdir}/sockets.target.wants/drkonqi-coredump-launcher.socket
%{systemduserunitdir}/timers.target.wants/drkonqi-coredump-cleanup.timer
%{systemduserunitdir}/timers.target.wants/drkonqi-sentry-postman.timer
%attr(755,root,root) %{_prefix}/libexec/drkonqi-sentry-postman
%attr(755,root,root) %{_prefix}/libexec/kf6/drkonqi-polkit-helper
%{_datadir}/dbus-1/system-services/org.kde.drkonqi.service
%{_datadir}/dbus-1/system.d/org.kde.drkonqi.conf
%{_datadir}/polkit-1/actions/org.kde.drkonqi.policy

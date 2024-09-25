
%global  qt_version 6.7.2

Summary: Qt6 - Sensors component
Name:    qt6-qtsensors
Version: 6.7.2
Release: 0%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io/
Source0: %{name}-%{version}.tar.bz2

# filter qml/plugin provides
%global __provides_exclude_from ^(%{_qt6_archdatadir}/qml/.*\\.so|%{_qt6_plugindir}/.*\\.so)$

BuildRequires: cmake
BuildRequires: clang
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel >= %{qt_version}
BuildRequires: qt6-qtsvg-devel >= %{qt_version}

BuildRequires: pkgconfig(xkbcommon) >= 0.5.0
BuildRequires: openssl-devel

# provides a plugin that can use iio-sensor-proxy
Recommends: iio-sensor-proxy

%description
The Qt Sensors API provides access to sensor hardware via QML and C++
interfaces.  The Qt Sensors API also provides a motion gesture recognition
API for devices.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/*
%{_qt6_libdir}/libQt6Sensors.so.6*
%{_qt6_libdir}/libQt6SensorsQuick.so.6*
%{_qt6_plugindir}/sensors/
%{_qt6_archdatadir}/qml/QtSensors/

%files devel
%{_qt6_headerdir}/QtSensors/
%{_qt6_headerdir}/QtSensorsQuick/
%{_qt6_libdir}/libQt6Sensors.so
%{_qt6_libdir}/libQt6Sensors.prl
%{_qt6_libdir}/libQt6SensorsQuick.prl
%{_qt6_libdir}/libQt6SensorsQuick.so
%{_qt6_libdir}/cmake/Qt6/FindSensorfw.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtSensorsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Sensors/
%{_qt6_libdir}/cmake/Qt6Sensors/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6SensorsQuick/
%{_qt6_libdir}/cmake/Qt6SensorsQuick/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_sensors*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc

#
# spec file for package srsRAN (former srsLTE)
#
# Copyright (c) 2017-2022, Martin Hauke <mardnh@gmx.de>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define realver 22_10
%define sover   0
# For uncertain reasons, the hardened build breaks the test suite
Name:           srsRAN_4G
Version:        22.10
Release:        0
Summary:        Open source 3GPP LTE library
# libraries are using GPL2.0 and LGPL-2.0 - see file COPYRIGHT
License:        AGPL-3.0-only
Group:          Productivity/Hamradio/Other
URL:            https://www.srsran.com/
#Git-Clone:     https://github.com/srsran/srsRAN.git
Source:         https://github.com/srsran/srsRAN_4g/archive/refs/tags/release_%{realver}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
# kernel-default and kmod needed for the SCTP-related unit-tests
BuildRequires:  kernel-modules
BuildRequires:  kmod
#
BuildRequires:  lksctp-tools-devel
BuildRequires:  mbedtls-devel
BuildRequires:  pkgconfig
#BuildRequires:  srsgui-devel
BuildRequires:  pkgconfig(SoapySDR)
BuildRequires:  pkgconfig(fftw3f)
#BuildRequires:  pkgconfig(libbladeRF)
BuildRequires:  pkgconfig(libconfig++)
BuildRequires:  pcsc-lite-devel
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  pkgconfig(uhd)
BuildRequires:  boost-devel

%description
srsLTE is a free and open-source LTE software suite.
It includes:
 * srsUE - a complete SDR LTE UE application featuring all layers
   from PHY to IP
 * srsENB - a complete SDR LTE eNodeB application
 * srsEPC - a light-weight LTE core network implementation with MME,
   HSS and S/P-GW
 * a highly modular set of common libraries for PHY, MAC, RLC, PDCP,
   RRC, NAS, S1AP and GW layers.

The libraries are highly modular with minimum inter-module or external
dependencies.

%package -n     libsrsran_rf%{sover}
Summary:        srsLTE RF Library
Group:          System/Libraries

%description -n libsrsran_rf%{sover}
%{name} is a free and open-source LTE software suite.
It includes:
 * srsUE - a complete SDR LTE UE application featuring all layers
   from PHY to IP
 * srsENB - a complete SDR LTE eNodeB application
 * srsEPC - a light-weight LTE core network implementation with MME,
   HSS and S/P-GW
 * a highly modular set of common libraries for PHY, MAC, RLC, PDCP,
   RRC, NAS, S1AP and GW layers.

The libraries are highly modular with minimum inter-module or external
dependencies.

This package contains the shared library.

%package examples
Summary:        Examples from the %{name} code

%description examples
srsRAN_4G comes with examples. This package contains them.

%package devel
Summary:        Development files for the libsrsran library
Group:          Development/Libraries/C and C++

%description devel
This subpackage contains libraries and header files for developing
applications that want to make use of libsrsran.

%prep
%setup -q -n %{name}-release_%{realver}

%build
# FIXME: you should use the %%cmake macros
export CXXFLAGS="%{build_cxxflags} -Wno-stringop-overflow"
%cmake \
    -DENABLE_SRSUE=ON \
    -DENABLE_SRSENB=ON \
    -DENABLE_GUI=OFF \
    -DENABLE_BLADERF=OFF \
    -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF

%cmake_build

%install
%cmake_install
install -d %{buildroot}/%{_sysconfdir}/srsran

## install examples
# FIXME: should be in an other path
mkdir -p "%{buildroot}%{_libexecdir}/srsran"
for f in $(find %{__cmake_builddir}/lib/examples/ -type f -executable); do
  chrpath -d "$f"
  install -Dpm0755 "$f" "%{buildroot}%{_libexecdir}/srsran/"
done

# check
# export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
# run ctest -- can't work, needs sctp kernel module to be loaded

%post -n libsrsran_rf%{sover} -p /sbin/ldconfig
%postun -n libsrsran_rf%{sover} -p /sbin/ldconfig

%files
%license LICENSE COPYRIGHT
%doc README.md
%{_datadir}/srsran
%config %{_sysconfdir}/srsran
%{_bindir}/srsenb
%{_bindir}/srsepc
%{_bindir}/srsue
%{_bindir}/srsmbms
%{_bindir}/srsepc_if_masq.sh
%{_bindir}/srsran_install_configs.sh
%{_libdir}/libasn1_utils.a
%{_libdir}/libnas_5g_msg.a
%{_libdir}/librrc_asn1.a
%{_libdir}/libngap_nr_asn1.a
%{_libdir}/librrc_nr_asn1.a
%{_libdir}/libs1ap_asn1.a
%{_libdir}/libsrslog.a
%{_libdir}/libsrsran_common.a
%{_libdir}/libsrsran_gtpu.a
%{_libdir}/libsrsran_mac.a
%{_libdir}/libsrsran_pdcp.a
%{_libdir}/libsrsran_phy.a
%{_libdir}/libsrsran_radio.a
%{_libdir}/libsrsran_rlc.a
%{_libdir}/libsrsran_rf.so
# {_libdir}/libsrsran_rf_blade.so
%{_libdir}/libsrsran_rf_soapy.so
%{_libdir}/libsrsran_rf_uhd.so
%{_libdir}/libsrsran_rf_zmq.so

%files -n libsrsran_rf%{sover}
%{_libdir}/libsrsran_rf*.so.*

%files examples
%dir %{_libexecdir}/srsran/
%{_libexecdir}/srsran/cell_search
%{_libexecdir}/srsran/cell_search_nbiot
%{_libexecdir}/srsran/npdsch_enodeb
%{_libexecdir}/srsran/npdsch_ue
%{_libexecdir}/srsran/pdsch_enodeb
%{_libexecdir}/srsran/pdsch_ue
%{_libexecdir}/srsran/pssch_ue
%{_libexecdir}/srsran/synch_file
%{_libexecdir}/srsran/usrp_capture
%{_libexecdir}/srsran/usrp_capture_sync
%{_libexecdir}/srsran/usrp_capture_sync_nbiot
%{_libexecdir}/srsran/usrp_txrx
%{_libexecdir}/srsran/zmq_remote_rx

%files devel
%{_includedir}/srsran/

%changelog
* Thu Mar 16 2023 Marcus Müller <mueller_fedora@baseband.digital> - 22.10-0
- Initial port of the OpenSUSE package
- Rename srsRAN -> srsRAN_4g as per mailing list 2023-03-15
- split off examples

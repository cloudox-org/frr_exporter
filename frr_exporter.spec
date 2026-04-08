%global debug_package %{nil}
%global user frr
%global group frr

Name: frr_exporter
Version: 1.11.0
Release: 1%{?dist}
Summary: Prometheus exporter for FRR metrics
License: MIT
URL:     https://github.com/tynany/frr_exporter

Source0: https://github.com/tynany/frr_exporter/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Export FRR service metrics to Prometheus.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group frr >/dev/null || groupadd -r frr
getent passwd frr >/dev/null || \
useradd -r -g frr -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "frr_exporter service" frr
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Wed Apr 08 2026 Ivan Garcia <igarcia@cloudox.org> - 1.11.0
- Initial packaging for the 1.11.0 branch
* Tue Mar 31 2026 Ivan Garcia <igarcia@cloudox.org> - 1.10.1
- Initial packaging for the 1.10.1 branch

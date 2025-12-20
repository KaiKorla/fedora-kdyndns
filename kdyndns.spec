%global debug_package %{nil}

Name:               kdyndns
Version:            3.0.0
Release:            2%{?dist}
%global upstream_tag %{lua:local v=rpm.expand("%{version}");print((v:gsub("~","-")))}
Summary:            A minimalistic DynDNS service written in Rust.

License:            MIT

URL:                https://github.com/KaiKorla/KDynDNS
Source0:            %{url}/archive/refs/tags/%{upstream_tag}.tar.gz
Source1:            kdyndns-sysusers.conf
Source2:            kdyndns.service
Source3:            kdyndns.socket

ExclusiveArch:      x86_64 aarch64

BuildRequires:      rust
BuildRequires:      cargo
BuildRequires:      rust-packaging
BuildRequires:      systemd-rpm-macros

Requires: systemd
Suggests: nginx

%description
A minimalistic DynDNS service written in Rust.

%prep
%autosetup -n KDynDNS-%{upstream_tag}
%cargo_prep -v vendor

%build
%cargo_build

%check
%cargo_test

%install
%cargo_install
install -d %{buildroot}%{_sysconfdir}/kdyndns
install -m0644 config/config.toml %{buildroot}%{_sysconfdir}/kdyndns/config.toml
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/kdyndns.conf
install -Dm0644 %{SOURCE2} %{buildroot}%{_unitdir}/kdyndns.service
install -Dm0644 %{SOURCE3} %{buildroot}%{_unitdir}/kdyndns.socket

%files
%license LICENSE
%doc CHANGELOG.md
%doc README.md

%config(noreplace) %{_sysconfdir}/kdyndns/config.toml

%{_sysusersdir}/kdyndns.conf
%{_unitdir}/kdyndns.service
%{_unitdir}/kdyndns.socket


%{_bindir}/kdyndns

%post
%systemd_post kdyndns.socket
%systemd_post kdyndns.service

%preun
%systemd_preun kdyndns.socket
%systemd_preun kdyndns.service

%postun
%systemd_postun kdyndns.socket
%systemd_postun_with_restart kdyndns.service

%changelog
%autochangelog

%global debug_package %{nil}

Name:               kdyndns
Version:            3.0.0
Release:            1%{?dist}
%global upstream_tag %{lua:local v=rpm.expand("%{version}");print((v:gsub("~","-")))}
Summary:            A minimalistic DynDNS service written in Rust.

License:            MIT

URL:                https://github.com/KaiKorla/KDynDNS
Source0:            %{url}/archive/refs/tags/%{upstream_tag}.tar.gz
Source1:            kdyndns-sysusers.conf
Source2:            kdyndns.service

ExclusiveArch:      x86_64 aarch64

BuildRequires:      rust
BuildRequires:      cargo
BuildRequires:      rust-packaging
BuildRequires:      systemd-rpm-macros

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

%files
%license LICENSE
%doc CHANGELOG.md
%doc README.md

%config(noreplace) %{_sysconfdir}/kdyndns/config.toml

%{_sysusersdir}/kdyndns.conf
%{_unitdir}/kdyndns.service

%{_bindir}/kdyndns

%post
%systemd_post kdyndns.socket

%preun
%systemd_preun kdyndns.socket

%postun
%systemd_postun kdyndns.socket

%changelog
%autochangelog

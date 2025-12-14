%global debug_package %{nil}

Name:               kdyndns
Version:            1.0.0~beta.0
Release:            1%{?dist}
%global upstream_tag %{lua:local v=rpm.expand("%{version}");print((v:gsub("~","-")))}
Summary:            A minimalistic DynDNS service written in Rust.

License:            MIT

URL:                https://github.com/KaiKorla/KDynDNS
Source0:            %{url}/archive/refs/tags/%{upstream_tag}.tar.gz
Source1:            kdyndns-sysusers.conf
Source2:            kdyndns-tmpfiles.conf
Source3:            kdyndns.service

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
install -Dm0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/kdyndns.conf
install -Dm0644 %{SOURCE3} %{buildroot}%{_unitdir}/kdyndns.service

%files
%license LICENSE
%doc CHANGELOG.md
%doc README.md

%config(noreplace) %{_sysconfdir}/kdyndns/config.toml

%{_sysusersdir}/kdyndns.conf
%{_tmpfilesdir}/kdyndns.conf
%{_unitdir}/kdyndns.service

%{_bindir}/kdyndns

%pre
%sysusers_create %{_sysusersdir}/kdyndns.conf

%post
%tmpfiles_create %{_tmpfilesdir}/kdyndns.conf
%systemd_post kdyndns.service

%preun
%systemd_preun kdyndns.service

%postun
%systemd_postun_with_restart kdyndns.service

%changelog
%autochangelog

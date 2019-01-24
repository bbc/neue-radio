# -----------------------------------------------------------------------------
# Overview of a spec
# -----------------------------------------------------------------------------
# This file provides the instructions for:
#
#   1) How to build an .rpm file.
#   2) What happens when the RPM is installed or uninstalled.
#
# To deferentiate between the two events, we use 'build time' and 'installation
# time' in the comments. The result of a build is a .rpm file. The result of an
# installation is the software existing on a machine, usually after a 'yum
# install ...' command has been run.
#
# For more information see:
# - https://confluence.dev.bbc.co.uk/display/platform/Packaging+your+software
# - https://access.redhat.com/articles/216643
# -----------------------------------------------------------------------------

Name: tne-prototype
Version: 0.1.0%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: %{name}
Source0: src.tar.gz

# -----------------------------------------------------------------------------
# CentOS packages
# -----------------------------------------------------------------------------
# Because we are using a CentOS 7 base image, at 'installation time', all
# packages CentOS 7 provide are made available for us without us having to
# specify the repository url in the Cosmos component.

# See: http://mirror.centos.org/centos/7/os/x86_64/Packages/
# -----------------------------------------------------------------------------
Requires: python2
Requires: python2-devel
Requires: python-pip

Requires: python-virtualenv

Requires: nginx

# -----------------------------------------------------------------------------
# Apache TLS - Access control
# -----------------------------------------------------------------------------
# Restrict the application to 'services' and 'developers' with valid BBC issued
# certificates (https://github.com/bbc/cloud-httpd-conf/).
#
# As this package is not available in the base CentOS 7 repositories, we have
# to configure the component to make another repository available at
# 'installation time'. If we forgot this step, the installation process will be
# unable to locate this package and will fail.
#
# To see where this repository is defined, search 'cloud-httpd-conf-el7' at
# https://admin.live.bbc.co.uk/cosmos/component/sample-app-python/repositories.
# -----------------------------------------------------------------------------
Requires: cloud-httpd24-ssl-services-devs

# -----------------------------------------------------------------------------
# Requirements for 'build time'
# -----------------------------------------------------------------------------
# For this python application, various packages are required via python-pip,
# defined in the requirements.txt file. These packages are bundled into
# the RPM.
# -----------------------------------------------------------------------------
BuildRequires: python2-devel
BuildRequires: python-pip
BuildRequires: systemd

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{name}

%prep
%setup -q -n cosmos/

%build

%install
rm -rf %{buildroot}

# Copy systemd config to /usr/lib/systemd/system/${name}.service
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp %{_builddir}/cosmos/systemd/%{name}.service %{buildroot}/usr/lib/systemd/system/

# Install dependencies to /usr/lib/${name}
mkdir -p %{buildroot}/usr/lib/%{name}
# PYTHONDONTWRITEBYTECODE=1 CFLAGS="$RPM_OPT_FLAGS" pip install --install-option='--install-platlib=$base/lib/python' --target %{buildroot}/usr/lib/%{name} --no-deps ../ext/*

# Copy application files to /usr/lib/${name}/${name}
cp -r %{_builddir}/cosmos/apps %{buildroot}/usr/lib/%{name}/
cp -r %{_builddir}/cosmos/deployment %{buildroot}/usr/lib/%{name}/
cp -r %{_builddir}/cosmos/services %{buildroot}/usr/lib/%{name}/
cp -r %{_builddir}/cosmos/shared %{buildroot}/usr/lib/%{name}/
cp -r %{_builddir}/cosmos/bin %{buildroot}/usr/

# Copy bake scripts to /etc/bake-scripts/${name}
mkdir -p %{buildroot}%{_sysconfdir}/bake-scripts
cp -R %{_builddir}/cosmos/bake-scripts %{buildroot}%{_sysconfdir}/bake-scripts/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d / -s /sbin/nologin %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%files
%defattr(0755, root, root, 0755)
/usr/bin/*
%defattr(-, root, root, 0755)
/etc/bake-scripts/*
%defattr(0644, root, root, 0755)
/usr/lib/%{name}
/usr/lib/systemd/system/*
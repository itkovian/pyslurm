# SPEC file taken from https://centos.pkgs.org/7/puias-computational-x86_64/python-pyslurm-17.02-1.gitab899c6.sdl7.x86_64.rpm.html
Name:		pyslurm
Version:	24.05
%global	rel     1
Release:	%{rel}.%{gittag}%{?dist}.ug
Summary:	PySlurm: Slurm Interface for Python

Group:		Development/Libraries
License:	GPLv2
URL:		https://github.com/PySlurm/pyslurm

# when the rel number is one, the directory name does not include it
%if "%{rel}" == "1"
%global pyslurm_source_dir %{name}-%{version}
%else
%global pyslurm_source_dir %{name}-%{version}-%{rel}
%endif


Source:         %{pyslurm_source_dir}.tar.gz
#Source0:	https://github.com/PySlurm/pyslurm/archive/%{pyslcommit}/archive/%{pkgname}.tar.gz#/%{pkgname}-%{pyslcommit}.tar.gz

BuildRequires:	python3-Cython, python36-devel
%global usepython python3.6
%global usepython_sitearch %{python3_sitearch}

BuildRequires:	slurm-devel >= %{version}
Requires:	slurm

%description
This module provides a low-level Python wrapper around the Slurm C-API using Cython.

%prep
%setup -q -n %{pyslurm_source_dir}

%build
%{usepython} setup.py build

%install
%{usepython} setup.py install --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%doc COPYING.txt
%{usepython_sitearch}/*

%changelog
* Tue May 29 2018 Andy Georges <andy.georges@ugent.be> - Adjusted for HPC UGent
* Fri May 19 2017 Josko Plazonic <plazonic@princeton.edu> - 17.02-1
- initial build

%define python3_pkgversion 3

Name:            python3-pyslurm
Version:         24.11.0
%define rel      1
Release:         %{rel}%{?dist}
Summary:         Python interface to Slurm
License:         GPLv2+
URL:             https://github.com/PySlurm/pyslurm
Source:          pyslurm-%{version}.tar.gz

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
BuildRequires:   python%{python3_pkgversion}-devel
BuildRequires:   python%{python3_pkgversion}-setuptools
BuildRequires:   python%{python3_pkgversion}-wheel
BuildRequires:   python%{python3_pkgversion}-Cython
BuildRequires:   python%{python3_pkgversion}-packaging
BuildRequires:   python-rpm-macros
BuildRequires:   slurm-devel >= 24.11.0
BuildRequires:   slurm >= 24.11.0
Requires:        python%{python3_pkgversion}

%description
pyslurm is a Python interface to Slurm

#%package -n python%{python3_pkgversion}-pyslurm
Summary:        %{summary}

%description -n python%{python3_pkgversion}-pyslurm
pyslurm is a Python interface to Slurm

%prep
%autosetup -p1 -n pyslurm-%{version}

#%generate_buildrequires
#%pyproject_buildrequires -R

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyslurm

%files -f %{pyproject_files}
%license COPYING.txt
%doc README.md

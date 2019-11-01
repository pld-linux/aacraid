#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		snap	58012
%define		rel	1
%define		pname	aacraid
Summary:	Adaptec RAID card driver
Name:		%{pname}%{_alt_kernel}
Version:	1.2.1
Release:	0.%{snap}.%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
Source0:	http://download.adaptec.com/raid/aac/linux/aacraid-linux-src-%{version}-%{snap}.tgz
# Source0-md5:	6ddeb36afc1bd0dd629bd2c22ba0c678
URL:		https://storage.microsemi.com/en-us/downloads/linux_source/linux_source_code/productid=asr-8885q&dn=adaptec+raid+8885q.php
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%description
Adaptec RAID card driver.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-scsi-aacraid\
Summary:	Adaptec RAID card driver\
Release:	0.%{snap}.%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-scsi-aacraid\
Adaptec RAID card driver\
\
%files -n kernel%{_alt_kernel}-scsi-aacraid\
%defattr(644,root,root,755)\
%doc CHANGELOG README TODO\
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/*.ko*\
\
%post	-n kernel%{_alt_kernel}-scsi-aacraid\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-scsi-aacraid\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m aacraid V=1\
%install_kernel_modules -D installed -m aacraid -d kernel/drivers/scsi/\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -qc
tar xvf *_source_*
mv *-%{version}-%{snap}/* .

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

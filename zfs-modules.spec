# The following block is used to allow the source RPM to be rebuilt 
# against specific kernels.  It is preferable that rpmbuild define the
# require_kver, require_kdir, require_obj constants for us, but if it does not
# not we attempt to determine the correct values based on your distro.

# kdir:    Full path to the kernel source headers
# kobj:    Full path to the kernel build objects
# kver:    Kernel version
# kpkg:    Kernel package name
# kdevpkg: Kernel devel package name
# kverpkg: Kernel package version

%if %{defined require_kver}
%define kver %{require_kver}
%endif

%if %{defined require_kdir}
%define kdir %{require_kdir}
%endif

%if %{defined require_kobj}
%define kobj %{require_kobj}
%endif

# Set using 'rpmbuild ... --with kernel ...', defaults to enabled.
%if %{defined _with_kernel}
 %define with_kernel 1
%else
 %if %{defined _without_kernel}
  %define with_kernel 0
 %else
  %define with_kernel 1
 %endif
%endif

# Set using 'rpmbuild ... --with kernel-debug ...', defaults to disabled.
%if %{defined _with_kernel_debug}
 %define with_kernel_debug 1
%else
 %if %{defined _without_kernel_debug}
  %define with_kernel_debug 0
 %else
  %define with_kernel_debug 0
 %endif
%endif

# Set using 'rpmbuild ... --with kernel-dkms ...', defaults to disabled.
%if %{defined _with_kernel_dkms}
 %define with_kernel_dkms 1
%else
 %if %{defined _without_kernel_dkms}
  %define with_kernel_dkms 0
 %else
  %define with_kernel_dkms 0
 %endif
%endif

# Set using 'rpmbuild ... --with debug ...', defaults to disabled.
%if %{defined _with_debug}
 %define kdebug --enable-debug
%else
 %if %{defined _without_debug}
  %define kdebug --disable-debug
 %else
  %define kdebug --disable-debug
 %endif
%endif

# Set using 'rpmbuild ... --with debug-dmu-tx ...', defaults to disabled.
%if %{defined _with_debug_dmu_tx}
 %define kdebug_dmu_tx --enable-debug-dmu-tx
%else
 %if %{defined _without_debug_dmu_tx}
  %define kdebug_dmu_tx --disable-debug-dmu-tx
 %else
  %define kdebug_dmu_tx --disable-debug-dmu-tx
 %endif
%endif

# SLES:
%if %{defined suse_version}
 %if %{undefined kver}
  %ifarch ppc64
   %define kverextra     ppc64
  %else
   %define kverextra     default
  %endif

  %if %{suse_version} >= 1100
   %define klnk          %{_usrsrc}/linux-obj/%{_target_cpu}/%{kverextra}
   %define krelease      %{klnk}/include/config/kernel.release
  %else
   %define klnk          %{_usrsrc}/linux-obj/%{_target_cpu}/%{kverextra}
   %define krelease      %{klnk}/.kernelrelease
  %endif

  %define kver_kern      %((echo X; %{__cat} %{krelease} 2>/dev/null)|tail -1)
  %define kver_dbug      %{nil}
 %else
  %define kver_kern      %{kver}
  %define kver_dbug      %{nil}
 %endif

 %if %{undefined kverextra}
  %define kverextra      %(echo %{kver_kern} | cut -f3 -d'-')
 %endif

 %define kpkg_kern       kernel-%{kverextra}
 %define kpkg_dbug       %{nil}
 %define kpkg_dkms       dkms

 %define kdevpkg_kern    kernel-source
 %define kdevpkg_dbug    %{nil}
 %define kdevpkg_dkms    dkms

 %define kverpkg_kern    %(echo %{kver_kern} | %{__sed} -e 's/-%{kverextra}//g')
 %define kverpkg_dbug    %{nil}
 %define kverpkg_dkms    2.2.0.2

 # The kernel and rpm versions do not strictly match under SLES11
 # e.g. kernel version 2.6.27.19-5 != rpm version 2.6.27.19-5.1
 %if %{suse_version} >= 1100
  %define koppkg         >=
 %else
  %define koppkg         =
 %endif

 %if %{undefined kdir}
  %define kdir_kern      %{_usrsrc}/linux-%{kverpkg_kern}
  %define kdir_dbug      %{nil}
 %else
  %define kdir_kern      %{kdir}
  %define kdir_dbug      %{nil}
 %endif

 %if %{undefined kobj}
  %define kobj_kern      %{kdir_kern}-obj/%{_target_cpu}/%{kverextra}
  %define kobj_dbug      %{nil}
 %else
  %define kobj_kern      %{kobj}
  %define kobj_dbug      %{nil}
 %endif
%else

# RHEL 5.x/6.x, CHAOS 5.x:
%if %{defined el5} || %{defined el6} || %{defined ch5}
 %if %{undefined kver}
  %define klnk           %{_usrsrc}/kernels/*/include/config
  %define kver_kern      %((echo X; ((%{__cat} %{klnk}/kernel.release
                            2>/dev/null) | %{__grep} -v debug)) | tail -1)
  %define kver_dbug      %((echo X; ((%{__cat} %{klnk}/kernel.release
                            2>/dev/null) | %{__grep} debug)) | tail -1)
 %else
  %define kver_kern      %{kver}
  %define kver_dbug      %{kver}.debug
 %endif

 %define kpkg_kern       kernel
 %define kpkg_dbug       kernel-debug
 %define kpkg_dkms       dkms

 %define kdevpkg_kern    kernel-devel
 %define kdevpkg_dbug    kernel-debug-devel
 %define kdevpkg_dkms    dkms

 %define kverpkg_dkms    2.2.0.2
 %if %{defined el6} || %{defined ch5}
  %define kverpkg_kern   %(echo %{kver_kern} | %{__sed} -e 's/.%{_target_cpu}//g')
  %define kverpkg_dbug   %(echo %{kver_dbug} | %{__sed} -e 's/.%{_target_cpu}//g' | %{__sed} -e 's/.debug//g')
 %else
  %define kverpkg_kern   %{kver_kern}
  %define kverpkg_dbug   %{kver_dbug}
 %endif

 %define koppkg          =

 %if %{undefined kdir}
  %if %{defined el6} || %{defined ch5}
   %define kdir_kern      %{_usrsrc}/kernels/%{kver_kern}
   %define kdir_dbug      %{_usrsrc}/kernels/%{kver_dbug}
  %else
   %define kdir_kern      %{_usrsrc}/kernels/%{kver_kern}-%{_target_cpu}
   %define kdir_dbug      %{_usrsrc}/kernels/%{kver_dbug}-%{_target_cpu}
  %endif
 %else
  %define kdir_kern       %{kdir}
  %define kdir_dbug       %{kdir}.debug
 %endif

 %if %{undefined kobj}
  %define kobj_kern      %{kdir_kern}
  %define kobj_dbug      %{kdir_dbug}
 %else
  %define kobj_kern      %{kobj}
  %define kobj_dbug      %{kobj}.debug
 %endif
%else

# Fedora:
%if %{defined fedora}
 %if %{undefined kver}
  %define klnk           %{_usrsrc}/kernels/*/include/config
  %define kver_kern      %((echo X; ((%{__cat} %{klnk}/kernel.release
                            2>/dev/null) | %{__grep} -v debug)) | tail -1)
  %define kver_dbug      %((echo X; ((%{__cat} %{klnk}/kernel.release
                            2>/dev/null) | %{__grep} debug)) | tail -1)
 %else
  %define kver_kern      %{kver}
  %define kver_dbug      %{kver}.debug
 %endif

 %define kpkg_kern       kernel
 %define kpkg_dbug       kernel-debug
 %define kpkg_dkms       dkms

 %define kdevpkg_kern    kernel-devel
 %define kdevpkg_dbug    kernel-debug-devel
 %define kdevpkg_dkms    dkms

 %define kverpkg_dkms    2.2.0.2
 %define kverpkg_kern    %(echo %{kver_kern} | %{__sed} -e 's/.%{_target_cpu}//g')
 %define kverpkg_dbug    %(echo %{kver_dbug} | %{__sed} -e 's/.%{_target_cpu}//g' | %{__sed} -e 's/.debug//g')

 %define koppkg          =

 %if %{undefined kdir}
  %define kdir_kern      %{_usrsrc}/kernels/%{kver_kern}
  %define kdir_dbug      %{_usrsrc}/kernels/%{kver_dbug}
 %else
  %define kdir_kern      %{kdir}
  %define kdir_dbug      %{kdir}.debug
 %endif

 %if %{undefined kobj}
  %define kobj_kern      %{kdir_kern}
  %define kobj_dbug      %{kdir_dbug}
 %else
  %define kobj_kern      %{kobj}
  %define kobj_dbug      %{kobj}.debug
 %endif
%else

# Unsupported distro:
 %if %{undefined kver}
  %define kver_kern      %(uname -r)
  %define kver_dbug      %{nil}
 %else
  %define kver_kern      %{kver}
  %define kver_dbug      %{nil}
 %endif

 %define kverpkg_kern    %{kver_kern}
 %define kverpkg_dbug    %{nil}
 %define kverpkg_dkms    %{nil}

 %if %{undefined kdir}
  %define kdir_kern      /lib/modules/%{kver_kern}/build
  %define kdir_dbug      %{nil}
 %else
  %define kdir_kern      %{kdir}
  %define kdir_dbug      %{nil}
 %endif

 %if %{undefined kobj}
  %define kobj_kern      %{kdir_kern}
  %define kobj_dbug      %{nil}
 %else
  %define kobj_kern      %{kobj}
  %define kobj_dbug      %{nil}
 %endif

%endif
%endif
%endif

# spldir:    Full path to the spl source headers
# splobj:    Full path to the spl build objects
# splver:    Spl version
# splpkg:    Spl package name
# spldevpkg: Spl devel package name
# splverpkg: Spl package version

%if %{defined require_splver}
%define splver %{require_splver}
%endif

%if %{defined require_spldir}
%define spldir %{require_spldir}
%endif

%if %{defined require_splobj}
%define splobj %{require_splobj}
%endif

%if %{undefined splver}
 %define spllnk_kern     %{_usrsrc}/spl-*/%{kver_kern}
 %define spllnk_dbug     %{_usrsrc}/spl-*/%{kver_dbug}
 %define spllnk_dkms     %{_var}/lib/dkms/spl/*/build

 %define splver_kern     %((echo X; %{__cat} %{spllnk_kern}/spl.release
                            2>/dev/null) | tail -1)
 %define splver_dbug     %((echo X; %{__cat} %{spllnk_dbug}/spl.release
                            2>/dev/null) | tail -1)
 %define splver_dkms     %((echo X; %{__cat} %{spllnk_dkms}/spl.release
                            2>/dev/null) | tail -1)
%else
 %define splver_kern     %{splver}
 %define splver_dbug     %{splver}
 %define splver_dksm     %{splver}
%endif

%define splpkg_kern      spl-modules
%define splpkg_dbug      spl-modules-debug
%define splpkg_dkms      spl-modules-dkms

%define spldevpkg_kern   spl-modules-devel
%define spldevpkg_dbug   spl-modules-debug-devel
%define spldevpkg_dkms   spl-modules-dkms

%define splverpkg_kern   %{splver_kern}
%define splverpkg_dbug   %{splver_dbug}
%define splverpkg_dkms   %{splver_dkms}

%if %{undefined spldir}
 %define spldir_kern     %{_usrsrc}/spl-%{splver_kern}/%{kver_kern}
 %define spldir_dbug     %{_usrsrc}/spl-%{splver_dbug}/%{kver_dbug}
 %define spldir_dkms     %{_usrsrc}/spl-%{splver_dkms}
%else
 %define spldir_kern     %{spldir}
 %define spldir_dbug     %{spldir}.debug
 %define spldir_dkms     %{spldir}
%endif

%if %{undefined splobj}
 %define splobj_kern     %{spldir_kern}
 %define splobj_dbug     %{spldir_dbug}
 %define splobj_dkms     %{spldir_dkms}
%else
 %define splobj_kern     %{splobj}
 %define splobj_dbug     %{splobj}.debug
 %define splobj_dkms     %{splobj}
%endif


# Distro agnostic:
%define name             zfs-modules
%define version          0.6.0

# The kernel version should only be appended to a binary RPM.  When
# building a source RPM it must be kernel version agnostic.  This means
# the source RPM must never specify a required kernel version, but the
# final RPM should be keyed to the kernel version it was built against.
%if %{defined build_src_rpm}

%define rel_kern         rc12
%define rel_dbug         rc12
%define rel_dkms         rc12

%if %{defined kpkg_kern}
%define req_kern         %{kpkg_kern}
%endif
%if %{defined kpkg_dbug}
%define req_dbug         %{kpkg_dbug}
%endif
%if %{defined kpkg_dkms}
%define req_dkms         %{kpkg_dkms}
%endif

%define splreq_kern      %{splpkg_kern}
%define splreq_dbug      %{splpkg_dbug}
%define splreq_dkms      %{splpkg_dkms}

%define spldevreq_kern   %{spldevpkg_kern}
%define spldevreq_dbug   %{spldevpkg_dbug}
%define spldevreq_dkms   %{spldevpkg_dkms}

%else

%define relext_kern      %(echo %{kverpkg_kern} | %{__sed} -e 's/-/_/g')
%define relext_dbug      %(echo %{kverpkg_dbug} | %{__sed} -e 's/-/_/g')
%define rel_kern         rc12_%{relext_kern}
%define rel_dbug         rc12_%{relext_dbug}
%define rel_dkms         rc12

%if %{defined kpkg_kern}
%define req_kern         %{kpkg_kern} %{koppkg} %{kverpkg_kern}
%endif
%if %{defined kpkg_dbug}
%define req_dbug         %{kpkg_dbug} %{koppkg} %{kverpkg_dbug}
%endif
%if %{defined kpkg_dkms}
%define req_dkms         %{kpkg_dkms} >= %{kverpkg_dkms}
%endif

%define splreq_kern      %{splpkg_kern} = %{splverpkg_kern}_%{relext_kern}
%define splreq_dbug      %{splpkg_dbug} = %{splverpkg_dbug}_%{relext_dbug}
%define splreq_dkms      %{splpkg_dkms} = %{splverpkg_dkms}

%define spldevreq_kern   %{spldevpkg_kern} = %{splverpkg_kern}_%{relext_kern}
%define spldevreq_dbug   %{spldevpkg_dbug} = %{splverpkg_dbug}_%{relext_dbug}
%define spldevreq_dkms   %{spldevpkg_dkms} = %{splverpkg_dkms}

%endif

Summary:         ZFS File System
Group:           Utilities/System
Name:            %{name}
Version:         %{version}
Release:         %{rel_kern}
License:         CDDL
URL:             git://github.com/zfsonlinux/zfs.git
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id} -un)
Source:          zfs-%{version}.tar.gz

%if %{?with_kernel}

%if %{defined req_kern}
Requires:        %{req_kern}
%endif
%if %{defined kdevpkg_kern}
BuildRequires:   %{kdevpkg_kern}
%endif
%if %{defined splreq_kern}
Requires:        %{splreq_kern}
%endif
%if %{defined spldevpkg_kern}
BuildRequires:   %{spldevpkg_kern}
%endif
Provides:        lustre-backend-fs

%endif

%description
The %{name} package contains kernel modules and support utilities for
the %{name} file system.

%if %{?with_kernel}

%package devel
Summary:         ZFS File System Headers and Symbols
Group:           Development/Libraries
Release:         %{rel_kern}
%if %{defined devreq_kern}
Requires:        %{devreq_kern}
%endif
%if %{defined kdevpkg_kern}
BuildRequires:   %{kdevpkg_kern}
%endif
%if %{defined spldevreq_kern}
Requires:        %{spldevreq_kern}
%endif
%if %{defined spldevpkg_kern}
BuildRequires:   %{spldevpkg_kern}
%endif

%description devel
The %{name}-devel package contains the kernel header files and
Module.symvers symbols needed for building additional modules
which use %{name}.

%endif
%if %{?with_kernel_debug}

%package debug
Summary:         ZFS File System (Debug)
Group:           Utilities/System
Release:         %{rel_dbug}
%if %{defined req_dbug}
Requires:        %{req_dbug}
%endif
%if %{defined kdevpkg_dbug}
BuildRequires:   %{kdevpkg_dbug}
%endif
%if %{defined splreq_dbug}
Requires:        %{splreq_dbug}
%endif
%if %{defined spldevpkg_dbug}
BuildRequires:   %{spldevpkg_dbug}
%endif
Provides:        lustre-backend-fs

%description debug
The %{name}-debug package contains debug kernel modules and support
utilities for the %{name} file system.

%package debug-devel
Summary:         ZFS File System Headers and Symbols (Debug)
Group:           Development/Libraries
Release:         %{rel_dbug}
%if %{defined devreq_dbug}
Requires:        %{devreq_dbug}
%endif
%if %{defined kdevpkg_dbug}
BuildRequires:   %{kdevpkg_dbug}
%endif
%if %{defined spldevreq_dbug}
Requires:        %{spldevreq_dbug}
%endif
%if %{defined spldevpkg_dbug}
BuildRequires:   %{spldevpkg_dbug}
%endif

%description debug-devel
The %{name}-debug-devel package contains the debug kernel header files
and Module.symvers symbols needed for building additional modules
which use %{name}.

%endif
%if %{?with_kernel_dkms}

%package dkms
Summary:         ZFS File System (DKMS)
Group:           Utilities/System
Release:         %{rel_dkms}
Provides:        %{name}
BuildArch:       noarch
%if %{defined req_dkms}
Requires:        %{req_dkms}
%endif
%if %{defined kdevpkg_dkms}
BuildRequires:   %{kdevpkg_dkms}
%endif
%if %{defined splreq_dkms}
Requires:        %{splreq_dkms}
%endif
%if %{defined spldevpkg_dkms}
BuildRequires:   %{spldevpkg_dkms}
%endif
Provides:        lustre-backend-fs

%description dkms
The %{name}-dkms package contains the necessary pieces to build and
install the ZFS kernel modules with Dynamic Kernel Modules Support
(DKMS).

%endif

%prep
%setup -n zfs-%{version}
%build
rm -rf $RPM_BUILD_ROOT

%if %{with_kernel}

%configure --with-linux=%{kdir_kern} --with-linux-obj=%{kobj_kern} \
           --with-spl=%{spldir_kern} --with-spl-obj=%{splobj_kern} \
           --with-config=kernel %{kdebug} %{kdebug_dmu_tx}
make
make DESTDIR=$RPM_BUILD_ROOT install

%endif
%if %{?with_kernel_debug}

%configure --with-linux=%{kdir_dbug} --with-linux-obj=%{kobj_dbug} \
           --with-spl=%{spldir_dbug} --with-spl-obj=%{splobj_dbug} \
           --with-config=kernel %{kdebug} %{kdebug_dmu_tx}
make
make DESTDIR=$RPM_BUILD_ROOT install

%endif
%if %{?with_kernel_dkms}

%configure %{kdebug} %{kdebug_dmu_tx}
make dist
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/src
tar -xf zfs-%{version}.tar.gz -C $RPM_BUILD_ROOT/%{_prefix}/src
cp -af dkms.conf $RPM_BUILD_ROOT/%{_prefix}/src/zfs-%{version}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{?with_kernel}

%files
%defattr(-, root, root)
/lib/modules/%{kver_kern}/*

%files devel
%defattr(-,root,root)
%{_prefix}/src/*/%{kver_kern}

%post
if [ -f /boot/System.map-%{kver_kern} ]; then
	/sbin/depmod -ae -F /boot/System.map-%{kver_kern} %{kver_kern} || exit 0
else
	/sbin/depmod -a || exit 0
fi

%postun
if [ -f /boot/System.map-%{kver_kern} ]; then
	/sbin/depmod -ae -F /boot/System.map-%{kver_kern} %{kver_kern} || exit 0
else
	/sbin/depmod -a || exit 0
fi

%postun devel
rmdir %{_prefix}/src/zfs-%{version}-rc12 2>/dev/null
exit 0

%endif
%if %{?with_kernel_debug}

%files debug
%defattr(-, root, root)
/lib/modules/%{kver_dbug}/*

%files debug-devel
%defattr(-,root,root)
%{_prefix}/src/*/%{kver_dbug}

%post debug
if [ -f /boot/System.map-%{kver_dbug} ]; then
	/sbin/depmod -ae -F /boot/System.map-%{kver_dbug} %{kver_dbug} || exit 0
else
	/sbin/depmod -a || exit 0
fi

%postun debug
if [ -f /boot/System.map-%{kver_dbug} ]; then
	/sbin/depmod -ae -F /boot/System.map-%{kver_dbug} %{kver_dbug} || exit 0
else
	/sbin/depmod -a || exit 0
fi

%postun debug-devel
rmdir %{_prefix}/src/zfs-%{version}-rc12 2>/dev/null
exit 0

%endif
%if %{?with_kernel_dkms}

%files dkms
%defattr(-,root,root)
%{_prefix}/src/zfs-%{version}

%post dkms
for POSTINST in %{_prefix}/lib/dkms/common.postinst; do
	if [ -f $POSTINST ]; then
		$POSTINST zfs %{version}
		exit $?
	fi
	echo "WARNING: $POSTINST does not exist."
done
echo -e "ERROR: DKMS version is too old and zfs was not"
echo -e "built with legacy DKMS support."
echo -e "You must either rebuild zfs with legacy postinst"
echo -e "support or upgrade DKMS to a more current version."
exit 1

%preun dkms
echo -e
echo -e "Uninstall of zfs module (version %{version}) beginning:"
dkms remove -m zfs -v %{version} --all --rpm_safe_upgrade
exit 0

%endif

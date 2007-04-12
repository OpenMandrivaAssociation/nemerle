%define name nemerle
%define version 0.9.3
%define release %mkrel 4
#rpmlint false alarm
#%mklibname
%if %mdkversion >= 200600
%define pkgconfigdir %_datadir/pkgconfig
%else
%define pkgconfigdir %_libdir/pkgconfig
%endif
%define monodir %_prefix/lib/mono
%define build_nant 1

Summary: Nemerle compiler
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://nemerle.org/download/%{name}-%{version}.tar.bz2
Patch: nemerle-0.3.2-readline5.patch
Patch1: nemerle-0.9.3-pkgconfig.patch
License: BSD
Group: Development/Other
Url: http://nemerle.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: mono
%if %build_nant
BuildRequires: nant
%endif
BuildRequires: glade-sharp-devel
BuildRequires: emacs-bin
# for cs2n
#BuildRequires: antlr >= 2.7.5
Requires: mono
Requires: nemerle-libs = %version
#gw for nemish
Requires: readline >= 5
Requires: libtermcap
BuildArch: noarch

%description
Nemerle is a new functional language designed from the ground up for
the .NET platform. Nemerle supports: object oriented and imperative
.NET concepts, variant datatypes, matching, higher order functions and
powerful macro system. It has simple, C#-like syntax and makes access
to imperative features easy, and thus is easy to learn.

%package libs
Group: System/Libraries
Summary: Nemerle runtime environment

%description libs
Nemerle is a new functional language designed from the ground up for
the .NET platform. Nemerle supports: object oriented and imperative
.NET concepts, variant datatypes, matching, higher order functions and
powerful macro system. It has simple, C#-like syntax and makes access
to imperative features easy, and thus is easy to learn.

This contains the libraries needed to run programs written in Nemerle.

%prep
%setup -q
%patch -p1 -b .dllimport
%patch1 -p1 -b .pkgconfig
perl -pi -e 's/\r//' $(find snippets/ -type f )

%build
./configure --prefix=%_prefix --libdir=%_prefix/lib --mandir=%_mandir --disable-bar
make

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std PKGCONFIGDIR=%pkgconfigdir
install -m 644 tools/nemerlish/nemish.exe.config %buildroot%_bindir
mkdir %buildroot%_mandir/man1
mv %buildroot%_mandir/ncc.1 %buildroot%_mandir/man1
mkdir -p %buildroot%_sysconfdir/emacs/site-start.d/
cat > %buildroot%_sysconfdir/emacs/site-start.d/%name.el << EOF
(autoload 'nemerle-mode "nemerle" "Major mode for editing Nemerle programs" t)
(add-to-list 'auto-mode-alist
'("\\\\.n$" . nemerle-mode))
EOF
cd misc
emacs -batch -q -f batch-byte-compile nemerle.el
mkdir -p %buildroot%_datadir/emacs/site-lisp/
install -m 644 nemerle.el nemerle.elc %buildroot%_datadir/emacs/site-lisp/
mkdir -p %buildroot%_datadir/vim/syntax
cp nemerle.vim %buildroot%_datadir/vim/syntax


%clean
rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr(-,root,root)
%doc README AUTHORS NEWS ChangeLog
%doc snippets doc/html/
%config(noreplace) %_sysconfdir/emacs/site-start.d/%name.el
%_datadir/emacs/site-lisp/*
%_datadir/vim/syntax/nemerle.vim
%_bindir/nemish
%_bindir/nemish.exe.config
%_bindir/ncc
%_bindir/cs2n
%attr(755,root,root) %_bindir/*.exe
%monodir/gac/Nemerle.Compiler/
%monodir/gac/Nemerle.Macros/
%monodir/gac/Nemerle.CSharp*
%monodir/gac/Nemerle.Evaluation
%monodir/gac/antlr.runtime
%monodir/nemerle/Nemerle.Compiler.dll*
%monodir/nemerle/Nemerle.Evaluation.dll*
%monodir/nemerle/Nemerle.Macros.dll*
%monodir/nemerle/Nemerle.CSharp*
%monodir/nemerle/antlr.runtime.dll*
%_mandir/man1/ncc.1*
%pkgconfigdir/nemerle.pc
%if %build_nant
%_datadir/NAnt/bin/Nemerle.NAnt.Tasks.dll
%endif
#%ghost %_bindir/ncc.exe.so
#%ghost %_bindir/nemish.exe.so
#%ghost %_bindir/cs2n.exe.so

%files libs
%defattr(-,root,root)
%doc COPYRIGHT
%dir %monodir/nemerle
%monodir/gac/Nemerle/
%monodir/nemerle/Nemerle.dll*



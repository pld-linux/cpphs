%define		pkgname	cpphs
Summary:	A liberalised re-implementation of cpp, the C pre-processor
Name:		cpphs
Version:	1.13.1
Release:	3
License:	LGPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/cpphs/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4fe8b5c71068e97602b0f45facd76be3
URL:		http://haskell.org/cpphs/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Obsoletes:	cpphs-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
Cpphs is a re-implementation of the C pre-processor that is both more
compatible with Haskell, and itself written in Haskell so that it can
be distributed with compilers.

This version of the C pre-processor is pretty-much feature-complete
and compatible with traditional (K&R) pre-processors. Additional
features include: a plain-text mode; an option to unlit literate code
files; and an option to turn off macro-expansion.

%package prof
Summary:	Profiling cpphs library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca cpphs dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling cpphs library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca cpphs dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q

%build
runhaskell Setup.hs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%attr(755,root,root) %{_bindir}/cpphs
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/*.p_hi

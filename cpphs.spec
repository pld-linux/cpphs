#
# Conditional build:
%bcond_without	prof	# profiling library

%define		pkgname	cpphs
Summary:	A liberalised re-implementation of cpp, the C pre-processor
Summary(pl.UTF-8):	Swobodniejsza reimplementacja cpp (preprocesora C)
Name:		cpphs
Version:	1.20.9.1
Release:	2
License:	LGPL
Group:		Development/Languages
# Source0Download: http://hackage.haskell.org/package/cpphs
Source0:	http://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a3a9902c2de8820e9aa022fd632645fb
URL:		http://haskell.org/cpphs/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-directory
BuildRequires:	ghc-time
BuildRequires:	ghc-polyparse >= 1.13
%if %{with prof}
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-directory-prof
BuildRequires:	ghc-time-prof
BuildRequires:	ghc-polyparse-prof >= 1.13
BuildRequires:	ghc-prof >= 6.12.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base < 5
Requires:	ghc-base >= 3
Requires:	ghc-directory
Requires:	ghc-time
Requires:	ghc-polyparse >= 1.9
Obsoletes:	cpphs-doc < 1.13.1-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Cpphs is a re-implementation of the C pre-processor that is both more
compatible with Haskell, and itself written in Haskell so that it can
be distributed with compilers.

This version of the C pre-processor is pretty-much feature-complete
and compatible with traditional (K&R) pre-processors. Additional
features include: a plain-text mode; an option to unlit literate code
files; and an option to turn off macro-expansion.

%description -l pl.UTF-8
Cpphs to reimplementacja preprocesora C, która jest bardziej zgodna z
Haskellem, a jednocześnie sama napisana w Haskellu, więc może być
rozprowadzania z kompilatorami.

Ta wersja preprocesora C jest w większości kompletna pod względem
funkcjonalności i zgodna z tradycyjnymi preprocesorami (K&R).
Dodatkowe funkcje obejmują m.in.: tryb zwykłego tekstu, opcję do
wyłączania rozwijania makr.

%package prof
Summary:	Profiling cpphs library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca cpphs dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof < 5
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-directory-prof
Requires:	ghc-time-prof
Requires:	ghc-polyparse-prof >= 1.13

%description prof
Profiling cpphs library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca cpphs dla GHC. Powinna być zainstalowana kiedy
potrzebujemy systemu profilującego z GHC.

%prep
%setup -q

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
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
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScpphs-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScpphs-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScpphs-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScpphs-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Preprocessor/Cpphs/*.p_hi
%endif

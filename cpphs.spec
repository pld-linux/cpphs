%define		pkgname	cpphs
Summary:	A liberalised re-implementation of cpp, the C pre-processor
Name:		cpphs
Version:	1.13
Release:	1
License:	LGPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/cpphs/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	05175b9b3fff129f9f3d9952040e3656
URL:		http://haskell.org/cpphs/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
Cpphs is a re-implementation of the C pre-processor that is both more
compatible with Haskell, and itself written in Haskell so that it can
be distributed with compilers.

This version of the C pre-processor is pretty-much feature-complete
and compatible with traditional (K&R) pre-processors. Additional
features include: a plain-text mode; an option to unlit literate code
files; and an option to turn off macro-expansion.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q

%build
runhaskell Setup.hs configure -v2 \
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
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc

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
%doc CHANGELOG README docs/design docs/index.html
%attr(755,root,root) %{_bindir}/cpphs
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf
%{_libdir}/%{ghcdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*

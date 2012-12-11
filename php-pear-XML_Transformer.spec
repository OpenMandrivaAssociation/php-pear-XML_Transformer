%define		_class		XML
%define		_subclass	Transformer
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(XML/Transformer/Tests/TestNamespace.php)\\|pear(XML/Transformer/Tests/TransformerTest.php)

Name:		php-pear-%{upstream_name}
Version:	1.1.1
Release:	%mkrel 7
Summary:	XML transformations in PHP
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/XML_Transformer/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
With the XML_Transformer class one can easily bind PHP functionality
to XML tags, thus transforming the input XML tree into an output XML
tree without the need for XSLT. Single XML elements can be overloaded
with PHP functions, methods and static method calls, XML namespaces
can be registered to be handled by PHP classes.


%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

perl -pi -e "s|PHPUnit2|PHPUnit|g" %{upstream_name}-%{version}/Transformer/Tests/*

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{upstream_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/README
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


%changelog
* Fri Dec 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-7mdv2012.0
+ Revision: 742312
- fix major breakage by careless packager

* Fri May 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-6
+ Revision: 679613
- mass rebuild

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-5mdv2011.0
+ Revision: 613799
- the mass rebuild of 2010.1 packages

* Wed Nov 11 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-4mdv2010.1
+ Revision: 464968
- spec cleanup
- use pear installer
- don't ship tests, even in documentation
- own all directories
- use rpm filetriggers starting from mandriva 2010.1

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 1.1.1-3mdv2010.0
+ Revision: 441767
- rebuild

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-2mdv2009.1
+ Revision: 322991
- rebuild

* Sat Nov 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-1mdv2009.1
+ Revision: 305818
- update to new version 1.1.1

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-11mdv2009.0
+ Revision: 237171
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-10mdv2008.1
+ Revision: 112114
- really fix deps

* Fri Nov 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-9mdv2008.1
+ Revision: 107008
- PHPUnit2/PHPUnit

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0-8mdv2008.0
+ Revision: 90159
- rebuild


* Sat Nov 11 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-7mdv2007.0
+ Revision: 82939
- Import php-pear-XML_Transformer

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-7mdk
- new group (Development/PHP)

* Fri Aug 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-6mdk
- rebuilt to fix auto deps

* Wed Aug 10 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-5mdk
- rebuilt to use new pear auto deps/reqs from pld

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-4mdk
- fix deps

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-3mdk
- reworked the %%post and %%preun stuff, like in conectiva
- fix deps

* Wed Jul 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-2mdk
- fix deps

* Tue Jul 19 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdk
- initial Mandriva package (PLD import)


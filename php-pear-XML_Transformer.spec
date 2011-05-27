%define		_class		XML
%define		_subclass	Transformer
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(XML/Transformer/Tests/TestNamespace.php)\\|pear(XML/Transformer/Tests/TransformerTest.php)

Name:		php-pear-%{upstream_name}
Version:	1.1.1
Release:	%mkrel 6
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
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/README
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml

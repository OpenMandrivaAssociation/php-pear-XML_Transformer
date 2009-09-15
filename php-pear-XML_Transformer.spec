%define		_class		XML
%define		_subclass	Transformer
%define		_status		stable
%define		_pearname	%{_class}_%{_subclass}

%define		_requires_exceptions pear(XML/Transformer/Tests/TestNamespace.php)\\|pear(XML/Transformer/Tests/TransformerTest.php)

Summary:	%{_pearname} - XML transformations in PHP
Name:		php-pear-%{_pearname}
Version:	1.1.1
Release:	%mkrel 3
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/XML_Transformer/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
With the XML_Transformer class one can easily bind PHP functionality
to XML tags, thus transforming the input XML tree into an output XML
tree without the need for XSLT. Single XML elements can be overloaded
with PHP functions, methods and static method calls, XML namespaces
can be registered to be handled by PHP classes.

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

perl -pi -e "s|PHPUnit2|PHPUnit|g" %{_pearname}-%{version}/Transformer/Tests/*

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/{Driver,Namespace}

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}
install %{_pearname}-%{version}/%{_subclass}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}
install %{_pearname}-%{version}/%{_subclass}/Driver/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Driver
install %{_pearname}-%{version}/%{_subclass}/Namespace/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Namespace

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/{README,%{_subclass}/Tests}
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}
%{_datadir}/pear/packages/%{_pearname}.xml

# TODO:
# - get rid of bundled jars. Use system libraries.
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java

%define		srcname	xstream
Summary:	Simple library to serialize objects to XML and back again
Name:		java-xstream
Version:	1.3.1
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://repository.codehaus.org/com/thoughtworks/xstream/xstream-distribution/%{version}/xstream-distribution-%{version}-src.zip
# Source0-md5:	3a129d9bdf88e385424a917c59e284e2
URL:		http://xstream.codehaus.org/
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	ant-trax
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XStream is a simple library to serialize objects to XML and back
again.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}

%build

cd xstream
%ant all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a xstream/target/xstream-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -sf %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a xstream/target/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# run tests (takes long time)

%include	/usr/lib/rpm/macros.java

%define		srcname	xstream
Summary:	XStream
Name:		java-xstream
Version:	1.3.1
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://repository.codehaus.org/com/thoughtworks/xstream/xstream-distribution/%{version}/xstream-distribution-%{version}-src.zip
# Source0-md5:	3a129d9bdf88e385424a917c59e284e2
URL:		http://xstream.codehaus.org/
BuildRequires:	ant
%{?with_tests:BuildRequires:	ant-junit >= 1.5}
BuildRequires:	java-sun
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	junit >= 3.8.1}
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XStream

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
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a target/commons-io-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf commons-io-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-io.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
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

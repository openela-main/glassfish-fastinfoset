Name:          glassfish-fastinfoset
Version:       1.2.13
Release:       9%{?dist}
Summary:       Fast Infoset
License:       ASL 2.0
URL:           https://fi.java.net
# svn export https://svn.java.net/svn/fi~svn/tags/fastinfoset-project-1.2.13/ glassfish-fastinfoset-1.2.13
# find glassfish-fastinfoset-1.2.13/ -name '*.class' -delete
# find glassfish-fastinfoset-1.2.13/ -name '*.jar' -delete
# rm -rf glassfish-fastinfoset-1.2.13/roundtrip-tests
# tar czf glassfish-fastinfoset-1.2.13-src-svn.tar.gz glassfish-fastinfoset-1.2.13
Source0:       %{name}-%{version}-src-svn.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt
# add xmlstreambuffer 1.5.x support
Patch0:        %{name}-1.2.12-utilities-FastInfosetWriterSAXBufferProcessor.patch

BuildRequires: maven-local
BuildRequires: mvn(com.sun.xml.stream.buffer:streambuffer)
BuildRequires: mvn(com.sun.xsom:xsom)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.java:jvnet-parent:pom:)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

%description
Fast Infoset specifies a standardized binary encoding for the XML Information
Set. An XML infoset (such as a DOM tree, StAX events or SAX events in
programmatic representations) may be serialized to an XML 1.x document or, as
specified by the Fast Infoset standard, may be serialized to a fast infoset
document.  Fast infoset documents are generally smaller in size and faster to
parse and serialize than equivalent XML documents.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0

cp %{SOURCE1} .

# Remove wagon-webdav
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-antrun-extended-plugin
%pom_remove_plugin org.sonatype.plugins:nexus-staging-maven-plugin
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin

%pom_disable_module roundtrip-tests
%pom_disable_module samples

# Disable default-jar execution of maven-jar-plugin, which is causing
# problems with version 3.0.0 of the plugin.
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
 <execution>
  <id>default-jar</id>
  <phase>skip</phase>
 </execution>" fastinfoset

%mvn_file :FastInfoset %{name}
%mvn_file :FastInfosetUtilities %{name}-utilities

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license copyright.txt LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%license copyright.txt LICENSE-2.0.txt

%changelog
* Fri May 25 2018 Michael Simacek <msimacek@redhat.com> - 1.2.13-9
- Regenerate BRs

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 1.2.13-5
- add missing build requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1.2.13-2
- introduce license macro

* Wed Jan 21 2015 gil cattaneo <puntogil@libero.it> 1.2.13-1
- update to 1.2.13
- Fix URL
- Add license text

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2.12-10
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.2.12-9
- rebuilt rhbz#992387
- add xmlstreambuffer and jvnet-parent support
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Juan Hernandez <juan.hernandez@redhat.com> - 1.2.12-7
- Remove the wagon-webdav build extension (rhbz 914033)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2.12-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 7 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2.12-3
- Changed name from glassfish-fi to glassfish-fastinfoset

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2.12-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.2.12-1
- Initial packaging

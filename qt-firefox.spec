# Conditional build:
%bcond_with	ft218	# compile with freetype >= 2.1.8
%bcond_with	cvs
#
%define 	_snap	041128
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		qt-firefox
Version:	1.0
Release:	0.%{_snap}.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
%if %{without cvs}
Source0:	http://ep09.pld-linux.org/~djurban/snap/firefox-%{_snap}.tar.bz2
# Source0-md5:	66393c13b9877a8519fba9869063f7be
%else
Source0:	kdesource.tar.gz
%endif
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-nss.patch
Patch2:		%{name}-lib_path.patch
Patch3:		%{name}-freetype.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	automake
%if %{with ft218}
BuildRequires:	freetype-devel >= 1:2.1.8
%else
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	freetype-devel < 1:2.1.8
BuildConflicts:	freetype-devel = 2.1.8
%endif
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nss-devel >= 3.8
BuildRequires:	nspr-devel >= 1:4.5.0-1
Conflicts:	mozilla-firefox
Requires:	%{name}-lang-resources = %{version}
%if %{with ft218}
Requires:	freetype >= 1:2.1.3
%else
Requires:	freetype >= 2.1.3
Requires:	freetype < 1:2.1.8
Conflicts:	freetype = 2.1.8
%endif
Requires:	nss >= 3.8
PreReq:		XFree86-Xvfb
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}
# mozilla and firefox provide their own versions
%define		_noautoreqdep	libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libnspr4.so
%define		_noautoprovfiles libnspr4.so libplc4.so libplds4.so

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package lang-en
Summary:	English resources for Mozilla-firefox
Summary(pl):	Anglojêzyczne zasoby dla Mozilla-FireFox
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla-firefox

%description lang-en -l pl
Anglojêzyczne zasoby dla Mozilla-FireFox

%prep
%setup -q -n mozilla %{?with_cvs: -D}
# Seems the firefox team has added their own gcc3 fixes for alpha asm.
#patch0 -p1
%patch1 -p1
%patch2 -p1
%{?with_ft218:%patch3 -p1}

%build
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
export MOZ_PHOENIX="1"
export BUILD_OFFICIAL="1"
export MOZILLA_OFFICIAL="1"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf
%configure2_13 \
%if %{?debug:1}0
	--enable-debug \
	--enable-debug-modules \
%else
	--disable-debug \
	--disable-debug-modules \
%endif
	--disable-composer \
	--disable-dtd-debug \
	--disable-installer \
	--disable-jsd \
	--disable-ldap \
	--disable-mailnews \
	--disable-tests \
	--disable-gnomevfs \
	--disable-gnomeui \
	--disable-static \
	--disable-xprint \
	--enable-crypto \
	--disable-pango \
	--enable-freetype2 \
	--enable-mathml \
	--enable-optimize="%{rpmcflags}" \
	--enable-plaintext-editor-only \
	--enable-reorder \
	--enable-strip \
	--enable-strip-libs \
	--enable-xinerama \
	--disable-xft \
	--enable-xterm-updates \
	--enable-default-toolkit="qt" \
	--enable-application="browser" \
	--with-pthreads \
	--with-system-nspr \
	--with-system-jpeg \
	--with-system-png \
	--with-system-zlib \
	--enable-single-profile \
	--disable-profilesharing 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-firefox" \
	MOZILLA_BIN="\$(DIST)/bin/firefox-bin" \
	EXCLUDE_NSPR_LIBS=1

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-firefox-*-linux-gnu.tar.gz

install other-licenses/branding/firefox/content/icon32.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

grep locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-en-US-installed-chrome.txt
grep -v locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-misc-installed-chrome.txt

rm -rf US classic comm embed-sample en-{US,mac,unix,win} modern pipnss pippki toolkit
rm -f en-win.jar en-mac.jar embed-sample.jar modern.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt > %{_firefoxdir}/chrome/installed-chrome.txt

unset MOZILLA_FIVE_HOME || :
MOZILLA_FIVE_HOME=%{_firefoxdir}
export MOZILLA_FIVE_HOME

# PATH
PATH=%{_firefoxdir}:$PATH
export PATH

# added /usr/lib : don't load your local library
LD_LIBRARY_PATH=%{_firefoxdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

/sbin/ldconfig || :

%{_firefoxdir}/regxpcom >/dev/null  || echo "E: regxpcom was exited: $?" >&2
%{_firefoxdir}/regchrome >/dev/null || echo "E: regchrome was exited: $?" >&2

TDIR=`mktemp -d /tmp/mozilla-firefox-pkg.XXXXXX` || exit 1
HOME="$TDIR"
export TDIR HOME

mkdir -p $TDIR/.mozilla/firefox/default
cp -rf %{_firefoxdir}/defaults/profile/* $TDIR/.mozilla/firefox/default

# preseed profiles.ini
cat > $TDIR/.mozilla/firefox/profiles.ini <<EOF
[General]
StartWithLastProfile=1

[Profile0]
Name=default
IsRelative=1
Path=default

EOF


( \
	/usr/X11R6/bin/Xvfb :69 -nolisten tcp -ac -terminate >/dev/null 2>&1 & \
	xvfb_pid=${!}; \
	DISPLAY=:69 %{_firefoxdir}/firefox-bin -list-global-items >/dev/null 2>&1 & \
	sleep 15; \
	kill ${xvfb_pid} >/dev/null 2>&1 \
)

rm -rf $TDIR

%postun
if [ "$1" != "0" ]; then
	umask 022
	cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt
fi

%preun
if [ "$1" == "0" ]; then
  rm -rf %{_firefoxdir}/chrome/overlayinfo
  rm -rf %{_firefoxdir}/components
  rm -f  %{_firefoxdir}/chrome/*.rdf
  rm -rf %{_firefoxdir}/extensions
fi

%post lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%postun lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%{_firefoxdir}/components/myspell
%{_firefoxdir}/plugins
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%dir %{_firefoxdir}/init.d
%attr(755,root,root) %{_firefoxdir}/*.so
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/reg*
%attr(755,root,root) %{_firefoxdir}/x*
%attr(755,root,root) %{_firefoxdir}/T*
%ifarch %{ix86}
%attr(755,root,root) %{_firefoxdir}/elf-dynstr-gc
%endif
%{_firefoxdir}/bloaturls.txt
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/browser.jar
# -chat subpackage?
#%{_firefoxdir}/chrome/chatzilla.jar
%{_firefoxdir}/chrome/classic.jar
%{_firefoxdir}/chrome/comm.jar
%{_firefoxdir}/chrome/content-packs.jar
%{_firefoxdir}/chrome/help.jar
# -dom-inspector subpackage?
#%{_firefoxdir}/chrome/inspector.jar
%{_firefoxdir}/chrome/modern.jar
%{_firefoxdir}/chrome/pip*.jar
%{_firefoxdir}/chrome/toolkit.jar
%{_firefoxdir}/chrome/mozilla-firefox-misc-installed-chrome.txt
%{_firefoxdir}/chrome/icons/default

%files lang-en
%defattr(644,root,root,755)
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/mozilla-firefox-en-US-installed-chrome.txt

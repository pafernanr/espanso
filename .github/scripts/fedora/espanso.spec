Name:           espanso
Version:        2.4.0
Release:        1%{?dist}
Summary:        Cross-platform Text Expander written in Rust

License:        GPL-3.0-only
URL:            https://espanso.org
Source0:        https://github.com/espanso/espanso/archive/v%{version}/espanso-%{version}.tar.gz

# is_espanso_in_path() only checks /usr/local/bin; add /usr/bin for RPM installs
Patch0:         espanso-fix-bin-path.patch

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  wxGTK-devel

Conflicts:      espanso-wayland

%description
Espanso detects when you type a specific keyword and replaces it with something
else. It is useful to save time writing emails, code, or any other text you find
yourself typing over and over.

This package contains the X11 variant.

%package        wayland
Summary:        Espanso text expander for Wayland
Requires:       wl-clipboard
Conflicts:      espanso

%description    wayland
Espanso detects when you type a specific keyword and replaces it with something
else. It is useful to save time writing emails, code, or any other text you find
yourself typing over and over.

This package contains the Wayland variant.

%prep
%autosetup -n espanso-%{version} -p1

%build
cargo build --release --no-default-features --features modulo,vendored-tls
cp target/release/espanso espanso-x11

cargo build --release --no-default-features --features modulo,vendored-tls,wayland
cp target/release/espanso espanso-wayland-bin

%install
install -Dpm 0755 espanso-x11 %{buildroot}%{_bindir}/espanso
install -Dpm 0755 espanso-wayland-bin %{buildroot}%{_bindir}/espanso-wayland

install -Dpm 0644 espanso/src/res/linux/icon.png \
    %{buildroot}%{_datadir}/pixmaps/espanso.png

install -Dpm 0644 espanso/src/res/linux/espanso.desktop \
    %{buildroot}%{_datadir}/applications/espanso.desktop
sed -i 's/^Icon=icon$/Icon=espanso/' %{buildroot}%{_datadir}/applications/espanso.desktop

install -d %{buildroot}%{_userunitdir}
cat > %{buildroot}%{_userunitdir}/espanso.service << 'EOF'
[Unit]
Description=Espanso - Text Expander

[Service]
ExecStart=%{_bindir}/espanso launcher
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/espanso.desktop

%post wayland
ln -sf espanso-wayland %{_bindir}/espanso

%postun wayland
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/espanso
fi

%files
%license LICENSE
%doc README.md
%caps(cap_dac_override=p) %{_bindir}/espanso
%{_datadir}/applications/espanso.desktop
%{_datadir}/pixmaps/espanso.png
%{_userunitdir}/espanso.service

%files wayland
%license LICENSE
%doc README.md
%caps(cap_dac_override=p) %{_bindir}/espanso-wayland
%ghost %{_bindir}/espanso
%{_datadir}/applications/espanso.desktop
%{_datadir}/pixmaps/espanso.png
%{_userunitdir}/espanso.service

%changelog
%autochangelog

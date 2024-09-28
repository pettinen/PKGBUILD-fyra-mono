# Maintainer: Jeremias Pettinen <hi@jeremi.as>

pkgbase=fyra-mono
pkgname=(otf-fyra-mono ttf-fyra-mono)
pkgver=3.206
_tag=4.106  # Tags are at Fira Sans' version
pkgrel=1
pkgdesc="Customized version of Mozilla's monospace typeface"
arch=('any')
license=('OFL-1.1-no-RFN')
url='https://github.com/mozilla/Fira'
source=(
    'git+https://github.com/mozilla/Fira.git'
    'git+https://github.com/Templarian/MaterialDesign.git'
    'add_icons.py'
    'change_ttf_name.patch'
    'fontedit.tar'
)
sha256sums=(
    'SKIP'
    'SKIP'
    '26f2880cc660e6eca4158f91c57d3376a67100b1769cab58ac012df5c7573fa0'
    'a1c80b984829069876a0b9459d9beca43fdea902b1ea5a2a7fb5fd21488e5e1b'
    'a59810683a2e650c1d275da4fd4159c1a7f8b23336fdf9ab9147e68ad34b9f33'
)
makedepends=(
    'fontforge'
    'git'
    'python'
    'python-fontmake'
)

function build {
    patch -Np1 -i change_ttf_name.patch

    tar -xf fontedit.tar

    mkdir master_otf
    python -m fontedit -w Fira/otf/FiraMono-Regular.otf > master_otf/FyraMono-Regular.otf
    python -m fontedit -w Fira/otf/FiraMono-Bold.otf > master_otf/FyraMono-Bold.otf
    python add_icons.py master_otf/FyraMono*.otf

    fontmake -g Fira/source/glyphs/FiraMono.glyphs -o ttf
    python add_icons.py master_ttf/FyraMono*.ttf
}

function _package {
    case "$1" in
        otf-fyra-mono)
            provides=(otf-fira-mono)
            conflicts=(otf-fira-mono)
            cd master_otf
            fonts=(FyraMono*.otf)
            installdir=OTF;;
        ttf-fyra-mono)
            provides=(ttf-fira-mono)
            conflicts=(ttf-fira-mono)
            cd master_ttf
            fonts=(FyraMono*.ttf)
            installdir=TTF;;
    esac

    # Prepare destination directory
    install -dm755 "$pkgdir/usr/share/fonts/$installdir"

    # Install fonts
    for font in "${fonts[@]}"; do
        install -m644 "$font" "$pkgdir/usr/share/fonts/$installdir"
    done

    install -D -m644 ../Fira/LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

for _pkgname in ${pkgname[@]}; do
    eval "function package_$_pkgname { _package $_pkgname; }"
done

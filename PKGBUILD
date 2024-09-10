# Maintainer: Jeremias Pettinen <hi@jeremi.as>

pkgbase=fyra-mono
pkgname=(otf-fyra-mono ttf-fyra-mono)
pkgver=3.206
pkgrel=1
pkgdesc="Customized version of Mozilla's monospace typeface"
arch=('any')
license=('OFL-1.1-no-RFN')
url='https://github.com/mozilla/Fira'
source=(
    'git+https://github.com/mozilla/Fira.git'
    'git+https://github.com/Templarian/MaterialDesign.git'
    'add_icons.py'
    'customize.patch'
)
sha256sums=(
    'SKIP'
    'SKIP'
    '8734ad88a8a994111bf322451af25fba722025167257125704b02fe236a801ca'
    '2a21cb3cafe12f625fd50bf97d754b2c9d6474b87f5152aac2b13d16ba9c9111'
)
makedepends=(
    'fontforge'
    'git'
    'python-fontmake'
)

function build {
    patch -Np1 -i customize.patch

    fontmake -g Fira/source/glyphs/FiraMono.glyphs -o otf
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

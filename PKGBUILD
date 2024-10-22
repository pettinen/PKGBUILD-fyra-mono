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
    'customize.py'
    'fontedit.tar'
)
sha256sums=(
    'SKIP'
    'SKIP'
    'd72bce66da4dd77bb19fcdf8252c825397fea1715306536a95ce073b22eb53ea'
    'ae4809e2ed9ce750d07f7d6e64731225c6f9ff7593832427c6532334e14b3eb4'
)
makedepends=(
    'fontforge'
    'git'
    'python'
)

function build {
    tar -xf fontedit.tar
    export PYTHONPATH=.
    python customize.py -w Fira/otf/FiraMono-Regular.otf > FyraMono-Regular.otf
    python customize.py -w Fira/otf/FiraMono-Bold.otf > FyraMono-Bold.otf
    python customize.py -w Fira/ttf/FiraMono-Regular.ttf > FyraMono-Regular.ttf
    python customize.py -w Fira/ttf/FiraMono-Bold.ttf > FyraMono-Bold.ttf
}

function _package {
    case "$1" in
        otf-fyra-mono)
            provides=(otf-fira-mono)
            conflicts=(otf-fira-mono)
            fonts=(FyraMono*.otf)
            installdir=OTF;;
        ttf-fyra-mono)
            provides=(ttf-fira-mono)
            conflicts=(ttf-fira-mono)
            fonts=(FyraMono*.ttf)
            installdir=TTF;;
    esac

    # Prepare destination directory
    install -dm755 "$pkgdir/usr/share/fonts/$installdir"

    # Install fonts
    for font in "${fonts[@]}"; do
        install -m644 "$font" "$pkgdir/usr/share/fonts/$installdir"
    done

    install -D -m644 Fira/LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

for _pkgname in ${pkgname[@]}; do
    eval "function package_$_pkgname { _package $_pkgname; }"
done

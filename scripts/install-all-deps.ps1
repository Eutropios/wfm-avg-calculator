function install-deps {
    <#
    .DESCRIPTION
    Sync virtualenv packages with locked Poetry deps, including docs and dev groups.
    #>
    poetry install --sync --with dev,docs,test
}

install-deps

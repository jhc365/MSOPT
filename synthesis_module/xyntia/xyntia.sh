#!/bin/bash

OPSET="expr"

POSITIONAL=()
while [[ $# -gt 0 ]];do
    key="$1"

    case $key in
        -opset)
            OPSET="$2"
            shift # past argument
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

PWD=$(readlink -f .)
parentDir="$(dirname "$PWD")"

#$parentDir/xyntia/bin/xyntia_$OPSET.exe $@
$parentDir/synthesis_module/xyntia/bin/xyntia_$OPSET.exe $@

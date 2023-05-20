#!/usr/bin/env bash

CLS_BIN="../../../AaronTools/bin"

for cls in `ls ${CLS_BIN}`; do
    cls_path="${CLS_BIN}/${cls}"
    echo $cls_path
    cls_name="${cls%%.py}"
    echo $cls_name
    help_file="${cls_name}_help.txt"
    echo ".. code-block:: text" > $help_file
    echo "" >> $help_file
    while IFS= read -r line; do
        echo "    ${line}" >> $help_file
    done < <(${cls_path} --help)
    rst_file="${cls_name}.rst"
    if [[ -f "$rst_file" ]] ; then
        echo "${rst_file} exists"
    else
        # this hasn't actually been tested
        # the other rst files were made with the python version
        echo "${rst_file} does not exist"
        echo "${cls}" > $rst_file
        for i in `seq 1 ${#cls}` ; do echo -n "-" >> $rst_file; done
        echo ""
        echo ".. include:: ${help_file}"
    fi
done

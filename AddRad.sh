#!/bin/bash

sed -i 's/.asd/.asd.rad/' `find . -name "*.asd.txt"`
rename .asd.txt .asd.rad.txt `find . -name "*.asd.txt"`

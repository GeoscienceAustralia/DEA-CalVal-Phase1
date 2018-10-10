BEGIN {print "    brdf_data = np.array([['', 'brdf0', 'brdf1', 'brdf2'],"}
/SENTINEL/ {print "                          ['"$2"', "$3", "$4", "$5"],"}
END {print "                         ])"}

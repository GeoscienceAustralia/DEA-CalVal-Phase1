BEGIN {print "BAND brdf0 brdf1 brdf2"}
/LANDSAT_8/ {print $2, $3, $4, $5}

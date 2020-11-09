BEGIN {print "BAND brdf0 brdf1 brdf2"}
/SENTINEL/ {print $2, $3, $4, $5}

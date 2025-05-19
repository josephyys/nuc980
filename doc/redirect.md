

# Copy from your machine to the intermediate server
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/tools/nc .

ssh -vvv -i "/home/joseph/project/nuc980/OraDB.pem" -R 0.0.0.0:8084:127.0.0.1:22 -N -T ubuntu@52.197.102.250 -p 8082





# Copy from your machine to the intermediate server
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/tools/nc .
oc whoami -t



### deep search 3003 3004
ssh -vvv -i "/home/joseph/project/nuc980/OraDB.pem" -R 0.0.0.0:3003:127.0.0.1:5173 -N -T ubuntu@52.197.102.250 -p 8082
ssh -vvv -i "/home/joseph/project/nuc980/OraDB.pem" -R 0.0.0.0:3004:127.0.0.1:2024 -N -T ubuntu@52.197.102.250 -p 8082

 sudo ssh -vvv -i "/home/joseph/project/nuc980/OraDB.pem" -R 0.0.0.0:8084:127.0.0.1:2`2 -N -T ubuntu@52.197.102.250 -p 8082


 export SYSROOT=/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot


 ssh -i "/home/joseph/project/nuc980/OraDB.pem" ubuntu@52.197.102.250 -p 8082


###  nuc980 -->3006 
ssh -vvv -i "/Users/joseph/Documents/OraDb.pem" -R 0.0.0.0:3006:192.168.2.2:8080 -N -T ubuntu@52.197.102.250 -p 8082



### 218 --> 3007
ssh -vvv -i "/home/joseph/project/nuc980/OraDB.pem" -R 0.0.0.0:8084:127.0.0.1:22 -N -T ubuntu@52.197.102.250 -p 8082
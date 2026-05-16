for i in $(seq 1 12)
do
    ADDRESS=$(printf '0xA%x' $i)
    i2cget -y 6 0x76 $ADDRESS
done

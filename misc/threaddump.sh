# Number of times to collect data.
LOOP=2
# Interval in seconds between data points.
INTERVAL=20

for ((i=1; i <= $LOOP; i++))
do
   /usr/bin/jstack -l $1 >> jstack_threaddump.out
   echo "thread dump #" $i
   if [ $i -lt $LOOP ]; then
    echo "sleeping..."
    sleep $INTERVAL
  fi
done


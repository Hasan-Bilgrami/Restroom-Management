#/Users/hasan/Desktop/MNNIT/Project/Python Project/driver.sh

echo "Enter minutes to run Sensor Simulators:"
read n

python MQ-137_Simulator.py $n &
python HC-SR04_Soap_Level_Detector.py $n &
python PIR_Movement_Count.py $n &
python DHT_Simulator.py $n &
python leak_detection_sensor.py $n&
python Atlas\ Database\ Initialiser.py $n&
for (( c=0; c<$n; c=c+1 ))
do
sleep 60
python updated3_restroom_management_algo.py
done


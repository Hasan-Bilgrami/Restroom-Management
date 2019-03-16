from random import uniform,randint


"""Odour and Feedback Simulator
Generates Text file with a pair of values: Odour and Feedback.
Both odour and feedback are unrelated and randomly generated.
13/03/2019"""

file_name="Odour_vs_Feedback.txt"


instances=int(input("Enter Number of Instances to Generate:"))
odour_randomvalue=0
feedback_randomvalue=0

s=open(file_name, "w")			#truncates the file

for i in range(instances+1):
	s=open(file_name, "a")
	s.write(str(i)+")"+"\t"+str(round(odour_randomvalue,3))+"\t"+str(feedback_randomvalue)+"\n")
	odour_randomvalue+=uniform(0,0.05)
	feedback_randomvalue=randint(1,5)

s.close()
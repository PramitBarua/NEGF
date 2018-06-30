# NEGF

New feature of this version:
	- Code can identify orthogonal and non-orthogonal system based on the presence
	  of overlap matrix. if overlap matrix (s00, sp1 and sn1) are present in the input 
	  folder then program will identify this system as non-orthogonal system.
	- Program checks the dimension of the input matrix before running NEGF code. If the 
	  matrix are not same in size then program will be terminated. A message will be saved 
	  in the file 'output.out' saying 'Matrix dimension mismatched'
	- Function 'self_energy' is modified. Now, 'self_energy' does not compute sigma. The 
	  calculation of sigma is now done in 'main'

Description of the project
	This code takes hemiltonian matrix, overlap matrix and trasfer matrix to generates density	
	of state(DOS) and transmission of the system. 


install/ run the project:
	main.py -p y -t y (name of the input folder)
	-p for plotting data if -p is not 'y' then it will save the figure but will
	not display
	-t to generate the file 'time.dat', that keeps track of time it took to perform several 
	important calculations.	


how to use the project/ prerequisite to run the project:
	The folder 'input' and 'output' and the file 'main.py' must be in the same 
	directory. 
	'input' folder can contain several folders. However, each folder must 
	contain file 'h00', 'hp1' and 'hn1'. h00 defines the hamiltonian matrix. 
	hp1 and hn1	is the right and left transfer matrix respectively. 
	
	Overlap matrix can be present along size with the hamiltonian matrix.
	
Contact:
	pramit.barua@gmail.com, pramit.barua@student.kit.edu
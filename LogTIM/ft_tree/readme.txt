
input paramaters in main function:
	data_path: raw syslog.
	out_path:  outfile path.

input.dat: 
	raw syslog. The first column of each log is messageType. If your syslogs have no messageType, please delete ‘f.write(pid+" “)’  (the 357-th line of ft-tree.py).

default pruning strategy: 
	when the amount of childern nodes is more than 10, we will prune the childern nodes. If you want to change this paramater, please change ‘if len(self._children) == 10:’ ( the 93-th line row of ft-tree.py)
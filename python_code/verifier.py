#!/usr/bin/python3
def check(query):
	query = query.strip().lower()
	start = ["select", "update", "insert into", "delete from"]
	comparators = ["<", "=", ">", "<=", ">="]
	middle = ["or", "and"]
	cond = False
	li = query.split()
	size = len(li)
	for word in li:
		if word == "where":
			cond = True
	#print(li)
	if cond:
		i = li.index("where")+1
		#print(i)
		while i<size:
			if size-i<3:
				return False
			first = li[i]
			second = li[i+1]
			third = li[i+2]
			if not second in comparators:
				return False
			i = i + 3
			if i<size:
				if not li[i] in middle:
					return False
				elif size-i < 4:
					return False
			i = i + 1
	return True
	
while(True):
	query = input()
	if check(query):
		print("True")
	else :
		print(query)

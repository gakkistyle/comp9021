class cup:
	def __init__(self,col,own,con):
		self.colour = col
		self.owner = own
		self.content = con

	def display_owner(self):
		return self.owner
	def modify_content(self,new_content):
		self.content = new_content

c1 = cup('blue','zqw','Empty')
print(c1.display_owner())
print(c1.content)

c_list = []
c_list.append(c1)
print(c_list[0].colour)
class MazeError(Exception):
	pass

class Maze:
	def __init__(self,filename):
		self.filename = filename
		self.grid = []
		with open(filename) as file:
			i = 0
			for l in file:
				if l.strip() == '':
					continue
				else:
					self.grid.append([])
					for e in l:
						if e.isdigit():
							self.grid[i].append(int(e))								
					i = i+1

		self.checkinput()
		self.num_gates = 0

		self.grid_plus = [[0, 0] for _ in range(len(self.grid))]
		_ = 0
		for row in self.grid:
			for e in row:
				self.grid_plus[_].insert(-1, e)
			_ = _ + 1
		self.grid_plus = [[0] * (len(self.grid[0]) + 2), *self.grid_plus, [0] * (len(self.grid[0]) + 2)]

		#connected walls
		self.set_walls = 0
		self.track = []
		self.trigger = 0
		#the inaccessible points attri
		self.num_inaccessible = 0
		self.num_single_inacc = 0
		self.track_inacc = []
		self.tem_track_inacc = []
		self.warning = 0
		# gates
		self.gates_track = []
		self.gates_already = []
		self.num_accessible = 0
		self.accessible_visted = []
		# cul-de-sacs and entry-exit path
		self.cul_de_sacs = []
		self.num_cul_de_sacs = 0
		self.path = []
		self.okpaths = []
		self.node = []
		self.gatenode = []
		self.deletepath = []
		self.entry_exit_path = []
		self.num_entry_exit_path = 0
		self.analyse_call = 0

	def checkinput(self):
		num_of_row = []
		for l in self.grid:
			if len(l) < 2:
				raise MazeError('Incorrect input.')
			num_of_row.append(len(l))
			for e in l:
				if e not in [0,1,2,3]:
					raise MazeError('Incorrect input.')

		if len(num_of_row) < 2 or len(num_of_row) > 41:
			raise MazeError('Incorrect input.')
		for i in range(0,len(num_of_row)-1):
			if num_of_row[i] != num_of_row[i+1] or num_of_row[i] >31:
				raise MazeError('Incorrect input.')
		for i in range(0,len(self.grid)):
			for j in range(0,len(self.grid[0])):
				if j == len(self.grid[0])-1:
					if self.grid[i][j] != 2 and self.grid[i][j] != 0:
						raise MazeError('Input does not represent a maze.')
				if i == len(self.grid)-1:
					if self.grid[i][j] != 1 and self.grid[i][j] != 0:
						raise MazeError('Input does not represent a maze.')
					if j == len(self.grid[0])-1 and self.grid[i][j] != 0:
						raise MazeError('Input does not represent a maze.')

	def check_walls(self,i, j):
		if self.grid_plus[i][j] == 0:
			return
		elif self.grid_plus[i][j] == 1 and [i,j] not in self.track:
			self.trigger = 1
			self.track.append([i,j])
			if self.grid_plus[i][j+1] != 0 :
				self.check_walls(i,j+1)
			if (self.grid_plus[i-1][j+1] == 2 or self.grid_plus[i-1][j+1] == 3):
				self.check_walls(i-1,j+1)
			if self.grid_plus[i-1][j] == 2 or self.grid_plus[i-1][j] == 3:
				self.check_walls(i-1,j)
			if self.grid_plus[i][j-1] == 1 or self.grid_plus[i][j-1] == 3:
				self.check_walls(i,j-1)
		elif self.grid_plus[i][j] == 2 and [i,j] not in self.track:
			self.trigger = 1
			self.track.append([i,j])
			if self.grid_plus[i+1][j] != 0 :
				self.check_walls(i+1,j)
			if self.grid_plus[i+1][j-1] == 1 or self.grid_plus[i+1][j-1] == 3:
				self.check_walls(i+1,j-1)
			if self.grid_plus[i][j-1] == 1 or self.grid_plus[i][j-1] == 3:
				self.check_walls(i,j-1)
			if self.grid_plus[i-1][j] == 2 or self.grid_plus[i-1][j] == 3:
				self.check_walls(i-1,j)
		elif self.grid_plus[i][j] == 3 and [i,j] not in self.track:
			self.trigger = 1
			self.track.append([i,j])
			if self.grid_plus[i][j+1] != 0:
				self.check_walls(i,j+1)
			if self.grid_plus[i-1][j+1] == 2 or self.grid_plus[i-1][j+1] == 3:
				self.check_walls(i-1,j+1)
			if self.grid_plus[i-1][j] == 2 or self.grid_plus[i-1][j] == 3:
				self.check_walls(i-1,j)
			if self.grid_plus[i][j-1] == 1 or self.grid_plus[i][j-1] == 3:
				self.check_walls(i,j-1)
			if self.grid_plus[i+1][j] != 0 :
				self.check_walls(i+1,j)
			if self.grid_plus[i+1][j-1] == 1 or self.grid_plus[i+1][j-1] == 3:
				self.check_walls(i+1,j-1)
		else :
			return

	def check_inacc_points(self,i,j):
		if i == 0 or i == len(self.grid_plus)-1 or j ==0 or j == len(self.grid_plus[0])-1:
			self.warning = 1
			self.num_single_inacc = 0
			return
		if self.warning == 1:
			return
		elif [i,j] not in self.tem_track_inacc  and [i,j] not in self.track_inacc:
			self.tem_track_inacc.append([i,j])
			self.num_single_inacc += 1
			# index 0:up index 1:right index 2:down index 3:left
			dir = [1,1,1,1]
			if self.grid_plus[i][j] == 3:
				dir[0] = 0
				dir[3] = 0
			if self.grid_plus[i][j] == 1:
				dir[0] = 0
			if self.grid_plus[i][j] == 2:
				dir[3] = 0
			if self.grid_plus[i][j+1] == 2 or self.grid_plus[i][j+1] == 3:
				dir[1] = 0
			if self.grid_plus[i+1][j] == 1 or self.grid_plus[i+1][j] == 3:
				dir[2] = 0
			if dir[0] == 1:
				self.check_inacc_points(i-1,j)
			if dir[1] == 1:
				self.check_inacc_points(i,j+1)
			if dir[2] == 1:
				self.check_inacc_points(i+1,j)
			if dir[3] == 1:
				self.check_inacc_points(i,j-1)
		else:
			return

	def check_accessible_area(self,i,j):
		if [i,j] in self.accessible_visted:
			return
		if i == 0 or i == len(self.grid_plus) - 1 or j == 0 or j == len(self.grid_plus[0]) - 1:
			return
		else:
			self.accessible_visted.append([i, j])
			dir = [1, 1, 1, 1]
			if [i,j] in self.gates_track and j == len(self.grid_plus[0])-2:
				dir = [0, 0, 0, 1]
			if [i,j] in self.gates_track and i == len(self.grid_plus)-2:
				dir = [1, 0, 0, 0]
			if self.grid_plus[i][j] == 3:
				dir[0] = 0
				dir[3] = 0
			if self.grid_plus[i][j] == 1:
				dir[0] = 0
			if self.grid_plus[i][j] == 2:
				dir[3] = 0
			if self.grid_plus[i][j + 1] == 2 or self.grid_plus[i][j + 1] == 3:
				dir[1] = 0
			if self.grid_plus[i + 1][j] == 1 or self.grid_plus[i + 1][j] == 3:
				dir[2] = 0
			if dir[0] == 1:
				self.check_accessible_area(i-1,j)
			if dir[1] == 1:
				self.check_accessible_area(i,j+1)
			if dir[2] == 1:
				self.check_accessible_area(i+1,j)
			if dir[3] == 1:
				self.check_accessible_area(i,j-1)
			if [i, j] in self.gates_track and [i, j] not in self.gates_already:
				self.gates_already.append([i, j])
				return
			else:
				return


	def check_all_paths(self,i,j):
		if [i,j] in self.path or [i,j] in self.deletepath:
			return
		if i == 0 or i == len(self.grid_plus) - 1 or j == 0 or j == len(self.grid_plus[0]) - 1:
			return
		else:
			self.path.append([i, j])
			if [i, j] in self.gates_track:
				self.gatenode.append([i,j])
			dir = [1,1,1,1]
			if [i,j] in self.gates_track and j == len(self.grid_plus[0])-2:
				dir = [0, 0, 0, 1]
			if [i,j] in self.gates_track and i == len(self.grid_plus)-2:
				dir = [1, 0, 0, 0]
			if self.grid_plus[i][j] == 3:
				dir[0] = 0
				dir[3] = 0
			if self.grid_plus[i][j] == 1 :
				dir[0] = 0
			if self.grid_plus[i][j] == 2 :
				dir[3] = 0
			if self.grid_plus[i][j + 1] == 2 or self.grid_plus[i][j + 1] == 3 :
				dir[1] = 0
			if self.grid_plus[i + 1][j] == 1 or self.grid_plus[i + 1][j] == 3 :
				dir[2] = 0
			if sum(dir) >= 3 and [i,j] not in self.cul_de_sacs:
				self.node.append([i,j])
			if sum(dir) == 1 and i != len(self.grid_plus)-2 and j!=len(self.grid_plus[0])-2 and [i,j] not in self.cul_de_sacs :
				self.num_cul_de_sacs += 1
				self.check_cul_de_sacs(i,j)
			if dir[0] == 1:
				self.check_all_paths(i-1,j)
			if dir[1] == 1:
				self.check_all_paths(i,j+1)
			if dir[2] == 1:
				self.check_all_paths(i+1,j)
			if dir[3] == 1:
				self.check_all_paths(i,j-1)
			if [i,j] in self.node:
				count_cul = 0
				if [i+1,j] in self.cul_de_sacs and dir[2] == 1:
					count_cul += 1
				if [i-1,j] in self.cul_de_sacs and dir[0] == 1:
					count_cul += 1
				if [i,j+1] in self.cul_de_sacs and dir[1] == 1:
					count_cul += 1
				if [i,j-1] in self.cul_de_sacs and dir[3] == 1:
					count_cul += 1
				if sum(dir)-1 == count_cul :
					self.node.remove([i,j])
					self.deletepath.append([i,j])
					self.num_cul_de_sacs = self.num_cul_de_sacs - (count_cul-1)
					self.check_cul_de_sacs(i,j)

	def check_cul_de_sacs(self,i,j):
		if [i,j] in self.cul_de_sacs:
			return
		if i == 0 or j == 0:
			return
		if [i,j] in self.gates_track and (i == len(self.grid_plus)-2 or j == len(self.grid_plus[0])-2):
			self.deletepath.append([i,j])
			self.path.remove([i,j])
			return
		if [i,j] in self.node:
			return
		else:
			self.cul_de_sacs.append([i,j])
			self.deletepath.append([i,j])
			self.path.remove([i,j])
			dir = [1, 1, 1, 1]
			if self.grid_plus[i][j] == 3:
				dir[0] = 0
				dir[3] = 0
			if self.grid_plus[i][j] == 1 :
				dir[0] = 0
			if self.grid_plus[i][j] == 2 :
				dir[3] = 0
			if self.grid_plus[i][j + 1] == 2 or self.grid_plus[i][j + 1] == 3 :
				dir[1] = 0
			if self.grid_plus[i + 1][j] == 1 or self.grid_plus[i + 1][j] == 3 :
				dir[2] = 0
			if dir[0] == 1:
				self.check_cul_de_sacs(i-1,j)
			if dir[1] == 1:
				self.check_cul_de_sacs(i,j+1)
			if dir[2] == 1:
				self.check_cul_de_sacs(i+1,j)
			if dir[3] == 1:
				self.check_cul_de_sacs(i,j-1)
			else:
				return

	def analyse(self):
		self.analyse_call = 1
		#number of gates
		for j in range(len(self.grid[0])-1):
			if self.grid[0][j] == 0 or self.grid[0][j] == 2:
				self.gates_track.append([1,j+1])
				self.num_gates += 1
		for i in range(len(self.grid)-1):
			if self.grid[i][-1] == 0:
				self.gates_track.append([i+1,len(self.grid_plus[0])-2])
				self.num_gates += 1
		for k in range(len(self.grid[-1])-1):
			if self.grid[-1][k] == 0:
				self.gates_track.append([len(self.grid_plus)-2,k+1])
				self.num_gates += 1
		for m in range(len(self.grid)-1):
			if self.grid[m][0] == 0 or self.grid[m][0] == 1:
				self.gates_track.append([m+1,1])
				self.num_gates += 1

		if self.num_gates == 0:
			print('The maze has no gate.')
		elif self.num_gates == 1:
			print('The maze has a single gate.')
		else:
			print('The maze has',self.num_gates,'gates.')


		# number of walls that are all connected
		for i in range(1,len(self.grid_plus)-1):
			for j in range(1,len(self.grid_plus[0])-1):
				self.check_walls(i,j)
				if self.trigger == 1:
					self.set_walls += 1
					self.trigger = 0
		if self.set_walls == 0:
			print('The maze has no wall.')
		elif self.set_walls == 1:
			print('The maze has walls that are all connected.')
		else:
			print('The maze has',self.set_walls,'sets of walls that are all connected.')

		#the num of inaccessible points
		for i in range(1,len(self.grid_plus)-1):
			for j in range(1,len(self.grid_plus[0])-1):
				if self.grid_plus[i][j] == 3:
					self.tem_track_inacc = []
					self.num_single_inacc = 0
					self.check_inacc_points( i, j)
					if self.warning == 1:
						self.warning = 0
						self.num_single_inacc = 0
					self.num_inaccessible += self.num_single_inacc
					if self.num_single_inacc > 0:
						self.track_inacc.extend(self.tem_track_inacc)
		if self.num_inaccessible == 0:
			print('The maze has no inaccessible inner point.')
		elif self.num_inaccessible == 1:
			print('The maze has a unique inaccessible inner point.')
		else:
			print('The maze has',self.num_inaccessible, 'inaccessible inner points.')

		#the num of accessible areas
		for i in range(1,len(self.grid_plus)-1):
			for j in range(1,len(self.grid_plus[0])-1):
				if [i,j] in self.gates_track and [i,j] not in self.gates_already:
					self.check_accessible_area(i,j)
					self.num_accessible += 1

		if self.num_accessible == 0:
			print('The maze has no accessible area.')
		elif self.num_accessible == 1:
			print('The maze has a unique accessible area.')
		else:
			print('The maze has',self.num_accessible,'accessible areas.')

		#num of cul_de_sacs and get paths
		for i in range(1,len(self.grid_plus)-1):
			for j in range(1,len(self.grid_plus[0])-1):
				if [i,j] in self.gates_track and [i,j] not in self.gatenode:
					self.path = []
					self.check_all_paths(i,j)
					if len(self.path) > 0:
						self.okpaths.append(self.path)
		self.cul_de_sacs.sort()

		if self.num_cul_de_sacs == 0:
			print('The maze has no accessible cul-de-sac.')
		elif self.num_cul_de_sacs == 1:
			print('The maze has accessible cul-de-sacs that are all connected.')
		else:
			print('The maze has',self.num_cul_de_sacs,'sets of accessible cul-de-sacs that are all connected.')

		# the num of entry-exit path
		for path in self.okpaths:
			gates_num = 0
			trigger = 1
			for e in path:
				if e in self.gates_track:
					gates_num += 1
				leave_num = 0
				dir = [1, 1, 1, 1]
				if self.grid_plus[e[0]][e[1]] == 3:
					dir[0] = 0
					dir[3] = 0
				if self.grid_plus[e[0]][e[1]] == 1:
					dir[0] = 0
				if self.grid_plus[e[0]][e[1]] == 2:
					dir[3] = 0
				if self.grid_plus[e[0]][e[1] + 1] == 2 or self.grid_plus[e[0]][e[1] + 1] == 3:
					dir[1] = 0
				if self.grid_plus[e[0] + 1][e[1]] == 1 or self.grid_plus[e[0] + 1][e[1]] == 3:
					dir[2] = 0
				if [e[0] + 1, e[1]] in path and dir[2] == 1:
					leave_num += 1
				if [e[0] - 1, e[1]] in path and dir[0] == 1:
					leave_num += 1
				if [e[0], e[1] + 1] in path and dir[1] == 1:
					leave_num += 1
				if [e[0], e[1] - 1] in path and dir[3] == 1:
					leave_num += 1
				if leave_num > 2:
					trigger = 0


			if gates_num > 2 or (gates_num == 1 and path[0] != [1,1]):
				trigger = 0
			if trigger == 1:
				self.num_entry_exit_path += 1
				self.entry_exit_path.append(path)

		if self.num_entry_exit_path == 0:
			print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
		elif self.num_entry_exit_path == 1:
			print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
		else:
			print('The maze has',self.num_entry_exit_path,'entry-exit paths with no intersections not to cul-de-sacs.')



	def display(self):
		if self.analyse_call == 0:
			for j in range(len(self.grid[0]) - 1):
				if self.grid[0][j] == 0 or self.grid[0][j] == 2:
					self.gates_track.append([1, j + 1])
			for i in range(len(self.grid) - 1):
				if self.grid[i][-1] == 0:
					self.gates_track.append([i + 1, len(self.grid_plus[0]) - 2])
			for k in range(len(self.grid[-1]) - 1):
				if self.grid[-1][k] == 0:
					self.gates_track.append([len(self.grid_plus) - 2, k + 1])
			for m in range(len(self.grid) - 1):
				if self.grid[m][0] == 0 or self.grid[m][0] == 1:
					self.gates_track.append([m + 1, 1])
			for i in range(1, len(self.grid_plus) - 1):
				for j in range(1, len(self.grid_plus[0]) - 1):
					if [i, j] in self.gates_track and [i, j] not in self.gatenode:
						self.path = []
						self.check_all_paths(i, j)
						if len(self.path) > 0:
							self.okpaths.append(self.path)
			for path in self.okpaths:
				gates_num = 0
				trigger = 1
				for e in path:
					if e in self.gates_track:
						gates_num += 1
					leave_num = 0
					dir = [1, 1, 1, 1]
					if self.grid_plus[e[0]][e[1]] == 3:
						dir[0] = 0
						dir[3] = 0
					if self.grid_plus[e[0]][e[1]] == 1:
						dir[0] = 0
					if self.grid_plus[e[0]][e[1]] == 2:
						dir[3] = 0
					if self.grid_plus[e[0]][e[1] + 1] == 2 or self.grid_plus[e[0]][e[1] + 1] == 3:
						dir[1] = 0
					if self.grid_plus[e[0] + 1][e[1]] == 1 or self.grid_plus[e[0] + 1][e[1]] == 3:
						dir[2] = 0
					if [e[0] + 1, e[1]] in path and dir[2] == 1:
						leave_num += 1
					if [e[0] - 1, e[1]] in path and dir[0] == 1:
						leave_num += 1
					if [e[0], e[1] + 1] in path and dir[1] == 1:
						leave_num += 1
					if [e[0], e[1] - 1] in path and dir[3] == 1:
						leave_num += 1
					if leave_num > 2:
						trigger = 0
						
				if gates_num > 2 or (gates_num == 1 and path[0] != [1,1]):
					trigger = 0
				if trigger == 1:
					self.entry_exit_path.append(path)
		self.cul_de_sacs.sort()
		with open(self.filename[0:-3]+'tex', 'w') as latex_file:
			print('\\documentclass[10pt]{article}\n'
				  '\\usepackage{tikz}\n'
				  '\\usetikzlibrary{shapes.misc}\n'
				  '\\usepackage[margin=0cm]{geometry}\n'
				  '\\pagestyle{empty}\n'
				  '\\tikzstyle{every node}=[cross out, draw, red]\n'
				  '\n'
				  '\\begin{document}\n'
				  '\n'
				  '\\vspace*{\\fill}\n'
				  '\\begin{center}\n'
				  '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]', file=latex_file
				  )
			#walls
			print('% Walls',file = latex_file)
			#hori
			i = 1
			while i < len(self.grid_plus) - 1:
				j = 1
				while j < len(self.grid_plus[0])-1:
					if self.grid_plus[i][j] == 1 or self.grid_plus[i][j] == 3:
						start_row = i-1
						start_col = j-1
						end_row = i-1
						end_col = j
						j_c = j
						while self.grid_plus[i][j_c+1] == 1 or self.grid_plus[i][j_c+1] == 3:
							end_col = j_c+1
							j_c += 1
						j = j_c
						print(f'    \\draw ({start_col},{start_row}) -- ({end_col},{end_row});',file = latex_file)
					j += 1
				i += 1

			#vertical
			j = 1
			while j < len(self.grid_plus[0])-1:
				i = 1
				while i < len(self.grid_plus)-1:
					if self.grid_plus[i][j] == 2 or self.grid_plus[i][j] == 3:
						start_row = i-1
						start_col = j-1
						end_row = i
						end_col = j-1
						i_c = i
						while self.grid_plus[i_c+1][j] == 2 or self.grid_plus[i_c+1][j] == 3:
							end_row = i_c+1
							i_c += 1
						i = i_c
						print(f'    \\draw ({start_col},{start_row}) -- ({end_col},{end_row});',file = latex_file)
					i += 1
				j += 1

			#pillars
			print('% Pillars', file=latex_file)
			for i in range(1,len(self.grid_plus)-1):
				for j in range(1,len(self.grid_plus[0])-1):
					if self.grid_plus[i][j] == 0:
						if self.grid_plus[i][j-1] == 2 or self.grid_plus[i][j-1] == 0:
							if self.grid_plus[i-1][j] == 1 or self.grid_plus[i-1][j] == 0:
								print(f'    \\fill[green] ({j-1},{i-1}) circle(0.2);',file = latex_file)

			#cul-de-sacs
			print('% Inner points in accessible cul-de-sacs', file=latex_file)
			for p in self.cul_de_sacs:
				row = p[0]
				col = p[1]
				print('    \\node at ('+str(col-0.5)+','+str(row-0.5)+') {};', file=latex_file)


			#entry-exit path
			print('% Entry-exit paths without intersections',file=latex_file)
			draw_path = []
			for path in self.entry_exit_path:
				for e in path:
					draw_path.append(e)
					if e[0] == 1 and (self.grid_plus[e[0]][e[1]] == 0 or self.grid_plus[e[0]][e[1]] == 2):
						draw_path.append([0,e[1]])
					if e[1] == 1 and (self.grid_plus[e[0]][e[1]] == 0 or self.grid_plus[e[0]][e[1]] == 1):
						draw_path.append([e[0],0])

			#horiz
			i = 1
			while i < len(self.grid_plus) - 2:
				j = 0
				while j < len(self.grid_plus[0]) -1 :
					if [i,j] in draw_path and [i,j+1] in draw_path and self.grid_plus[i][j+1] != 2 and self.grid_plus[i][j+1] != 3:
						start_row = i-0.5
						start_col = j-0.5
						end_row = i-0.5
						end_col = j+0.5
						j_c = j+1
						while [i,j_c+1] in draw_path and self.grid_plus[i][j_c+1] != 2 and self.grid_plus[i][j_c+1] != 3:
							end_col += 1
							j_c += 1
						j = j_c
						print(f'    \\draw[dashed, yellow] ({start_col},{start_row}) -- ({end_col},{end_row});',file=latex_file)
					j += 1
				i += 1

			#vertical
			j = 1
			while j < len(self.grid_plus[0])-2:
				i = 0
				while i < len(self.grid_plus) -1:
					if [i,j] in draw_path and [i+1,j] in draw_path and self.grid_plus[i+1][j] != 1 and self.grid_plus[i+1][j] != 3:
						start_row = i-0.5
						start_col = j-0.5
						end_row = i+0.5
						end_col = j-0.5
						i_c = i+1
						while [i_c+1,j] in draw_path and self.grid_plus[i_c+1][j] != 1 and self.grid_plus[i_c+1][j] != 3:
							end_row += 1
							i_c += 1
						i = i_c
						print(f'    \\draw[dashed, yellow] ({start_col},{start_row}) -- ({end_col},{end_row});',file=latex_file)
					i += 1
				j += 1

			print('\\end{tikzpicture}\n'
				  '\\end{center}\n'
				  '\\vspace*{\\fill}\n'
				  '\n'
				  '\\end{document}', file=latex_file
				  )



#maze = Maze('maze_2.txt')
#maze.analyse()
#maze.display()
#print(maze.gates_track)
#print(maze.entry_exit_path)
#print(maze.okpaths)
#print(maze.cul_de_sacs)











			
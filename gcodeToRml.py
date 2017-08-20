#!/usr/bin/env python

import sys


class gcodeToRml:
	
	def __init__(self,input_file):
		self.command_list = []
		self.displacement_units = ''
		self.coordinates_mode = ''
		self.speed_units=''
		self.speed =''
		self.PZ = {'UP':'','DW':'','H':''}
		self.input_file = input_file

	def mm_to_mil(self,pos):
		return pos / 0.0254

	def inch_to_mil(self,pos):
		return pos / 0.0254

	def absolute_pos(self,pos):
		return pos / 0.0254

	def relative_pos(self,pos):
		return pos / 0.0254
	
	def interpret(self):
		for command in self.input_file:
			if command[0] == 'G':
				items_array = command.split()
				if not items_array:
					print("List is empty")
				elif items_array[0] == 'G20' :
					self.displacement_units = self.inch_to_mil
				elif items_array[0] == 'G21' :
					self.displacement_units = self.mm_to_mil
				elif items_array[0] == 'G90' :
					self.coordinates_mode = self.absolute_pos
				elif items_array[0] == 'G91' :
					self.coordinates_mode = self.relative_pos
				elif (items_array[0] == 'G01') or (items_array[0] == 'G00'):
					if items_array[1][0] == 'Z':
						val = float(items_array[1][1:len(items_array[1])-1])
						if val < 0:
							self.PZ['H']='PD'
							self.PZ['DW'] = min(val,self.PZ['DW'])
						else:
							self.PZ['H']='PU'
							self.PZ['UP'] = min(val,self.PZ['UP'])
					elif items_array[1][0] == 'X':
						xy_pos = items_array[1][1:len(items_array[1])].split('Y')
						x_pos = int(round(self.displacement_units(float(xy_pos[0]))))
						y_pos = int(round(self.displacement_units(float(xy_pos[1]))))
						self.command_list.append(self.PZ['H']+str(x_pos)+','+str(y_pos)+';')
			elif command[0] == 'F':
				self.speed = float(command[1:len(command)-1])
			elif command[0] == 'M':
				continue
	def write_rml(self):
		config = 'PA;PA;!PZ'+str(self.PZ['DW'])+','+str(self.PZ['UP'])+';VS2;!MC1;'
		commands = config+''.join(self.command_list)+'MC0;'
		return commands
		




def main():
	print('Gcode to RML converter by HELKAROUI')
	if(len(sys.argv)<2):
		print('No file passed in arguments')
	else:
		gcode_file = open(sys.argv[1],'r')
		rml_file = gcodeToRml(gcode_file)
		rml_file.interpret()
		gcode_file.close()
		print(rml_file.speed)
		print(rml_file.PZ)
		print(rml_file.command_list)
		print(rml_file.write_rml())


if __name__ == '__main__':
	main()
	

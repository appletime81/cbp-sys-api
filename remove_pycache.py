import os

path = os.getcwd()

for root, dirs, files in os.walk(path):
	for dir in dirs:
		if dir == '__pycache__':
			os.system(f'rm -rf {os.path.join(root, dir)}')



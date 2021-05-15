#!/bin/env python3
import sys, re, json, subprocess as sub

PACKAGE_SOLUTION = "config/package-solution.json"


class SpVersion:
	def __init__(self, v):
		if type(v) is str:
			self.version = [int(x) for x in v.split('.')]
		elif type(v) in (list, tuple):
			self.version = [int(x) for x in v]
		else:
			raise TypeError("The type of the version must be a string or a list/tuple")

		assert len(self.version) == 4 , "The length of the version must be 4"

	def next(self):
		self.version[-1] += 1
		nextv = SpVersion(self.version)
		self.version[-1] -= 1
		return nextv

	def __str__(self):
		return ".".join((str(x) for x in self.version))


def load_ps():
	# load the package-solution file
	try:
		with open(PACKAGE_SOLUTION, 'r') as f:
			return json.load(f)
	except:
		print("Unable to open the file "+PACKAGE_SOLUTION+" (are you in the root of the project?)")
		sys.exit(1)

def write_ps(d):
	# update the package-solution file
	try:
		with open(PACKAGE_SOLUTION, 'w') as f:
			f.write(json.dumps(d, indent=2))
	except:
		print("Unable to update the file "+PACKAGE_SOLUTION+" (are you in the root of the project?)")
		sys.exit(1)


try:
	# load the actual version
	d = load_ps()
	old_v = SpVersion(d['solution']['version'])
	package_path = "sharepoint/" + d['paths']['zippedPackage']

	v = input(f"Update the version? {old_v} -> {old_v.next()} [Y/n/x.y.z.k] ")

	if len(v) == 0 or v in 'yY':
		v = old_v.next()
	elif v in 'nN':
		v = old_v
	elif re.match(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", v) is not None:
		v = SpVersion(v)
	else:
		print("if you want to specify the version it must be like x.y.z.k")
		sys.exit(1)

	# upgrade version
	d['solution']['version'] = str(v)
	for f in d['solution'].get('features', []):
		f['version'] = str(v)

	# write back the updated version
	write_ps(d)
	print(f"Solution version: {v}")

	# make the package
	sub.run(["gulp", "clean", *sys.argv[1:]], check=True)
	sub.run(["gulp", "bundle", "--ship", *sys.argv[1:]], check=True)
	sub.run(["gulp", "package-solution", "--ship", *sys.argv[1:]], check=True)

	###
	# here you can add some custom behaviors
	###

	if input("commit the new version? [Y/n] ") in 'yY':
		sub.run(["git", "add", PACKAGE_SOLUTION], check=True)
		sub.run(["git", "commit", "-m", f"\"version {v}\""], check=True)

except KeyboardInterrupt:
	print("\nUnderstandable, have a great day")
except Exception as e:
	print("\nSomething goes wrong:", e)
	sys.exit(1)

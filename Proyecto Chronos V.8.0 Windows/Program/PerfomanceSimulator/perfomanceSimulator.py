from datetime import datetime

class ExecutionTime:
	def getTime(self):
		return datetime.now()

	def diff(self, i, f):
		return f - i

class TestAlgorithm:
	def test(self,algorithFunction = None, path = "", destiny = ""):
		i = ExecutionTime().getTime()
		algorithFunction(path, destiny)
		f = ExecutionTime().getTime()

		date = i.strftime("%d-%m-%Y %H:%M:%S")
		nameFile = path.split("/").pop()

		diff = ExecutionTime().diff(i,f)

		seconds = float(diff.seconds)
		seconds += float(diff.days * 24 * 60 * 60)
		seconds += float(diff.microseconds) / 1000000

		# @Tupla: nombre archivo, fecha y hora de ejecucion, tiempo que tardo en encriptar  
		return (nameFile.encode("utf-8"), date, seconds )


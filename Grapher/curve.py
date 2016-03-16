class curve:
	def __init__(self,color,name,curveid,gid,pid,docid):
		# list of points in the curve
		self.x = []
		self.y = []
		self.curveid=curveid
		self.graph=gid
		self.page=pid
		self.doc=docid
		self.color=color
		self.name=name

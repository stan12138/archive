import threading
import queue

__all__ = ["Work","ThreadPool"]

class WorkDone(Exception) :
	pass


class WorkThread(threading.Thread) :

	def __init__(self,work_queue,result_queue,timeout) :
		threading.Thread.__init__(self)

		#self.setDaemon(True) 已经被废弃了
		self.daemon = True
		self.work_queue = work_queue
		self.result_queue = result_queue

		self.timeout = timeout

		self.dismiss = threading.Event()

		self.start()

	def run(self) :

		while True:
			if self.dismiss.is_set() :
				break

			try :
				work = self.work_queue.get(True,self.timeout)

			except queue.Empty :
				continue
			else :
				if self.dismiss.is_set() :
					self.work_queue.put(work)
					break
				try :
					result = work.work_func(*work.args)   
					#print('%s is done'%work.work_ID)
					self.result_queue.put((work,result))
				except :
					pass


	def set_dismiss(self) :
		self.dismiss.set()


class Work() :
	def __init__(self,target=None,args=[],work_ID=None) :
		if work_ID == None :
			self.work_ID = id(self)
		else :
			try :
				self.work_ID = hash(work_ID)
			except :
				print("workID must be hashable,this id can't use,we will set as default")
				self.work_ID = id(self)

		self.work_func = target
		self.args = args

	def __str__(self) :
		return 'work thread id=%s args=%s'%(self.work_ID,self.args)








class ThreadPool(object):

	def __init__(self,worker_num,work_size=0,result_size=0,timeout=5) :

		self.work_queue = queue.Queue(work_size)
		self.result_queue = queue.Queue(result_size)
		self.timeout = timeout

		self.workers = []
		self.dismiss_workers = []
		self.work = {}

		self.creat_workers(worker_num)


	def creat_workers(self,num) :
		for i in range(num) :
			self.workers.append(WorkThread(self.work_queue, self.result_queue, self.timeout))
		
		
	def dismiss_thread(self,num,do_join=False) :
		dismiss_list = []
		num = min(num,len(self.workers))
		for i in range(num) :
			worker = self.workers.pop()
			worker.set_dismiss()
			dismiss_list.append(worker)

		print('stop %s work thread and leave %s thread.....'%(num,len(self.workers)))

		if do_join :
			for i in dismiss_list :
				i.join()
			print('join all dismiss thread already...')

		else :
			self.dismiss_workers.extend(dismiss_list)

	def join_dismiss_thread(self) :

		for i in self.dismiss_workers :
			i.join()
		

		print('join %s dismiss workers already,now there are still %s workers...'%(len(self.dismiss_workers),len(self.workers)))

		self.dismiss_workers = []


	def put_work(self,work,block=True,timeout=None) :

		if isinstance(work,Work) :
			self.work_queue.put(work,block,timeout)
			self.work[work.work_ID] = work

		else :
			print('work must be Work class,put failure.....')

		#print('add one work')

	def get_all_result(self,block=False) :
		while True:
			if not self.work :
				raise WorkDone
			try :
				work, result = self.result_queue.get(block=block) 
				#print('got one result')
				del self.work[work.work_ID]
			except :
				break

	def stop(self) :
		self.dismiss_thread(self.worker_num(),True)
		self.join_dismiss_thread()

	def worker_num(self) :
		return len(self.workers)

	def wait(self) :
		while True:
			try:
				self.get_all_result(True)
			except WorkDone:
				print('work done!!!!')
				break



if __name__ == "__main__" :

	import datetime

	def work(name,data) :
		with open(name,'w') as fi :
			fi.write(data)

		print('write %s already'%name)

	main = ThreadPool(5)

	for i in range(10) :
		main.put_work(Work(target=work,args=(str(i)+'.txt','hello')))

	main.wait()
	main.stop()









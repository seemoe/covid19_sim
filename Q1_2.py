# 依赖
import threading
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# 多线程重写

class Thread(threading.Thread):
    def __init__(self, func, args=()):
        super(Thread,self).__init__()
        self.func= func
        self.args= args
 
    def run(self):
        self.result= self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result
        except Exception:
            return Exception

# 函数

# get_ltr= lambda o : chr(o+97) # 0 is 'a'

def numful(n):
	i=1
	b=1
	while i*b<n:
		if i<b:
			i+=1
		else:
			b+=1
	return i,b

# 使用点位检测(x,y)
def check( people , x ):
	count=0
	while len(people) > 0:
		if len(people)>(x**2):
			checknow=[people[x*i:(x+1)*i] for i in np.arange(x)]
			del people[0:x**2]
		else:
			a,b=numful(len(people))
			checknow=[people[a*i:((a+1)*i if (a+1*i) <= len(people) else 0)] for i in np.arange(b)]
			del people[0:len(people)]
		xleng=len(checknow[0])
		yleng=len(checknow)
		tx=[]
		ty=[]
		for i in np.arange(yleng):
			count+=1
			if sum(checknow[i]) > 0:
				ty.append(i)
		for i in np.arange(xleng):
			count+=1
			if sum([checknow[j][i] for j in np.arange(yleng)]) >0:
				tx.append(i)
		if len(tx)>=2 and len(ty)>=2:
			count+=(len(tx)*len(ty))
	return count

# sorted_people = lambda n : [0 for i in range(n-1)]+[random.randint(0,1) for i in range(int(n*0.05))]
generate= lambda y,o : [0 for i in np.arange(int(y*o+0.5))]+[(1 if np.random.randint(0,101) <=80 else 0) for j in np.arange(int(y*o))]


def rand( lst ):
	leng=len(lst)
	for i in np.arange(leng):
		o=np.random.randint(0,leng)
		lst[i],lst[o]=lst[o],lst[i]
	return lst

def start(x,y):
	# x 一组几人 y 总共几人
	count=0
	for i in np.arange(3):
		ori=generate(y,0.05)
		people=rand(ori)
		count+=check(people,x)
	return x,y,count/3

#########################

begin=1000
end=5000

zlist=np.zeros([26,end-begin+1],np.int32)
xlist=np.arange(5,31)
ylist=np.arange(begin,end+1)

def get(x,y):
	return zlist[x-5][y-begin]

def main():
	# x 一组几人(-5) y 总共几人(-1000) content 检测次数
	global xlist
	global ylist
	global zlist
	for y in np.arange(begin,end+1):
		print(y)
		th_lst=[]
		for x in np.arange(5,31):
			th_lst.append(Thread(start,(x,y)))
			th_lst[-1].start()
		for i in np.arange(len(th_lst)):
			while th_lst[i].is_alive():
				time.sleep(0.1)
			th_lst[i].join()
			x,y,z=th_lst[i].get_result()
			zlist[x-5][y-begin]=z
	x,y = np.meshgrid(xlist, ylist)
	z=np.array( list([get(i,j) for i in xlist] for j in ylist) )
	print(z)
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.plot_surface(x,y,z,rstride = 1, cstride = 1,cmap='rainbow')
	plt.rcParams['font.sans-serif']=['Microsoft YaHei']
	ax.set_xlabel('每组人数')
	ax.set_ylabel('总人数')
	ax.set_zlabel('检测次数')
	ax.view_init(elev=12, azim=-40)
	plt.show()


# 运行

if __name__=="__main__":
	main()
	print("====================\nOperation completed!")
# -*- coding: utf-8 -*-
# coding:utf-8 
"""
@author: zhangyangyang
		826235954@qq.com
"""
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys
import re 

class huoche(object):
	"""docstring for huoche"""
	# 浏览器以及浏览器驱动
	driver_name='chrome'
	executable_path='E:/workspace/chromedriver.exe'
	#用户名，密码
	# username = u"xxx@qq.com"
	username = u""
	passwd = u""
	# cookies值得自己去找, 下面两个分别是北京, 商丘
	# starts = u"%u5317%u4EAC%u897F%2CBXP"
	starts = u"%u5317%u4EAC%2CBJP"
	# ends = u"%u4FAF%u9A6C%u897F%2CHPV"
	# ends = u"%u97E9%u57CE%2CHCY"
	ends = u"%u5546%u4E18%2CSQF"	
	# 时间格式2018-01-19
	dtime = u"2018-02-13"
	# dtime = u"2018-02-22"
	# 车次，选择第几趟，数组里不能为0；单赋给order=0则从上至下依次点击查询全部列车
	order = [11,12,13,5,6,7]
	###乘客名
	users = [u"张三"]
	##席位
	# xb = u"二等座"
	# pz=u"成人票"
	# pz=u"学生票"

	"""网址"""
	ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
	login_url = "https://kyfw.12306.cn/otn/login/init"
	initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
	buy="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	login_url='https://kyfw.12306.cn/otn/login/init'
	
	def __init__(self):
		# 浏览器以及浏览器驱动
		self.driver_name='chrome'
		# 修改1
		self.executable_path='E:/workspace/chromedriver.exe'

	def login(self):
		self.driver.visit(self.login_url)
		self.driver.fill("loginUserDTO.user_name", self.username)
		# sleep(1)
		self.driver.fill("userDTO.password", self.passwd)
		print (u"等待验证码，自行输入...")
		while True:
			if self.driver.url != self.initmy_url:
				sleep(1)
			else:
				break

	def start(self):
		self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
		self.driver.driver.set_window_size(1400, 1000)
		self.login()
		# sleep(1)
		self.driver.visit(self.ticket_url)
		try:
			print (u"购票页面开始...")
			# sleep(1)
			# 加载查询信息
			self.driver.cookies.add({"_jc_save_fromStation": self.starts})
			self.driver.cookies.add({"_jc_save_toStation": self.ends})
			self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
			self.driver.reload()
			self.refresh()
		except Exception as e:
			print (e)

	def refresh(self):
			count=0
			if self.order!=0:
				while self.driver.url==self.ticket_url:
					self.driver.find_by_text(u"查询").click()
					count += 1
					print('\n')
					print (u"循环点击查询, 第 %s 次" % count)
					sleep(0.2)
						#修改2 find_by_text(u"预订")[]   这是个数组，所以要-1
						# self.driver.find_by_text(u"预订")[self.order - 1].click()
					for i in range(len(self.order)):
						try:
							print('正在查询Train:' + str(self.order[i]))
							self.driver.find_by_text(u"预订")[self.order[i] - 1].click()
							sleep(0.2)
							if self.driver.url==self.buy:
								self.reserve()	
						except Exception as e:
							print (e)
							print (u"还没开始预订")
							self.driver.visit(self.ticket_url)
							self.refresh()
							continue
			else:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text(u"查询").click()
					count += 1
					print('\n')
					print (u"循环点击查询, 第 %s 次" % count)
					sleep(2)
					for i in self.driver.find_by_text(u"预订"):
						try:
							print('正在查询Train:' + str(i+1))
							i.click()
							sleep(0.2)
							if self.driver.url==self.buy:
								self.reserve()
						except Exception as e:
							print (e)
							print (u"还没开始预订 %s" %count)
							continue


	def reserve(self):
			print (u"开始预订")
			# sleep(3)
			# self.driver.reload()
			print (u'开始选择用户')
			for user in self.users:
				self.driver.find_by_text(user).last.click()
				# 学生票会有下面操作
				sleep(0.1)
				#
				self.driver.evaluate_script('document.getElementById("dialog_xsertcj_ok").style="display: inline-block; visibility: visible;"')
				# 上面代码让跳出的提示框的元素可见，可被获取到
				#
				self.driver.find_by_id('dialog_xsertcj_ok').click() # 确认是学生票
				# self.driver.find_by_text(u"取消").click() # 取消是成人票
				# self.driver.find_by_text(self.xb).click()  #二等座

				# self.driver.find_by_text(u"提交订单").click()
				# self.driver.find_by_text(u"确认").click()

			print (u"提交订单...")
			sleep(0.1)
			# self.driver.select("confirmTicketType","1")# 用这个来选择下拉框，这里是成人票选择
			self.driver.find_by_xpath('//select[@id="seatType_1"]/option[@value="1"]')._element.click()# select没有name这么使用，这里是硬座选择
			sleep(0.1)
			self.driver.find_by_id('submitOrder_id').click() #提交订单
			# print u"开始选座..."
			# self.driver.find_by_id('1D').last.click()
			# self.driver.find_by_id('1F').last.click()
			print (u"确认选座...")
			#
			self.driver.evaluate_script('document.getElementById("sy_ticket_num_id").style="display: inline-block; visibility: visible;"')
			#
			# ticketnum = self.driver.find_by_id('sy_ticket_num_id').text #找到显示余票的文字
			# print("11+"+ticketnum)
			# a = re.findall(r'\d+', ticketnum)								#正则，找出数字，得到list
			# print ("余票..." + int(a[0]))
			ticketnum = self.driver.find_by_xpath('//p[@id="sy_ticket_num_id"]/strong').text
			print("还有余票："+ticketnum+"张")
			if int(ticketnum)>0:
				print (u"请稍等...")
				# sleep(3)  #这里能不能修改为一直点确认直到成功
				self.driver.evaluate_script('document.getElementById("qr_submit_id").style="display: inline-block; visibility: visible;"')
				while True:
					try:
						print('正在点确定')
						self.driver.find_by_id('qr_submit_id').click()
						# self.driver.find_by_text(u"确定").click()
					except Exception as e:
						raise e
			else:
				self.driver.evaluate_script('document.getElementById("back_edit_id").style="display: inline-block; visibility: visible;"')
				self.driver.find_by_id('back_edit_id').click()
				self.driver.find_by_text(u"上一步").click()
				self.refresh()
			
			
				
					

if __name__ == '__main__':
	huoche=huoche()
	huoche.start()
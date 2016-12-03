# -*- coding: utf-8 -*-

tab = ['#task1','#task2','#task3','#task4','#task5','#task6','#task7','#task8','#task9','#task10','#task11']

s = {}
s['#task1'] = "hid3_in_the_treeS"
s['#task2'] = "yes_you_c4n"
s['#task3'] = "hidden_1_7896b61ed718bc44c0c73de186d6f8c655f9f15e"
s['#task4'] = "C_to_V_to_E_2016_eight_six_two_one"
s['#task5'] = "Lucky_p4dd1ng_0r_y0u_r34d_my_m1nd"
s['#task6'] = "N0_alias_anym0r3"
s['#task7'] = "shellc0de_sixteen_bytes"
s['#task8'] = "roadtothecastle"
s['#task9'] = ""
s['#task10'] = "http_chunked_is_tricky_sometimes"
s['#task11'] = ""

def getPad(data):
	return "SVATTT{" + data + "}"

url = "https://scoreboard.svattt.org/task"
user = "n/a"
pwd = "justforSVATTTonly"


from splinter import Browser
from time import sleep

with Browser() as b:
	b.visit(url)
	b.find_by_id('name').fill(user)
	b.find_by_id('password').fill(pwd)
	b.find_by_value("Đăng nhập").first.click()
	sleep(1)
	b.visit(url)
	while True:
		for i in tab:
			try :
				if (s[i] == ""):
					continue
				payload = getPad(s[i])
				b.find_by_id(i).first.click()
				board = b.find_by_id(i[1:])
				sleep(1)
				board.find_by_id("flag").fill(payload)
				sleep(1)
				board.find_by_tag('button').first.click()
				sleep(2)
			except:
				continue
		sleep(10)
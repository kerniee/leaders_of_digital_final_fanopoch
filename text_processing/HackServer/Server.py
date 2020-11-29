import json
from socketserver import *

import language_processor as lp
import string

keys = [["срочно", "не срочно", "позже", "неважно", "немедленно", "быстро", "критически", "опасно", "важно",
         "не важно", "серьёзно", "опасность", "угроза", "травма", "ужас", "скорее", "экстренно", "врач",
         "больница", "боль"],
        ["до xx:xx", "xx:xx", "после xx:xx", "в полдень", "днем", "ночью", "после обеда", "во время обеда",
         "после работы", "после смены", "перед сменой", "после смены", "во время смены", "завтра",
         "послезавтра", "вчера", "позавчера", "сегодня"],
        ["техническое задание", "технологическое задание", "организационное задание", "техзадание", "ТЗ",
         "починить", "сообщить", "сообщение", "сообщаю", "заявляю", "уведомить", "отработать", "пожаловаться",
         "жалоба", "жалуюсь", "уведомляю", "уведомление", "предложение", "объяснение", "восстановить", "печь",
         "механизм", "конструкция", "стержень", "трос", "станок", "пресс", "заготовки", "плавильня", "ремонт",
         "пресс", "экскаватор"],
        ["мастер", "мастеру", "технолог", "инженер", "инженеру", "работник", "сотрудник", "начальник участка",
         "руководитель", "начальник", "все"],
        ["цех", "корпус", "завод", "участок", "площадка"]]

# keys = ["немедленно", "быстро", "важно", "срочно", "31", "3381","317", "15:34", "участок", "цех", "механизм", "станок","печь", "мастер", "участок", "работник", "технолог", "инженер по ремонту", "начальник участка", "корпус", "руководитель младшего звена", "руководитель среднего звена"]

# lp.calculate_keys(keys)
lp.load_keys(keys, "key_vectors.json")

host = 'localhost'
port = 49490
addr = (host, port)
class service(StreamRequestHandler):
    def handle(self):
        while True:
            in_string = self.rfile.readline()
            in_string = in_string.decode()
            if in_string:
                res = lp.keys_grouped_check(in_string)
                self.request.sendall((json.dumps(res) + "\n").encode("utf-8"))
                print("Приоритет: " + res[0])
                print("Время: " + res[1])
                print("Тип: " + res[2])
                print("Получатель: " + res[3])
                print("Место: " + res[4])
            else:
                break

class ThreadedTCPServer(TCPServer):
    pass

ThreadedTCPServer.allow_reuse_address = True
server = ThreadedTCPServer(addr, service)
print("Server is listening!")
server.serve_forever()
print("Stopping the server...")
server.server_close()
server.shutdown()
server.socket.close()
print("Server is stopped")
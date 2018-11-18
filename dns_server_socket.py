from socket import *
import time
import binascii
cache = {}
def modify_ttl(time_pass,information_list):
    start = 4
    questions = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    answer_rrs = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    authority_rrs = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    additional_rrs = information_list[start] * 16 * 16 + information_list[start + 1]

    # 解析question块
    start = 12
    request_name = ''
    while information_list[start] != 0:
        length = information_list[start]
        for i in range(length):
            start = start + 1
        start = start + 1
    start = start + 5
    # 解析answer块,找出最小的ttl
    total_answer = answer_rrs + authority_rrs
    for j in range(total_answer):
        if information_list[start] != 192:
            while information_list[start] != 0:
                length = information_list[start]
                for i in range(length):
                    start = start + 1
                start = start + 1
            start = start + 5
        else:
            start = start + 6
        temp_ttl = information_list[start] * 16777216 + information_list[start + 1] * 65536 + information_list[
            start + 2] * 256 + information_list[start + 3]
        new_ttl = int(temp_ttl - time_pass) + 1
        information_list[start:start+4] = list(new_ttl.to_bytes(length=4, byteorder='big'))
        start = start + 4
        data_length = information_list[start] * 256 + information_list[start + 1]
        start = start + 2 + data_length
    information = b''
    for i in information_list:
        tempi = i.to_bytes(length=1, byteorder='big')
        # print(tempi)
        information+=tempi
    return information

def udp_s():
    server_port = 8081
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print('The server is ready to recieve')
    while True:
        message, client_address = server_socket.recvfrom(2048)
        message_list = list(message)
        print(message_list)
        start = 0
        id = (message_list[start], message_list[start + 1])
        start = 12
        name = ''
        while message_list[start] != 0:
            length=message_list[start]
            for i in range(length):
                start = start + 1
                name = name + message_list[start].to_bytes(length=1, byteorder='big').decode()
            name = name + '.'
            start = start + 1
        name = name.strip('.')
        rr_type = message_list[start + 1]*16*16 + message_list[start+2]
        rr_class =  message_list[start + 3]*16*16 + message_list[start+4]
        print("name in query is", name)
        print("type in query is", rr_type)
        print("class in query is", rr_class)
        if cache.keys().__contains__((name, rr_type)):
            rec_time = cache[(name, rr_type)][1]
            ttl = cache[(name, rr_type)][0]
            information = cache[(name, rr_type)][2]
            now = time.time()
            time_pass = now - rec_time
            if time_pass < ttl:
                new_rec_time = now
                new_ttl = ttl - time_pass
                information_list = list(information)
                information_list[0] = id[0]
                information_list[1] = id[1]
                if new_ttl < 0: print("############################")
                information = modify_ttl(time_pass, information_list)
                cache[(name, rr_type)] = (new_ttl, new_rec_time, information)
            else:
                information = udp_c(message)
        else:
            information = udp_c(message)
        server_socket.sendto(information, client_address)

def udp_c(message):
    server_name = 'ns2.sustc.edu.cn'
    server_port = 53
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.sendto(message,(server_name,server_port))
    information, server_address = client_socket.recvfrom(2048)
    information_list = list(information)
    print("information list is", information_list)
    #解析各个板块数量

    start = 4
    questions = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    answer_rrs = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    authority_rrs = information_list[start] * 16 * 16 + information_list[start + 1]
    start = start + 2
    additional_rrs = information_list[start] * 16 * 16 + information_list[start + 1]
    print("questions:%d\r\nanswer RRs:%d\r\nauthority RRs:%d\r\nadditional RRs:%d\r\n"
          % (questions,answer_rrs,authority_rrs,additional_rrs))

    #解析question块
    start = 12
    request_name = ''
    while information_list[start] != 0:
        length = information_list[start]
        for i in range(length):
            start = start + 1
            request_name = request_name + information_list[start].to_bytes(length=1, byteorder='big').decode()
        request_name = request_name + '.'
        start = start + 1
    request_name = request_name.strip('.')

    rr_request_type = information_list[start + 1] * 16 * 16 + information_list[start + 2]
    rr_request_class = information_list[start + 3] * 16 * 16 + information_list[start + 4]
    start = start + 5
    print("name in respond is", request_name)
    print("type in respond is", rr_request_type)
    print("class in respond is", rr_request_class)
    print('infromation is',information_list)

    # 解析answer块,找出最小的ttl
    ttl = float('inf')
    total_answer = answer_rrs+authority_rrs

    for j in range(total_answer):
        # print('information_list[start]',information_list[start])
        if information_list[start] != 192:
            while information_list[start] != 0:
                length = information_list[start]
                for i in range(length):
                    start = start + 1
                start = start + 1
            start = start + 5
        else:
            start = start + 6
        temp_ttl = information_list[start]*16777216 + information_list[start+1]*65536 + information_list[start+2]*256 + information_list[start+3]
        # print("tempttl:", temp_ttl)
        start = start + 4
        ttl = min(ttl, temp_ttl)
        # print("ttl", ttl)
        data_length = information_list[start]*256 + information_list[start+1]
        start = start + 2 + data_length

    rec_time = time.time()
    cache[(request_name, rr_request_type)] = (ttl, rec_time, information)


    client_socket.close()
    return information

if __name__ == "__main__":
    try:
        while(True):
            udp_s()
    except KeyboardInterrupt:
        pass
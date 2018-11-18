import dns.resolver
a = dns.resolver.query("www.163.com",'a')
print("This is based on UDP stream")
for i in a.response.answer:
    for j in i.items:
            print(j)

a = dns.resolver.query("www.163.com",'a', tcp=True)
print("\r\nThis is based on TCP stream")
for i in a.response.answer:
    for j in i.items:
            print(j)

# www.163.com.lxdns.com.
# 14.215.100.245
# 121.11.81.164
# 183.58.18.95
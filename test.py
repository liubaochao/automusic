import urllib

url_mess = 'http://www.xiami.com/song/playlist/id/%s/type/0/cat/json'

d = {'songId':1}

mess = "8h28n55%F%9mtD3EE%a97tF.e%%5154ph17--588%t%xt22E7E43_52%%Efc5p2i%FF%768%k%%553e9E%Fa28551613e55EEa6893mmF95E4__FyEE-51336A1i776%53la%9%%7fe5b%2.115288.u3955b391e"
rows = int(mess[0])
print "row: %d" % rows
url = mess[1:]
print "url: %s" % url
len_url = len(url)
print "url len: %d" % len_url
cols = len_url / rows
print "cols: %d" % cols
re_col = len_url % rows
print "re_col: %d" % re_col


l = []
for row in xrange(rows):
    if row < re_col:
        ln = cols + 1
    else:
        ln = cols
    print ("ln: %d" % ln)
    l.append(url[:ln])
    print ("l: %s" % l)
    url = url[ln:]
    print ("url: %s" % url)

durl = ''
for i in xrange(len_url):
    durl += l[i % rows][i / rows]
# print ("------------------")
# print (urllib.unquote(durl).replace('^', '0'))
# print ("------------------")



L1 = ['Hello', 'World', 18, 'Apple', None]

print ([s.lower() for s in L1 if (isinstance(s, str))])
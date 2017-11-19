import printerclock as pc

h,m,d = pc.gettime()
print pc.getposition(h, m, d)

h = 5
m = 45
d = 0
print pc.getposition(h, m, d)

h = 2
m = 00
d= 0
print pc.getposition(h, m, d)

h = 19
m = 10
d = 0
print pc.getposition(h, m, d)
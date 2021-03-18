from app.utils.frame.site import Site

frame_location = Site()
try:
    with open("site_0.txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
except IOError:
    print('not  found file or read error')

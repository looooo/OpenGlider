import time
from openglider import jsonify
from openglider.glider import ParametricGlider

#gl = Glider2D.import_ods('acro.ods')
num = 3
#with open('acro.json', 'w') as outfile:
#    jsonify.dump(gl, outfile)

start = time.time()

for i in range(num):
    with open('acro.json') as infile:
        glider_2d = jsonify.load(infile)["data"]
    glider_3d = glider_2d.get_glider_3d()
    glider_3d.return_polygon_indices()

stop = time.time()
print((stop-start)/num)
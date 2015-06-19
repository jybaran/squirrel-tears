from display import *
from matrix import *
from gmath import calculate_dot
from math import cos, sin, pi
import random

Z_BUFF = [[-9223372036854775807 for x in range(500)] for x in range(500)]
MAX_STEPS = 100
     

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )
    
def draw_polygons( points, screen, color, ambK, specK, diffK, ambI, light_pos):
    #light_pos = [x,y,z] position of light source
    #ambK = [a,b,c] values are strength of ambient RBG
    #ambI = [a,b,c] values are RBG values for ambient light
    #specK = [a,b,c] values are strength of specular reflcetion
    #diffK = [a,b,c] values are strength of diffuse relection
    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0

    while p < len( points ) - 2:
        #backface culling
        if calculate_dot( points, p ) >= 0:
            color[0] = random.randint(0,255)
            color[1] = random.randint(0,255)
            color[2] = random.randint(0,255)

            ambI_R = ambI[0]*ambK[0]
            ambI_G = ambI[1]*ambK[1]
            ambI_B = ambI[2]*ambK[2]

            difI_R = calculate_dot_light(points,p,light_pos)*ambI_R*diffK[0]
            difI_G = calculate_dot_light(points,p,light_pos)*ambI_G*diffK[1]
            difI_B = calculate_dot_light(points,p,light_pos)*ambI_B*diffK[2]
            
            specI_R = calculate_specular(ambI_R,specK[0],points,p,light_pos)
            specI_G = calculate_specular(ambI_G,specK[1],points,p,light_pos)
            specI_B = calculate_specular(ambI_B,specK[2],points,p,light_pos)

            
            z_plane = calculate_plane( screen,
                                       points[p][0], points[p][1], points[p][2],
                                       points[p+1][0], points[p+1][1], points[p+1][2],
                                       points[p+2][0], points[p+2][1], points[p+2][2])
            draw_line( screen, 
                       points[p][0], points[p][1], points[p][2],
                       points[p+1][0], points[p+1][1], points[p+1][2],
                       z_plane,
                       color )
            draw_line( screen, 
                       points[p+1][0], points[p+1][1], points[p+1][2],
                       points[p+2][0], points[p+2][1], points[p+2][2],
                       z_plane,
                       color )
            draw_line( screen, 
                       points[p+2][0], points[p+2][1], points[p+2][2],
                       points[p][0], points[p][1], points[p][2],
                       z_plane,
                       color )
            #scanline conversion
            scanline_convert( screen, color, z_plane,
                              points,
                              points[p][0], points[p][1],
                              points[p+1][0], points[p+2][1],
                              points[p+2][0], points[p+2][1] )
        p+= 3

def calculate_specular( ambI, diffK, points, p, light_pos):
    return 0

def calculate_dot_light(points, p, light_pos):
    return 0
    
def calculate_plane( screen, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    #given 3 points (aka triangle vertices), determine the unique plane equation
    #rx + sy + tz = k
    #print "points: (",x0,",",y0,",",z0,"),\n\t(",x1,",",y1,",",z1,"), \n\t(",x2,",",y2,",",z2,")"
    v1 = [x0-x1, y0-y1, z0-z1]
    v2 = [x0-x2, y0-y2, z0-z2]
    #print "v1: ",v1[0],",",v1[1],",",v1[2]
    #print "v2: ",v2[0],",",v2[1],",",v2[2]
    n = cross_product(v1, v2)
    r = n[0]
    s = n[1]
    t = n[2]
    k = r*x0 + s*y0 + t*z0
    plane = [r,s,t,k]
    #print "plane: ",r,",",s,",",t,"=",k
    return plane

def cross_product(v1, v2):
    n = [0,0,0]
    n[0] = v1[1]*v2[2] - v1[2]*v2[1]
    n[1] = v1[2]*v2[0] - v1[0]*v2[2]
    n[2] = v1[0]*v2[1] - v1[1]*v2[0]
    return n

def dot_product(v1, v2):
    dot = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    mag = ( (v1[0] * v1[0]) + (v1[1] * v1[1]) + (v1[2] * v1[2]) ) ** 0.5
    mag*=( (v2[0] * v2[0]) + (v2[1] * v2[1]) + (v2[2] * v2[2]) ) ** 0.5
    return dot/mag

def scanline_convert( screen, color, zplane, points, x0, y0, x1, y1, x2, y2 ):
    s = sorted( [ (y0, x0), (y1, x1), (y2, x2) ] )
    
    Ty = round(s[2][0])
    Tx = round(s[2][1])
    
    By = round(s[0][0])
    Bx = round(s[0][1])
    
    My = round(s[1][0])
    Mx = round(s[1][1])
    
    y = By
    xa = Bx #one of x-coords
    xb = Bx
    
    pastM = False
    while y < Ty: #not yet at top of triangle
        d0 = ((Tx - Bx)*1.0)/(Ty-By)
        if not pastM and y >= My:
            pastM = True
            xb = Mx
            y = My
        if pastM:
            if (My - .5) <= Ty <= (My + .5):
                d1 = 0
            else:
                d1 = ((Tx - Mx)*1.0)/(Ty-My)
        else:
            if (By - .5) <= My <= (By + .5):
                d1 = 0
            else:
                d1 = ((Mx - Bx)*1.0)/(My-By)

        xa += d0
        xb += d1
        y += 1
        draw_line( screen, 
                   int(xa), int(y), 0, 
                   int(xb), int(y), 0,
                   zplane,
                   color )


def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth
    
    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, 
                   matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2],
                   0, #zplane = 0, image is flat, z vals >0 will override, z vals <0 will not
                   color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, z0, x1, y1, z1, zplane, color ):
    #zbuff somewhere in here
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    if dx + dy < 0: #if points not in order
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0: #straight line vertical
        y = y0
        while y <= y1:
            plot(screen, color,  x0, y, Z_BUFF, zplane)
            y = y + 1
    elif dy == 0: #straight line horizontal
        x = x0
        while x <= x1:
            plot(screen, color, x, y0, Z_BUFF, zplane)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y, Z_BUFF, zplane)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y, Z_BUFF, zplane)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y, Z_BUFF, zplane)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y, Z_BUFF, zplane)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

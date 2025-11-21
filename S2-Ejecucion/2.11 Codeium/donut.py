import math
import time
import sys

def render_donut():

    A = 0  
    B = 0  
    
    screen_width = 80
    screen_height = 40
    
    chars = ".,-~:;=!*#$@"
    
    print("\x1b[2J")

    try:
        while True:

            output = [' '] * (screen_width * screen_height)

            zbuffer = [0] * (screen_width * screen_height)
            
            cosA = math.cos(A)
            sinA = math.sin(A)
            cosB = math.cos(B)
            sinB = math.sin(B)

            theta = 0
            while theta < 2 * math.pi:
                costheta = math.cos(theta)
                sintheta = math.sin(theta)

                phi = 0
                while phi < 2 * math.pi:
                    cosphi = math.cos(phi)
                    sinphi = math.sin(phi)

                    circle_x = 2 + costheta 
                    circle_y = sintheta

                    x = circle_x * (cosB * cosphi + sinA * sinB * sinphi) - circle_y * cosA * sinB
                    y = circle_x * (sinB * cosphi - sinA * cosB * sinphi) + circle_y * cosA * cosB
                    z = 1 / (circle_x * cosA * sinphi + circle_y * sinA + 5) 

                    xp = int(screen_width / 2 + 30 * 1 / (z * 5) * x) 
                    yp = int(screen_height / 2 - 15 * 1 / (z * 5) * y) 

                    L = cosphi * costheta * sinB - cosA * costheta * sinphi - \
                        sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

                    if L > 0:

                        idx = xp + yp * screen_width
                        
                        if 0 <= idx < len(zbuffer):

                            if z > zbuffer[idx]:
                                zbuffer[idx] = z
                                luminance_index = int(L * 8)
                                output[idx] = chars[max(0, min(11, luminance_index))]

                    phi += 0.07 
                theta += 0.02 

            sys.stdout.write("\x1b[H")

            for i in range(len(output)):
                sys.stdout.write(output[i])
                if (i + 1) % screen_width == 0:
                    sys.stdout.write("\n")

            A += 0.04
            B += 0.02

    except KeyboardInterrupt:
        print("\nPrograma detenido.")

if __name__ == "__main__":
    render_donut()
import math
import time
import sys

def render_donut():
    """
    This function renders a rotating 3D donut using ASCII characters

    The function uses the parametric equation of a torus to generate 3D points
    and then projects them onto a 2D screen using perspective projection.
    The resulting image is rendered on the console using ASCII characters.
    """

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

            # Iterate over the parametric equation of a torus
            theta = 0
            while theta < 2 * math.pi:
                costheta = math.cos(theta)
                sintheta = math.sin(theta)

                phi = 0
                while phi < 2 * math.pi:
                    cosphi = math.cos(phi)
                    sinphi = math.sin(phi)

                    # Calculate the 3D point on the torus
                    circle_x = 2 + costheta 
                    circle_y = sintheta

                    # Calculate the x and y coordinates of the projected 2D point
                    x = circle_x * (cosB * cosphi + sinA * sinB * sinphi) - circle_y * cosA * sinB
                    y = circle_x * (sinB * cosphi - sinA * cosB * sinphi) + circle_y * cosA * cosB
                    z = 1 / (circle_x * cosA * sinphi + circle_y * sinA + 5) 

                    # Calculate the index of the projected point in the output array
                    xp = int(screen_width / 2 + 30 * 1 / (z * 5) * x) 
                    yp = int(screen_height / 2 - 15 * 1 / (z * 5) * y) 

                    # Calculate the luminance of the projected point
                    L = cosphi * costheta * sinB - cosA * costheta * sinphi - \
                        sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

                    # Check if the projected point is visible
                    if L > 0:

                        idx = xp + yp * screen_width
                        
                        # Check if the projected point is within the bounds of the output array
                        if 0 <= idx < len(zbuffer):

                            # Check if the projected point is closer than the previous point
                            if z > zbuffer[idx]:
                                zbuffer[idx] = z
                                # Calculate the index of the ASCII character to use
                                luminance_index = int(L * 8)
                                output[idx] = chars[max(0, min(11, luminance_index))]

                    phi += 0.07 
                theta += 0.02 

            # Clear the console
            sys.stdout.write("\x1b[H")

            # Print the output array
            for i in range(len(output)):
                sys.stdout.write(output[i])
                if (i + 1) % screen_width == 0:
                    sys.stdout.write("\n")

            # Increment the rotation angles
            A += 0.04
            B += 0.02

    except KeyboardInterrupt:
        print("\nPrograma detenido.")

if __name__ == "__main__":
    render_donut()
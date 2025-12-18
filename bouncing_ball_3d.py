#!/usr/bin/env python3
"""
3D Bouncing Red Ball using pyglet and OpenGL
"""
import pyglet
from pyglet.gl import *
import math


def setup_perspective(fov, aspect, near, far):
    """Set up perspective projection matrix manually"""
    f = 1.0 / math.tan(math.radians(fov) / 2.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Create perspective projection matrix
    matrix = (GLfloat * 16)(
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (far + near) / (near - far), -1,
        0, 0, (2 * far * near) / (near - far), 0
    )
    glLoadMatrixf(matrix)


def setup_lookat(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z):
    """Set up view matrix manually (lookat)"""
    # Calculate forward vector
    fx = center_x - eye_x
    fy = center_y - eye_y
    fz = center_z - eye_z
    
    # Normalize forward
    f_len = math.sqrt(fx*fx + fy*fy + fz*fz)
    fx, fy, fz = fx/f_len, fy/f_len, fz/f_len
    
    # Calculate right vector (cross product of forward and up)
    rx = fy * up_z - fz * up_y
    ry = fz * up_x - fx * up_z
    rz = fx * up_y - fy * up_x
    
    # Normalize right
    r_len = math.sqrt(rx*rx + ry*ry + rz*rz)
    rx, ry, rz = rx/r_len, ry/r_len, rz/r_len
    
    # Calculate up vector (cross product of right and forward)
    ux = ry * fz - rz * fy
    uy = rz * fx - rx * fz
    uz = rx * fy - ry * fx
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Create view matrix
    matrix = (GLfloat * 16)(
        rx, ux, -fx, 0,
        ry, uy, -fy, 0,
        rz, uz, -fz, 0,
        -(rx*eye_x + ry*eye_y + rz*eye_z),
        -(ux*eye_x + uy*eye_y + uz*eye_z),
        (fx*eye_x + fy*eye_y + fz*eye_z),
        1
    )
    glLoadMatrixf(matrix)


class BouncingBall3D:
    def __init__(self):
        # Ball properties
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0
        
        # Velocity (units per second)
        self.vx = 1.2
        self.vy = 1.8
        self.vz = 0.6
        
        # Ball radius
        self.radius = 0.5
        
        # Boundaries
        self.bounds = 2.5
        
        # Gravity (units per second squared)
        self.gravity = -0.06
        
        # Damping for realistic bounce
        self.damping = 0.95
        
    def update(self, dt):
        """Update ball position and handle bouncing"""
        # Apply gravity (frame-rate independent)
        self.vy += self.gravity * dt
        
        # Update position (frame-rate independent)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        
        # Bounce off walls (x-axis)
        if abs(self.x) > self.bounds - self.radius:
            self.vx = -self.vx * self.damping
            self.x = (self.bounds - self.radius) * (1 if self.x > 0 else -1)
        
        # Bounce off floor and ceiling (y-axis)
        if abs(self.y) > self.bounds - self.radius:
            self.vy = -self.vy * self.damping
            self.y = (self.bounds - self.radius) * (1 if self.y > 0 else -1)
        
        # Bounce off front and back walls (z-axis)
        if abs(self.z + 5.0) > self.bounds - self.radius:
            self.vz = -self.vz * self.damping
            if self.z + 5.0 > self.bounds - self.radius:
                self.z = -5.0 + (self.bounds - self.radius)
            else:
                self.z = -5.0 - (self.bounds - self.radius)
    
    def draw_sphere(self, slices=20, stacks=20):
        """Draw a sphere using OpenGL"""
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)
            
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)
                
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(
                    self.x + self.radius * x * zr0,
                    self.y + self.radius * y * zr0,
                    self.z + self.radius * z0
                )
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(
                    self.x + self.radius * x * zr1,
                    self.y + self.radius * y * zr1,
                    self.z + self.radius * z1
                )
            glEnd()


class BallWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set window background color (black)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        # Enable depth testing for 3D
        glEnable(GL_DEPTH_TEST)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up light position
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(5.0, 5.0, 5.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat * 4)(0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(0.8, 0.8, 0.8, 1.0))
        
        # Create the ball
        self.ball = BouncingBall3D()
        
        # Schedule update
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        
    def on_draw(self):
        """Render the scene"""
        self.clear()
        
        # Set up 3D perspective
        setup_perspective(60.0, self.width / self.height, 0.1, 100.0)
        
        # Set up view matrix
        setup_lookat(0, 0, 0,    # Eye position
                     0, 0, -5,   # Look at position
                     0, 1, 0)    # Up vector
        
        # Draw the red ball
        glColor3f(1.0, 0.0, 0.0)  # Red color
        self.ball.draw_sphere()
        
        # Draw a wireframe box to show boundaries
        self.draw_boundary_box()
    
    def draw_boundary_box(self):
        """Draw wireframe box showing the boundaries"""
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)
        glLineWidth(1.0)
        
        b = self.ball.bounds
        z_offset = -5.0
        
        # Draw the 12 edges of the box
        lines = [
            # Bottom face
            [(-b, -b, z_offset - b), (b, -b, z_offset - b)],
            [(b, -b, z_offset - b), (b, -b, z_offset + b)],
            [(b, -b, z_offset + b), (-b, -b, z_offset + b)],
            [(-b, -b, z_offset + b), (-b, -b, z_offset - b)],
            # Top face
            [(-b, b, z_offset - b), (b, b, z_offset - b)],
            [(b, b, z_offset - b), (b, b, z_offset + b)],
            [(b, b, z_offset + b), (-b, b, z_offset + b)],
            [(-b, b, z_offset + b), (-b, b, z_offset - b)],
            # Vertical edges
            [(-b, -b, z_offset - b), (-b, b, z_offset - b)],
            [(b, -b, z_offset - b), (b, b, z_offset - b)],
            [(b, -b, z_offset + b), (b, b, z_offset + b)],
            [(-b, -b, z_offset + b), (-b, b, z_offset + b)],
        ]
        
        glBegin(GL_LINES)
        for line in lines:
            glVertex3f(*line[0])
            glVertex3f(*line[1])
        glEnd()
        
        glEnable(GL_LIGHTING)
    
    def update(self, dt):
        """Update game state"""
        self.ball.update(dt)
    
    def on_resize(self, width, height):
        """Handle window resize"""
        super().on_resize(width, height)
        glViewport(0, 0, width, height)
        return pyglet.event.EVENT_HANDLED


def main():
    """Main entry point"""
    window = BallWindow(width=800, height=600, caption="3D Bouncing Red Ball", resizable=True)
    pyglet.app.run()


if __name__ == "__main__":
    main()

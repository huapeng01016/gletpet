"""
Bouncing Ball Game using Pyglet

A simple game with a ball that bounces around the window,
colliding with the boundaries and reversing direction.
"""
import pyglet
from pyglet import shapes


class BouncingBall:
    """Represents a bouncing ball with physics"""
    
    def __init__(self, x, y, radius=30, color=(255, 100, 100)):
        """
        Initialize the bouncing ball
        
        Args:
            x: Initial x position
            y: Initial y position
            radius: Ball radius
            color: RGB color tuple
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
        # Velocity in pixels per second
        self.velocity_x = 200
        self.velocity_y = 250
        
        # Create the visual circle
        self.shape = shapes.Circle(x, y, radius, color=color)
    
    def update(self, dt, window_width, window_height):
        """
        Update ball position and handle collisions
        
        Args:
            dt: Delta time in seconds
            window_width: Window width
            window_height: Window height
        """
        # Update position based on velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Check collision with left/right walls
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.velocity_x = abs(self.velocity_x)  # Bounce right
        elif self.x + self.radius >= window_width:
            self.x = window_width - self.radius
            self.velocity_x = -abs(self.velocity_x)  # Bounce left
        
        # Check collision with top/bottom walls
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity_y = abs(self.velocity_y)  # Bounce up
        elif self.y + self.radius >= window_height:
            self.y = window_height - self.radius
            self.velocity_y = -abs(self.velocity_y)  # Bounce down
        
        # Update shape position
        self.shape.x = self.x
        self.shape.y = self.y
    
    def draw(self):
        """Draw the ball"""
        self.shape.draw()


class BouncingBallGame:
    """Main game class"""
    
    def __init__(self, width=800, height=600):
        """
        Initialize the game
        
        Args:
            width: Window width
            height: Window height
        """
        self.width = width
        self.height = height
        
        # Create window
        self.window = pyglet.window.Window(width, height, caption="Bouncing Ball Game")
        
        # Create ball in the center
        self.ball = BouncingBall(width // 2, height // 2)
        
        # Create background batch for efficient rendering
        self.batch = pyglet.graphics.Batch()
        
        # Set up event handlers
        self.window.on_draw = self.on_draw
        
        # Schedule update at 60 FPS
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        
        # Add instructions label
        self.instructions = pyglet.text.Label(
            'Press ESC to exit',
            font_name='Arial',
            font_size=12,
            x=10,
            y=height - 20,
            color=(255, 255, 255, 255)
        )
    
    def update(self, dt):
        """Update game state"""
        self.ball.update(dt, self.width, self.height)
    
    def on_draw(self):
        """Draw the game"""
        self.window.clear()
        
        # Set background color (light blue)
        pyglet.gl.glClearColor(0.53, 0.81, 0.92, 1.0)
        
        # Draw ball
        self.ball.draw()
        
        # Draw instructions
        self.instructions.draw()
    
    def run(self):
        """Start the game"""
        pyglet.app.run()


def main():
    """Entry point for the game"""
    game = BouncingBallGame()
    game.run()


if __name__ == "__main__":
    main()

"""
Unit tests for the bouncing ball game
"""
import unittest
from bouncing_ball import BouncingBall


class TestBouncingBall(unittest.TestCase):
    """Test cases for BouncingBall class"""
    
    def test_ball_initialization(self):
        """Test that ball initializes with correct values"""
        ball = BouncingBall(100, 200, radius=25, color=(255, 0, 0))
        self.assertEqual(ball.x, 100)
        self.assertEqual(ball.y, 200)
        self.assertEqual(ball.radius, 25)
        self.assertEqual(ball.color, (255, 0, 0))
    
    def test_ball_movement(self):
        """Test that ball moves according to velocity"""
        ball = BouncingBall(100, 100)
        initial_x = ball.x
        initial_y = ball.y
        
        # Update with small time step
        ball.update(0.1, 800, 600)
        
        # Ball should have moved
        self.assertNotEqual(ball.x, initial_x)
        self.assertNotEqual(ball.y, initial_y)
    
    def test_ball_collision_left_wall(self):
        """Test ball bounces off left wall"""
        ball = BouncingBall(10, 300)
        ball.velocity_x = -200  # Moving left
        
        # Update to trigger collision
        ball.update(0.1, 800, 600)
        
        # Velocity should reverse (become positive)
        self.assertGreater(ball.velocity_x, 0)
        # Ball should be pushed away from wall
        self.assertGreaterEqual(ball.x, ball.radius)
    
    def test_ball_collision_right_wall(self):
        """Test ball bounces off right wall"""
        ball = BouncingBall(790, 300)
        ball.velocity_x = 200  # Moving right
        
        # Update to trigger collision
        ball.update(0.1, 800, 600)
        
        # Velocity should reverse (become negative)
        self.assertLess(ball.velocity_x, 0)
        # Ball should be pushed away from wall
        self.assertLessEqual(ball.x, 800 - ball.radius)
    
    def test_ball_collision_bottom_wall(self):
        """Test ball bounces off bottom wall"""
        ball = BouncingBall(400, 10)
        ball.velocity_y = -200  # Moving down
        
        # Update to trigger collision
        ball.update(0.1, 800, 600)
        
        # Velocity should reverse (become positive)
        self.assertGreater(ball.velocity_y, 0)
        # Ball should be pushed away from wall
        self.assertGreaterEqual(ball.y, ball.radius)
    
    def test_ball_collision_top_wall(self):
        """Test ball bounces off top wall"""
        ball = BouncingBall(400, 590)
        ball.velocity_y = 200  # Moving up
        
        # Update to trigger collision
        ball.update(0.1, 800, 600)
        
        # Velocity should reverse (become negative)
        self.assertLess(ball.velocity_y, 0)
        # Ball should be pushed away from wall
        self.assertLessEqual(ball.y, 600 - ball.radius)


if __name__ == '__main__':
    unittest.main()

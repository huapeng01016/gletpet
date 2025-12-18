#!/usr/bin/env python3
"""
Unit tests for the 3D bouncing ball physics (without GUI)
"""
import math


class BouncingBall3DPhysics:
    """Ball physics without OpenGL dependencies for testing"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0
        
        self.vx = 1.2
        self.vy = 1.8
        self.vz = 0.6
        
        self.radius = 0.5
        self.bounds = 2.5
        self.gravity = -0.06
        self.damping = 0.95
        
    def update(self, dt):
        """Update ball position and handle bouncing"""
        self.vy += self.gravity * dt
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        
        if abs(self.x) > self.bounds - self.radius:
            self.vx = -self.vx * self.damping
            self.x = (self.bounds - self.radius) * (1 if self.x > 0 else -1)
        
        if abs(self.y) > self.bounds - self.radius:
            self.vy = -self.vy * self.damping
            self.y = (self.bounds - self.radius) * (1 if self.y > 0 else -1)
        
        if abs(self.z + 5.0) > self.bounds - self.radius:
            self.vz = -self.vz * self.damping
            if self.z + 5.0 > self.bounds - self.radius:
                self.z = -5.0 + (self.bounds - self.radius)
            else:
                self.z = -5.0 - (self.bounds - self.radius)


def test_ball_physics():
    """Test that ball physics work correctly"""
    ball = BouncingBall3DPhysics()
    
    print("Testing 3D Bouncing Ball Physics...")
    print(f"Initial position: ({ball.x:.2f}, {ball.y:.2f}, {ball.z:.2f})")
    print(f"Initial velocity: ({ball.vx:.3f}, {ball.vy:.3f}, {ball.vz:.3f})")
    
    # Simulate 1000 updates (about 16.7 seconds at 60 FPS)
    for i in range(1000):
        ball.update(1/60.0)
        
        # Verify boundaries
        assert abs(ball.x) <= ball.bounds + 0.01, f"X out of bounds at step {i}: {ball.x}"
        assert abs(ball.y) <= ball.bounds + 0.01, f"Y out of bounds at step {i}: {ball.y}"
        assert abs(ball.z + 5.0) <= ball.bounds + 0.01, f"Z out of bounds at step {i}: {ball.z + 5.0}"
    
    print(f"After 1000 updates:")
    print(f"Position: ({ball.x:.2f}, {ball.y:.2f}, {ball.z:.2f})")
    print(f"Velocity: ({ball.vx:.3f}, {ball.vy:.3f}, {ball.vz:.3f})")
    
    # Verify ball is still moving (not stuck)
    total_velocity = abs(ball.vx) + abs(ball.vy) + abs(ball.vz)
    assert total_velocity > 0.001, "Ball stopped moving"
    
    print("✓ All physics tests passed!")
    return True


if __name__ == "__main__":
    test_ball_physics()

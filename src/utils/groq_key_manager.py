"""
Multi-Key Groq API Manager

Automatically rotates between multiple API keys when rate limits are hit.
"""

import os
from dotenv import load_dotenv
import time

class GroqKeyManager:
    """
    Manages multiple Groq API keys with automatic rotation on rate limit.
    """
    
    def __init__(self):
        load_dotenv()
        
        # Load all available keys
        self.keys = []
        self.key_names = []
        
        # Primary key
        primary_key = os.getenv("GROQ_API_KEY")
        if primary_key:
            self.keys.append(primary_key)
            self.key_names.append("GROQ_API_KEY")
        
        # Secondary keys (GROQ_API_KEY_2, GROQ_API_KEY_3, etc.)
        for i in range(2, 10):  # Support up to 9 keys
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key:
                self.keys.append(key)
                self.key_names.append(f"GROQ_API_KEY_{i}")
        
        if not self.keys:
            raise ValueError("No Groq API keys found in .env file")
        
        self.current_key_index = 0
        self.rate_limit_cooldown = {}  # Track cooldown for each key
        
        print(f"✅ Loaded {len(self.keys)} Groq API key(s)")
        for name in self.key_names:
            print(f"   - {name}")
    
    def get_current_key(self):
        """Get the currently active API key"""
        return self.keys[self.current_key_index]
    
    def get_current_key_name(self):
        """Get the name of the currently active key"""
        return self.key_names[self.current_key_index]
    
    def rotate_key(self):
        """
        Rotate to the next available API key.
        
        Returns:
            bool: True if rotation successful, False if all keys exhausted
        """
        # Mark current key as rate-limited
        self.rate_limit_cooldown[self.current_key_index] = time.time()
        
        # Try next key
        original_index = self.current_key_index
        
        for _ in range(len(self.keys)):
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)
            
            # Check if this key is still in cooldown (60 seconds)
            last_limit_time = self.rate_limit_cooldown.get(self.current_key_index, 0)
            if time.time() - last_limit_time > 60:
                print(f"🔄 Rotated to {self.key_names[self.current_key_index]}")
                return True
        
        # All keys are rate-limited
        print(f"⚠️  All {len(self.keys)} API keys are rate-limited")
        
        # Wait for cooldown on first key
        wait_time = 60 - (time.time() - self.rate_limit_cooldown.get(0, 0))
        if wait_time > 0:
            print(f"⏳ Waiting {wait_time:.0f} seconds for cooldown...")
            time.sleep(wait_time)
            self.current_key_index = 0
            return True
        
        return False
    
    def handle_rate_limit_error(self, error):
        """
        Handle rate limit error by rotating keys.
        
        Args:
            error: The error object
        
        Returns:
            bool: True if successfully rotated, False otherwise
        """
        if "rate_limit" in str(error).lower() or "429" in str(error):
            print(f"⚠️  Rate limit hit on {self.get_current_key_name()}")
            return self.rotate_key()
        return False


# Global key manager instance
_key_manager = None

def get_key_manager():
    """Get or create the global key manager"""
    global _key_manager
    if _key_manager is None:
        _key_manager = GroqKeyManager()
    return _key_manager

def get_groq_api_key():
    """Get the current active Groq API key"""
    manager = get_key_manager()
    return manager.get_current_key()

def handle_groq_error(error):
    """
    Handle Groq API errors with automatic key rotation.
    
    Args:
        error: The error object
    
    Returns:
        bool: True if should retry, False otherwise
    """
    manager = get_key_manager()
    return manager.handle_rate_limit_error(error)


if __name__ == "__main__":
    # Test the key manager
    print("Testing Groq Key Manager...")
    print("="*60)
    
    manager = GroqKeyManager()
    
    print(f"\nCurrent key: {manager.get_current_key_name()}")
    print(f"Total keys: {len(manager.keys)}")
    
    # Simulate rate limit
    print("\nSimulating rate limit...")
    if manager.rotate_key():
        print(f"✅ Successfully rotated to: {manager.get_current_key_name()}")
    else:
        print("❌ No keys available")

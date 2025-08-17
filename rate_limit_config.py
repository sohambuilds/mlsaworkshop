#!/usr/bin/env python3
"""
Rate Limiting Configuration for AGNO Workshop
=============================================

This module provides utilities for managing API rate limits when using teams.
"""

import time
from typing import Dict, Any


class RateLimitConfig:
    """Configuration for handling API rate limits"""
    
    # Conservative settings for Gemini API
    DEFAULT_DELAY = 2  # seconds between retries
    TEAM_DELAY = 3     # seconds between team member responses  
    EXPONENTIAL_BACKOFF = True
    
    # Gemini Flash has these approximate limits:
    # - 1000 requests per minute for free tier
    # - 1 million tokens per minute for free tier
    
    @classmethod
    def get_agent_config(cls) -> Dict[str, Any]:
        """Get rate limiting configuration for individual agents"""
        return {
            "exponential_backoff": cls.EXPONENTIAL_BACKOFF,
            "delay_between_retries": cls.DEFAULT_DELAY,
        }
    
    @classmethod
    def get_team_config(cls) -> Dict[str, Any]:
        """Teams don't have direct rate limiting - individual agents handle it"""
        return {
            "note": "Rate limiting is configured on individual agents, not teams",
            "agent_delay": cls.DEFAULT_DELAY,
        }
    
    @classmethod
    def add_team_delays(cls, enable: bool = True):
        """Add delays between team member responses to prevent rate limiting"""
        if enable:
            print(f"⏱️  Adding {cls.TEAM_DELAY}s delays between team responses to prevent rate limiting")
            time.sleep(cls.TEAM_DELAY)


def print_rate_limit_info():
    """Print information about rate limiting configuration"""
    print("\n⚡ Rate Limiting Configuration")
    print("=" * 35)
    print("🎯 Optimized for Gemini API limits:")
    print(f"   - Exponential backoff: {RateLimitConfig.EXPONENTIAL_BACKOFF}")
    print(f"   - Individual agent retry delay: {RateLimitConfig.DEFAULT_DELAY}s")
    print("\n💡 Rate limiting is applied to individual agents")
    print("   Teams coordinate agents, but agents handle their own rate limits")
    print("   This prevents 'Too Many Requests' errors automatically")


if __name__ == "__main__":
    print_rate_limit_info()


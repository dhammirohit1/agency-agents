"""
Base Agent Class - Parent class for all sub-agents
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger


class BaseAgent(ABC):
    """
    Abstract base class for all agent types.
    Each agent must implement core methods for operation.
    """
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.is_running = False
        self.last_activity = None
        self.performance_metrics = {
            "tasks_completed": 0,
            "revenue_generated": 0.0,
            "errors": 0,
            "uptime_seconds": 0
        }
        self.start_time = None
        
    @abstractmethod
    async def start(self) -> bool:
        """
        Start the agent's main loop.
        Returns True if started successfully.
        """
        pass
    
    @abstractmethod
    async def stop(self) -> bool:
        """
        Gracefully stop the agent.
        Returns True if stopped successfully.
        """
        pass
    
    @abstractmethod
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single task and return results.
        """
        pass
    
    @abstractmethod
    async def generate_revenue(self) -> float:
        """
        Execute revenue-generating activities.
        Returns amount earned (0.0 if none).
        """
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check agent health and return status.
        """
        return {
            "agent_id": self.agent_id,
            "is_running": self.is_running,
            "last_activity": self.last_activity,
            "performance": self.performance_metrics,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        }
    
    def _update_metrics(self, revenue: float = 0.0, error: bool = False):
        """Update performance metrics."""
        self.performance_metrics["tasks_completed"] += 1
        self.performance_metrics["revenue_generated"] += revenue
        if error:
            self.performance_metrics["errors"] += 1
        self.last_activity = datetime.now()
    
    async def _run_with_retry(self, func, max_retries: int = 3):
        """Execute function with retry logic."""
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                logger.error(f"{self.agent_id} - Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.agent_id}, running={self.is_running})"

"""
Main entry point for the Anthropomorphic AI System
"""

import logging
from core.config import settings
from core.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

def main():
    """Initialize and start the AI system"""
    try:
        logger.info("Starting Anthropomorphic AI System...")
        
        # Initialize orchestrator
        orchestrator = Orchestrator()
        
        # Start system components
        orchestrator.initialize_modules()
        
        logger.info("Anthropomorphic AI System started successfully")
        
        # Keep the system running
        orchestrator.run()
        
    except Exception as e:
        logger.error(f"Failed to start system: {e}")
        raise

if __name__ == "__main__":
    main()
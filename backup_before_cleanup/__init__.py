"""
KatenaScout Conversation Orchestrator

This module provides conversation orchestration for the KatenaScout application,
handling intent recognition, entity extraction, and response generation.
"""

from .models import ConversationMemory, Intent
from .orchestrator import conversation_orchestrator, process_user_message
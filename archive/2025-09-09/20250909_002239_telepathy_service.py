"""
TELEPATHY SERVICE - FASE 9
Unified telepathy operations for chat and CLI
"""

import time
import json
from datetime import datetime
from typing import Dict, Any, Optional, List


class TelepathyService:
    """Service for telepathy network operations"""
    
    def __init__(self, telepathy_network=None):
        """Initialize telepathy service
        
        Args:
            telepathy_network: TelepathyNetwork instance
        """
        self.network = telepathy_network
        self.message_history = []
        self.max_history = 100
        
    def send_message(self, message: str, channel: str = "default", 
                    metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Send telepathic message - FASE 9 unified
        
        Args:
            message: Message to send
            channel: Channel to use
            metadata: Optional metadata
            
        Returns:
            Result dictionary
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "channel": channel,
            "message_id": None,
            "details": {}
        }
        
        try:
            if not self.network:
                raise ValueError("Telepathy network not available")
            
            # Generate message ID
            message_id = f"msg_{int(time.time() * 1000)}"
            
            # Prepare full message
            full_message = {
                "id": message_id,
                "content": message,
                "channel": channel,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Send via network
            if hasattr(self.network, 'send'):
                self.network.send(channel, json.dumps(full_message))
                result["success"] = True
            else:
                # Fallback: store locally
                self._store_local_message(full_message)
                result["success"] = True
                result["details"]["fallback"] = "stored_locally"
            
            result["message_id"] = message_id
            result["details"]["length"] = len(message)
            
            # Add to history
            self.message_history.append(full_message)
            if len(self.message_history) > self.max_history:
                self.message_history.pop(0)
            
        except Exception as e:
            result["error"] = str(e)
            result["details"]["error_type"] = type(e).__name__
            
        return result
    
    def receive_messages(self, channel: str = "default", 
                        limit: int = 10) -> Dict[str, Any]:
        """Receive telepathic messages
        
        Args:
            channel: Channel to read from
            limit: Maximum messages to retrieve
            
        Returns:
            Result with messages
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "channel": channel,
            "messages": [],
            "count": 0
        }
        
        try:
            if not self.network:
                # Return from local history
                channel_messages = [
                    m for m in self.message_history 
                    if m.get("channel") == channel
                ][-limit:]
                
                result["messages"] = channel_messages
                result["count"] = len(channel_messages)
                result["success"] = True
                result["source"] = "local_history"
                
            elif hasattr(self.network, 'receive'):
                # Receive from network
                messages = self.network.receive(channel, limit)
                result["messages"] = messages
                result["count"] = len(messages)
                result["success"] = True
                result["source"] = "network"
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def broadcast(self, message: str, channels: List[str] = None) -> Dict[str, Any]:
        """Broadcast message to multiple channels
        
        Args:
            message: Message to broadcast
            channels: List of channels (default: all)
            
        Returns:
            Result dictionary
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "broadcast_id": f"bcast_{int(time.time() * 1000)}",
            "channels_sent": [],
            "channels_failed": []
        }
        
        # Default channels
        if not channels:
            channels = ["default", "system", "evolution"]
        
        for channel in channels:
            send_result = self.send_message(message, channel)
            
            if send_result["success"]:
                result["channels_sent"].append(channel)
            else:
                result["channels_failed"].append(channel)
        
        result["success"] = len(result["channels_sent"]) > 0
        result["total_sent"] = len(result["channels_sent"])
        result["total_failed"] = len(result["channels_failed"])
        
        return result
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get telepathy network status
        
        Returns:
            Network status dictionary
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "available": self.network is not None,
            "messages_in_history": len(self.message_history)
        }
        
        if self.network and hasattr(self.network, 'get_status'):
            network_status = self.network.get_status()
            status.update({
                "mode": network_status.get("mode", "unknown"),
                "connected": network_status.get("connected", False),
                "redis_available": network_status.get("redis_available", False)
            })
        
        if self.network and hasattr(self.network, 'get_active_peers'):
            peers = self.network.get_active_peers()
            status["active_peers"] = len(peers)
            status["peer_list"] = peers[:5]  # First 5 peers
        
        return status
    
    def sync_peers(self) -> Dict[str, Any]:
        """Synchronize with network peers
        
        Returns:
            Sync result
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "peers_synced": 0
        }
        
        try:
            if not self.network:
                result["message"] = "Network not available"
                return result
            
            # Get peers
            if hasattr(self.network, 'get_active_peers'):
                peers = self.network.get_active_peers()
                
                # Simulate sync (in real implementation, would sync data)
                for peer in peers:
                    # Send sync message
                    self.send_message(
                        f"SYNC_REQUEST_{datetime.now().isoformat()}",
                        channel="sync",
                        metadata={"peer": peer}
                    )
                
                result["peers_synced"] = len(peers)
                result["success"] = True
                result["message"] = f"Synced with {len(peers)} peers"
            else:
                result["message"] = "Peer sync not supported"
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Sync failed: {e}"
        
        return result
    
    def _store_local_message(self, message: Dict[str, Any]):
        """Store message locally when network unavailable
        
        Args:
            message: Message to store
        """
        # In production, would persist to disk
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get telepathy service status
        
        Returns:
            Service status
        """
        return {
            "service": "TelepathyService",
            "available": True,
            "network_connected": self.network is not None,
            "messages_cached": len(self.message_history),
            "features": ["send", "receive", "broadcast", "sync"]
        }
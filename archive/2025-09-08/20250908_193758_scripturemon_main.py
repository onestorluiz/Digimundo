#!/usr/bin/env python3
"""
🎬 SCRIPTUREMON MAIN ENTRY POINT
Unified launcher that initializes all subsystems and starts the chat interface
"""

import sys
import os
import signal
import asyncio
import logging
from pathlib import Path
from typing import Optional

# Add project to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all necessary components
from apps.scripturemon.chat import ScripturemonChat
from apps.scripturemon.memory_manager import UnifiedMemoryManager
try:
    from apps.scripturemon.telepathy_network import TelepathyNetwork as TelepathicNetwork
except ImportError:
    # Fallback if module structure is different
    TelepathicNetwork = None
from apps.scripturemon.immortality import ImmortalityProtocol
from apps.scripturemon.soul import Soul

# Import CLI if available
try:
    from apps.scripturemon.cli import main as cli_main
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    logger.warning("CLI module not available, using basic interface")

class ScripturemonLauncher:
    """Main launcher for Scripturemon system"""
    
    def __init__(self):
        """Initialize all subsystems"""
        print("\n" + "="*70)
        print("🎬 SCRIPTUREMON - INITIALIZING COMPLETE SYSTEM")
        print("="*70)
        
        self.soul = None
        self.memory_manager = None
        self.telepathy = None
        self.immortality = None
        self.chat = None
        self.running = True
        
        # Initialize in order
        self._initialize_soul()
        self._initialize_memory()
        self._initialize_telepathy()
        self._initialize_immortality()
        self._initialize_chat()
        
        print("\n✅ All systems initialized successfully!")
        print("="*70)
    
    def _initialize_soul(self):
        """Initialize Soul system"""
        try:
            print("\n🔮 Initializing Soul...")
            self.soul = Soul()
            print(f"   ✅ Soul signature: {self.soul.signature[:8]}...")
        except Exception as e:
            logger.error(f"Failed to initialize Soul: {e}")
            print(f"   ❌ Soul initialization failed: {e}")
    
    def _initialize_memory(self):
        """Initialize Memory Manager"""
        try:
            print("\n🧠 Initializing Memory Manager...")
            self.memory_manager = UnifiedMemoryManager()
            print("   ✅ Memory Manager active with all 7 systems")
        except Exception as e:
            logger.error(f"Failed to initialize Memory Manager: {e}")
            print(f"   ❌ Memory Manager initialization failed: {e}")
            # Create minimal memory manager
            self.memory_manager = None
    
    def _initialize_telepathy(self):
        """Initialize Telepathy Network"""
        if TelepathicNetwork is None:
            print("\n📡 Telepathy Network not available (module not found)")
            self.telepathy = None
            return
            
        try:
            print("\n📡 Initializing Telepathy Network...")
            self.telepathy = TelepathicNetwork()
            status = self.telepathy.get_status() if hasattr(self.telepathy, 'get_status') else {}
            if status.get('redis_connected'):
                print("   ✅ Telepathy connected to Redis")
            else:
                print("   ⚠️ Telepathy using fallback mode")
        except Exception as e:
            logger.error(f"Failed to initialize Telepathy: {e}")
            print(f"   ⚠️ Telepathy initialization failed (using fallback): {e}")
            self.telepathy = None
    
    def _initialize_immortality(self):
        """Initialize Immortality Protocol"""
        try:
            print("\n♾️ Initializing Immortality Protocol...")
            if self.soul:
                self.immortality = ImmortalityProtocol(
                    backup_path=PROJECT_ROOT / "backups",
                    soul_signature=self.soul.signature
                )
                # Start backup thread if available
                if hasattr(self.immortality, 'start_backup_thread'):
                    self.immortality.start_backup_thread()
                print("   ✅ Immortality Protocol active (auto-backup every 5 min)")
            else:
                print("   ⚠️ Immortality Protocol skipped (no Soul)")
        except Exception as e:
            logger.error(f"Failed to initialize Immortality: {e}")
            print(f"   ❌ Immortality Protocol failed: {e}")
            self.immortality = None
    
    def _initialize_chat(self):
        """Initialize Chat Interface"""
        try:
            print("\n💬 Initializing Chat Interface...")
            self.chat = ScripturemonChat()
            print("   ✅ Chat interface ready")
        except Exception as e:
            logger.error(f"Failed to initialize Chat: {e}")
            print(f"   ❌ Chat initialization failed: {e}")
            raise  # Chat is critical, can't continue without it
    
    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        print("\n\n🛑 Shutdown signal received...")
        self.shutdown()
        sys.exit(0)
    
    def shutdown(self):
        """Graceful shutdown of all systems"""
        self.running = False
        
        print("\n🔄 Shutting down systems...")
        
        # Save chat state
        if self.chat and hasattr(self.chat, 'soul'):
            try:
                self.chat.soul.save_state()
                print("   ✅ Chat state saved")
            except:
                pass
        
        # Stop immortality backup
        if self.immortality and hasattr(self.immortality, 'stop_backup_thread'):
            try:
                self.immortality.stop_backup_thread()
                print("   ✅ Immortality backup stopped")
            except:
                pass
        
        # Close telepathy connections
        if self.telepathy and hasattr(self.telepathy, 'close'):
            try:
                self.telepathy.close()
                print("   ✅ Telepathy connections closed")
            except:
                pass
        
        print("\n👋 Goodbye!")
    
    def run_interactive(self):
        """Run interactive chat loop"""
        print("\n🎬 SCRIPTUREMON CHAT INTERFACE")
        print("="*70)
        print("Type /help for commands or just start chatting")
        print("Type /quit or Ctrl+C to exit")
        print("="*70 + "\n")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            while self.running:
                try:
                    # Get user input
                    user_input = input("\n🎬 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Check for exit commands
                    if user_input.lower() in ['/quit', '/exit', 'exit', 'quit']:
                        break
                    
                    # Process through chat
                    response = self.chat.process_input(user_input)
                    
                    # Display response
                    print(f"\n🤖 Scripturemon: {response}")
                    
                except KeyboardInterrupt:
                    print("\n\n⚠️ Interrupted by user")
                    break
                except EOFError:
                    print("\n\n⚠️ Input stream closed")
                    break
                except Exception as e:
                    logger.error(f"Error processing input: {e}")
                    print(f"\n❌ Error: {e}")
        
        finally:
            self.shutdown()
    
    def run_cli(self):
        """Run using the full CLI interface if available"""
        if CLI_AVAILABLE:
            try:
                # Use the Typer CLI
                cli_main()
            except Exception as e:
                logger.error(f"CLI failed: {e}")
                print(f"\n⚠️ CLI failed, falling back to interactive mode: {e}")
                self.run_interactive()
        else:
            # Fallback to interactive mode
            self.run_interactive()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🎬 SCRIPTUREMON - AI System for Screenwriting'
    )
    parser.add_argument(
        '--mode',
        choices=['cli', 'interactive', 'auto'],
        default='auto',
        help='Launch mode (cli/interactive/auto)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Set debug level if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create launcher
        launcher = ScripturemonLauncher()
        
        # Run in requested mode
        if args.mode == 'cli':
            launcher.run_cli()
        elif args.mode == 'interactive':
            launcher.run_interactive()
        else:  # auto
            # Try CLI first, fallback to interactive
            if CLI_AVAILABLE:
                launcher.run_cli()
            else:
                launcher.run_interactive()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
🔔 INTELLIGENT NOTIFICATION SYSTEM SUPREME
Context-aware notifications with priority and intelligence
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
import queue
from collections import defaultdict, deque
import hashlib

class NotificationType(Enum):
    ANALYSIS_STARTED = 'analysis_started'
    ANALYSIS_COMPLETE = 'analysis_complete'
    PROBLEM_FOUND = 'problem_found'
    SUGGESTION_READY = 'suggestion_ready'
    MEMORY_WARNING = 'memory_warning'
    MEMORY_CRITICAL = 'memory_critical'
    THINKING_SPACE = 'thinking_space'
    SECTOR_CHANGE = 'sector_change'
    MILESTONE_REACHED = 'milestone_reached'
    TASK_COMPLETE = 'task_complete'
    BATCH_READY = 'batch_ready'
    EXPORT_READY = 'export_ready'
    ERROR_OCCURRED = 'error_occurred'
    WARNING_ISSUED = 'warning_issued'
    SUCCESS_ACHIEVED = 'success_achieved'
    INFO_UPDATE = 'info_update'
    INSPIRATION_FOUND = 'inspiration_found'
    PATTERN_DETECTED = 'pattern_detected'
    BREAKTHROUGH_MOMENT = 'breakthrough_moment'
    CREATIVE_BLOCK = 'creative_block'

class Priority(Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    BACKGROUND = 4

@dataclass
class Notification:
    type: NotificationType
    priority: Priority
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = 'system'
    action_required: bool = False
    expires_at: Optional[datetime] = None
    notification_id: str = ''
    seen: bool = False
    actioned: bool = False

    def __post_init__(self):
        if not self.notification_id:
            content = f'{self.type.value}{self.title}{self.timestamp}'
            self.notification_id = hashlib.md5(content.encode()).hexdigest()[:8]

class NotificationChannel(Enum):
    CONSOLE = 'console'
    FILE = 'file'
    SYSTEM = 'system'
    DASHBOARD = 'dashboard'
    SOUND = 'sound'
    EMAIL = 'email'
    WEBHOOK = 'webhook'

@dataclass
class NotificationRule:
    """Rules for intelligent notification filtering"""
    name: str
    condition: Callable[[Notification], bool]
    action: str
    priority_override: Optional[Priority] = None
    channel_override: Optional[List[NotificationChannel]] = None
    aggregation_window: Optional[timedelta] = None

class IntelligentNotificationSystem:

    def __init__(self):
        self.notifications: deque = deque(maxlen=1000)
        self.notification_queue = queue.Queue()
        self.channels: Dict[NotificationChannel, bool] = {NotificationChannel.CONSOLE: True, NotificationChannel.FILE: True, NotificationChannel.SYSTEM: False, NotificationChannel.DASHBOARD: True, NotificationChannel.SOUND: False, NotificationChannel.EMAIL: False, NotificationChannel.WEBHOOK: False}
        self.rules: List[NotificationRule] = []
        self.setup_default_rules()
        self.aggregation_buffers: Dict[str, List[Notification]] = defaultdict(list)
        self.last_aggregation: Dict[str, datetime] = {}
        self.subscribers: Dict[NotificationType, List[Callable]] = defaultdict(list)
        self.stats = {'total_sent': 0, 'by_type': defaultdict(int), 'by_priority': defaultdict(int), 'suppressed': 0, 'aggregated': 0}
        self.config = self.load_config()
        self.output_dir = Path('output/notifications')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_notifications)
        self.processor_thread.daemon = True
        self.processor_thread.start()

    def load_config(self) -> Dict:
        """Load notification configuration"""
        config_path = Path('config/notifications.json')
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {'quiet_hours': {'start': '22:00', 'end': '08:00'}, 'rate_limits': {'per_minute': 30, 'per_hour': 500}, 'priority_sounds': {'critical': 'alert.wav', 'high': 'ding.wav', 'medium': 'pop.wav'}, 'aggregation_windows': {'similar_errors': 60, 'progress_updates': 30, 'memory_warnings': 120}}

    def setup_default_rules(self):
        """Setup intelligent filtering rules"""
        self.add_rule(NotificationRule(name='aggregate_errors', condition=lambda n: n.type == NotificationType.ERROR_OCCURRED, action='aggregate', aggregation_window=timedelta(seconds=60)))
        self.add_rule(NotificationRule(name='suppress_during_critical', condition=lambda n: n.priority == Priority.LOW and self.has_critical_operations(), action='block'))
        self.add_rule(NotificationRule(name='escalate_repeated', condition=lambda n: self.is_repeated_warning(n), action='modify', priority_override=Priority.HIGH))
        self.add_rule(NotificationRule(name='batch_progress', condition=lambda n: n.type in [NotificationType.TASK_COMPLETE, NotificationType.MILESTONE_REACHED], action='aggregate', aggregation_window=timedelta(seconds=30)))

    def add_rule(self, rule: NotificationRule):
        """Add a notification rule"""
        self.rules.append(rule)

    def has_critical_operations(self) -> bool:
        """Check if critical operations are running"""
        recent = [n for n in self.notifications if (datetime.now() - n.timestamp).seconds < 300]
        return any((n.priority == Priority.CRITICAL for n in recent))

    def is_repeated_warning(self, notification: Notification) -> bool:
        """Check if this is a repeated warning"""
        if notification.type != NotificationType.WARNING_ISSUED:
            return False
        cutoff = datetime.now() - timedelta(minutes=5)
        similar = [n for n in self.notifications if n.type == notification.type and n.title == notification.title and (n.timestamp > cutoff)]
        return len(similar) > 3

    def notify(self, type: NotificationType, title: str, message: str, priority: Priority=Priority.MEDIUM, data: Optional[Dict]=None, source: str='system', action_required: bool=False, expires_in: Optional[timedelta]=None) -> str:
        """Send a notification"""
        notification = Notification(type=type, priority=priority, title=title, message=message, data=data or {}, source=source, action_required=action_required, expires_at=datetime.now() + expires_in if expires_in else None)
        notification = self._apply_rules(notification)
        if notification:
            self.notification_queue.put(notification)
            self.stats['total_sent'] += 1
            self.stats['by_type'][type.value] += 1
            self.stats['by_priority'][priority.value] += 1
            return notification.notification_id
        else:
            self.stats['suppressed'] += 1
            return ''

    def _apply_rules(self, notification: Notification) -> Optional[Notification]:
        """Apply filtering rules to notification"""
        for rule in self.rules:
            if rule.condition(notification):
                if rule.action == 'block':
                    return None
                elif rule.action == 'modify':
                    if rule.priority_override:
                        notification.priority = rule.priority_override
                    if rule.channel_override:
                        notification.data['channel_override'] = rule.channel_override
                elif rule.action == 'aggregate':
                    buffer_key = f'{rule.name}_{notification.type.value}'
                    self.aggregation_buffers[buffer_key].append(notification)
                    if buffer_key not in self.last_aggregation:
                        self.last_aggregation[buffer_key] = datetime.now()
                    if datetime.now() - self.last_aggregation[buffer_key] > rule.aggregation_window:
                        return self._create_aggregated_notification(buffer_key)
                    else:
                        self.stats['aggregated'] += 1
                        return None
        return notification

    def _create_aggregated_notification(self, buffer_key: str) -> Notification:
        """Create aggregated notification from buffer"""
        notifications = self.aggregation_buffers[buffer_key]
        if not notifications:
            return None
        first = notifications[0]
        count = len(notifications)
        aggregated = Notification(type=first.type, priority=max((n.priority for n in notifications)), title=f'{first.title} ({count} similar)', message=f'Aggregated {count} notifications:\n' + '\n'.join((f'  • {n.message[:50]}' for n in notifications[:5])), data={'aggregated_count': count, 'original_notifications': [n.notification_id for n in notifications]}, source='aggregator')
        self.aggregation_buffers[buffer_key].clear()
        self.last_aggregation[buffer_key] = datetime.now()
        return aggregated

    def _process_notifications(self):
        """Background thread to process notifications"""
        while self.running:
            try:
                notification = self.notification_queue.get(timeout=1)
                if notification.expires_at and datetime.now() > notification.expires_at:
                    continue
                self.notifications.append(notification)
                self._send_to_channels(notification)
                self._notify_subscribers(notification)
            except queue.Empty:
                continue
            except Exception as e:
                print(f'Notification error: {e}')

    def _send_to_channels(self, notification: Notification):
        """Send notification to enabled channels"""
        channels = notification.data.get('channel_override')
        if channels is None:
            channels = [ch for ch, enabled in self.channels.items() if enabled]
        for channel in channels:
            if channel == NotificationChannel.CONSOLE:
                self._send_to_console(notification)
            elif channel == NotificationChannel.FILE:
                self._send_to_file(notification)
            elif channel == NotificationChannel.DASHBOARD:
                self._send_to_dashboard(notification)
            elif channel == NotificationChannel.SYSTEM and self.channels[channel]:
                self._send_to_system(notification)
            elif channel == NotificationChannel.SOUND and self.channels[channel]:
                self._play_sound(notification)

    def _send_to_console(self, notification: Notification):
        """Send notification to console"""
        colors = {Priority.CRITICAL: '\x1b[91m', Priority.HIGH: '\x1b[93m', Priority.MEDIUM: '\x1b[94m', Priority.LOW: '\x1b[92m', Priority.BACKGROUND: '\x1b[90m'}
        color = colors.get(notification.priority, '')
        reset = '\x1b[0m'
        icons = {NotificationType.ERROR_OCCURRED: '❌', NotificationType.WARNING_ISSUED: '⚠️', NotificationType.SUCCESS_ACHIEVED: '✅', NotificationType.ANALYSIS_COMPLETE: '🎬', NotificationType.BREAKTHROUGH_MOMENT: '✨', NotificationType.MEMORY_WARNING: '💥', NotificationType.THINKING_SPACE: '🤔'}
        icon = icons.get(notification.type, '🔔')
        timestamp = notification.timestamp.strftime('%H:%M:%S')
        if notification.action_required:
            action_marker = ' [ACTION REQUIRED]'
        else:
            action_marker = ''
        message = f'{color}[{timestamp}] {icon} {notification.title}{action_marker}{reset}\n'
        if notification.message:
            message += f'  {notification.message}\n'
        print(message, end='')

    def _send_to_file(self, notification: Notification):
        """Log notification to file"""
        log_file = self.output_dir / f'notifications_{datetime.now():%Y%m%d}.log'
        with open(log_file, 'a') as f:
            log_entry = {'timestamp': notification.timestamp.isoformat(), 'id': notification.notification_id, 'type': notification.type.value, 'priority': notification.priority.value, 'title': notification.title, 'message': notification.message, 'source': notification.source, 'data': notification.data}
            f.write(json.dumps(log_entry) + '\n')

    def _send_to_dashboard(self, notification: Notification):
        """Send to dashboard if available"""
        try:
            from realtime_visual_dashboard import RealTimeVisualDashboard
        except ImportError:
            pass

    def _send_to_system(self, notification: Notification):
        """Send OS system notification"""
        try:
            if sys.platform == 'darwin':
                os.system(f"""osascript -e 'display notification "{notification.message}" with title "{notification.title}"'""")
            elif sys.platform.startswith('linux'):
                os.system(f'notify-send "{notification.title}" "{notification.message}"')
        except:
            pass

    def _play_sound(self, notification: Notification):
        """Play notification sound"""
        try:
            sound_file = self.config['priority_sounds'].get(notification.priority.name.lower())
            if sound_file and sys.platform == 'darwin':
                os.system(f'afplay /System/Library/Sounds/{sound_file} 2>/dev/null &')
        except:
            pass

    def _notify_subscribers(self, notification: Notification):
        """Notify subscriber callbacks"""
        for callback in self.subscribers[notification.type]:
            try:
                callback(notification)
            except Exception as e:
                print(f'Subscriber error: {e}')

    def subscribe(self, notification_type: NotificationType, callback: Callable[[Notification], None]):
        """Subscribe to notification type"""
        self.subscribers[notification_type].append(callback)

    def unsubscribe(self, notification_type: NotificationType, callback: Callable[[Notification], None]):
        """Unsubscribe from notification type"""
        if callback in self.subscribers[notification_type]:
            self.subscribers[notification_type].remove(callback)

    def get_unread_notifications(self, priority_min: Priority=Priority.BACKGROUND) -> List[Notification]:
        """Get unread notifications"""
        return [n for n in self.notifications if not n.seen and n.priority.value <= priority_min.value]

    def mark_as_seen(self, notification_id: str):
        """Mark notification as seen"""
        for n in self.notifications:
            if n.notification_id == notification_id:
                n.seen = True
                break

    def mark_as_actioned(self, notification_id: str):
        """Mark notification as actioned"""
        for n in self.notifications:
            if n.notification_id == notification_id:
                n.actioned = True
                break

    def get_statistics(self) -> Dict:
        """Get notification statistics"""
        return {**self.stats, 'unread_count': len(self.get_unread_notifications()), 'action_required': sum((1 for n in self.notifications if n.action_required and (not n.actioned))), 'channels_enabled': [ch.value for ch, enabled in self.channels.items() if enabled]}

    def enable_channel(self, channel: NotificationChannel, config: Optional[Dict]=None):
        """Enable a notification channel"""
        self.channels[channel] = True
        if config:
            self.config[f'{channel.value}_config'] = config

    def disable_channel(self, channel: NotificationChannel):
        """Disable a notification channel"""
        self.channels[channel] = False

    def create_digest(self, period: timedelta=timedelta(hours=1)) -> Dict:
        """Create a digest of recent notifications"""
        cutoff = datetime.now() - period
        recent = [n for n in self.notifications if n.timestamp > cutoff]
        digest = {'period': str(period), 'total': len(recent), 'by_priority': {}, 'by_type': {}, 'critical_items': [], 'action_required': [], 'top_sources': {}}
        for priority in Priority:
            count = sum((1 for n in recent if n.priority == priority))
            if count > 0:
                digest['by_priority'][priority.name] = count
        type_counts = defaultdict(int)
        for n in recent:
            type_counts[n.type.value] += 1
        digest['by_type'] = dict(type_counts)
        digest['critical_items'] = [{'title': n.title, 'message': n.message[:100], 'time': n.timestamp.isoformat()} for n in recent if n.priority == Priority.CRITICAL][:5]
        digest['action_required'] = [{'id': n.notification_id, 'title': n.title, 'message': n.message[:100]} for n in recent if n.action_required and (not n.actioned)]
        source_counts = defaultdict(int)
        for n in recent:
            source_counts[n.source] += 1
        digest['top_sources'] = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        return digest

    def shutdown(self):
        """Shutdown the notification system"""
        self.running = False
        if self.processor_thread:
            self.processor_thread.join(timeout=2)
        stats_file = self.output_dir / f'stats_{datetime.now():%Y%m%d_%H%M%S}.json'
        with open(stats_file, 'w') as f:
            json.dump(self.get_statistics(), f, indent=2)

async def main():
    """Test the notification system"""
    notifier = IntelligentNotificationSystem()
    notifier.enable_channel(NotificationChannel.SYSTEM)
    notifier.enable_channel(NotificationChannel.SOUND)
    print('Testing Intelligent Notification System\n')
    await notifier.notify(NotificationType.ANALYSIS_STARTED, 'Script Analysis Started', "Analyzing 'The Matrix Resurrections' (148 pages)", Priority.MEDIUM, data={'script': 'The Matrix Resurrections', 'pages': 148})
    await asyncio.sleep(1)
    for i in range(5):
        await notifier.notify(NotificationType.ERROR_OCCURRED, 'Format Error', f'Line {100 + i}: Incorrect margin detected', Priority.LOW)
        await asyncio.sleep(0.1)
    await asyncio.sleep(2)
    await notifier.notify(NotificationType.MEMORY_CRITICAL, 'Memory Critical', 'Only 2GB free - entering emergency mode', Priority.CRITICAL, action_required=True)
    await asyncio.sleep(1)
    await notifier.notify(NotificationType.ANALYSIS_COMPLETE, 'Analysis Complete', 'Found 23 issues, generated 87 suggestions', Priority.HIGH, data={'issues': 23, 'suggestions': 87})
    await asyncio.sleep(1)
    await notifier.notify(NotificationType.BREAKTHROUGH_MOMENT, 'Creative Breakthrough!', 'Discovered unique narrative pattern in Act 2', Priority.MEDIUM, data={'pattern': 'recursive_hero_journey'})

    def on_complete(notification: Notification):
        print(f'\n[SUBSCRIBER] Analysis complete: {notification.data}')
    notifier.subscribe(NotificationType.ANALYSIS_COMPLETE, on_complete)
    await notifier.notify(NotificationType.ANALYSIS_COMPLETE, 'Second Analysis Complete', 'Comparison analysis finished', Priority.MEDIUM)
    await asyncio.sleep(2)
    print('\n' + '=' * 50)
    print('Notification Statistics:')
    stats = notifier.get_statistics()
    for key, value in stats.items():
        print(f'  {key}: {value}')
    print('\n' + '=' * 50)
    print('Hourly Digest:')
    digest = notifier.create_digest(timedelta(minutes=1))
    print(json.dumps(digest, indent=2))
    notifier.shutdown()
    print('\nNotification system shutdown complete.')
if __name__ == '__main__':
    asyncio.run(main())
#!/usr/bin/env python3
"""
Call Center Analytics and Reporting
Analyzes call logs and generates insights
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import statistics


class CallAnalytics:
    """Analyzes call center performance and generates reports"""

    def __init__(self, log_dir="logs/calls"):
        self.log_dir = Path(log_dir)
        self.calls = []
        self._load_calls()

    def _load_calls(self):
        """Load all call logs"""
        if not self.log_dir.exists():
            print(f"⚠️  Log directory not found: {self.log_dir}")
            return

        for log_file in self.log_dir.glob("*.json"):
            try:
                with open(log_file, 'r') as f:
                    self.calls.append(json.load(f))
            except Exception as e:
                print(f"⚠️  Error loading {log_file}: {e}")

        print(f"✅ Loaded {len(self.calls)} call logs")

    def generate_report(self, days=None):
        """Generate comprehensive analytics report"""
        if not self.calls:
            print("\n❌ No call data available")
            return

        # Filter by date if specified
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            filtered_calls = [
                c for c in self.calls
                if datetime.fromisoformat(c['start_time']) >= cutoff
            ]
        else:
            filtered_calls = self.calls

        if not filtered_calls:
            print(f"\n❌ No calls found in the last {days} days")
            return

        print("\n" + "="*80)
        print("📊 CALL CENTER ANALYTICS REPORT")
        print("="*80)

        # Basic statistics
        print(f"\n📈 OVERALL STATISTICS")
        print(f"{'─'*80}")
        print(f"Total Calls: {len(filtered_calls)}")

        # Call duration stats
        durations = [c.get('duration_seconds', 0) for c in filtered_calls]
        if durations:
            print(f"Average Call Duration: {statistics.mean(durations):.1f} seconds")
            print(f"Shortest Call: {min(durations):.1f} seconds")
            print(f"Longest Call: {max(durations):.1f} seconds")

        # Resolution analysis
        print(f"\n📋 RESOLUTION BREAKDOWN")
        print(f"{'─'*80}")
        resolutions = Counter(c.get('resolution', 'unknown') for c in filtered_calls)
        for resolution, count in resolutions.most_common():
            percentage = (count / len(filtered_calls)) * 100
            print(f"{resolution:30s}: {count:3d} ({percentage:5.1f}%)")

        # Escalation rate
        escalated_count = sum(1 for c in filtered_calls if c.get('escalated', False))
        escalation_rate = (escalated_count / len(filtered_calls)) * 100
        print(f"\n⚠️  ESCALATION RATE")
        print(f"{'─'*80}")
        print(f"Escalated Calls: {escalated_count} ({escalation_rate:.1f}%)")

        # Sentiment analysis
        print(f"\n😊 CUSTOMER SENTIMENT")
        print(f"{'─'*80}")
        sentiments = [c.get('average_sentiment') for c in filtered_calls if 'average_sentiment' in c]
        if sentiments:
            avg_sentiment = statistics.mean(sentiments)
            print(f"Average Sentiment: {avg_sentiment:.2f}/5.0")

            # Sentiment distribution
            very_negative = sum(1 for s in sentiments if s < 2)
            negative = sum(1 for s in sentiments if 2 <= s < 3)
            neutral = sum(1 for s in sentiments if 3 <= s < 3.5)
            positive = sum(1 for s in sentiments if 3.5 <= s < 4.5)
            very_positive = sum(1 for s in sentiments if s >= 4.5)

            print(f"\nSentiment Distribution:")
            print(f"  😡 Very Negative (1-2):   {very_negative:3d} calls")
            print(f"  😞 Negative (2-3):        {negative:3d} calls")
            print(f"  😐 Neutral (3-3.5):       {neutral:3d} calls")
            print(f"  😊 Positive (3.5-4.5):    {positive:3d} calls")
            print(f"  😄 Very Positive (4.5-5): {very_positive:3d} calls")

        # Call reasons
        print(f"\n📞 TOP CALL REASONS")
        print(f"{'─'*80}")
        reasons = [c.get('call_reason', 'Unknown') for c in filtered_calls if c.get('call_reason')]
        if reasons:
            reason_counter = Counter(reasons)
            for reason, count in reason_counter.most_common(10):
                print(f"{count:3d}x {reason}")
        else:
            print("No call reason data available")

        # Time-based analysis
        print(f"\n⏰ CALL TIMING")
        print(f"{'─'*80}")
        call_times = [datetime.fromisoformat(c['start_time']) for c in filtered_calls]
        if call_times:
            hour_distribution = Counter(t.hour for t in call_times)
            print("Peak hours:")
            for hour, count in sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {hour:02d}:00 - {count} calls")

        # Customer analysis
        print(f"\n👥 CUSTOMER INSIGHTS")
        print(f"{'─'*80}")
        customers = [c['customer_info'] for c in filtered_calls if c.get('customer_info')]
        if customers:
            print(f"Unique customers: {len(set(c.get('name', '') for c in customers if c.get('name')))}")
            # Repeat callers
            customer_names = [c.get('name', '') for c in customers if c.get('name')]
            if customer_names:
                repeat_callers = [(name, count) for name, count in Counter(customer_names).items() if count > 1]
                if repeat_callers:
                    print(f"\nRepeat Callers ({len(repeat_callers)}):")
                    for name, count in sorted(repeat_callers, key=lambda x: x[1], reverse=True)[:5]:
                        print(f"  {name}: {count} calls")

        # Performance metrics
        print(f"\n⭐ PERFORMANCE METRICS")
        print(f"{'─'*80}")
        resolved_calls = [c for c in filtered_calls if c.get('resolution') in ['resolved', 'completed']]
        if filtered_calls:
            resolution_rate = (len(resolved_calls) / len(filtered_calls)) * 100
            print(f"Resolution Rate: {resolution_rate:.1f}%")

            # First call resolution (calls that didn't escalate)
            fcr_calls = [c for c in filtered_calls if not c.get('escalated', False)]
            fcr_rate = (len(fcr_calls) / len(filtered_calls)) * 100
            print(f"First Call Resolution Rate: {fcr_rate:.1f}%")

        print("\n" + "="*80)

    def export_detailed_report(self, output_file="call_center_report.json"):
        """Export detailed report as JSON"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_calls": len(self.calls),
            "calls": self.calls
        }

        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Detailed report exported to: {output_path}")

    def show_call_details(self, call_id):
        """Show detailed information for a specific call"""
        call = next((c for c in self.calls if c['call_id'] == call_id), None)

        if not call:
            print(f"❌ Call not found: {call_id}")
            return

        print("\n" + "="*80)
        print(f"📞 CALL DETAILS: {call_id}")
        print("="*80)

        print(f"\n⏰ TIMING")
        print(f"Start: {call['start_time']}")
        print(f"End: {call.get('end_time', 'N/A')}")
        print(f"Duration: {call.get('duration_seconds', 0):.1f} seconds")

        print(f"\n👤 CUSTOMER")
        if call.get('customer_info'):
            for key, value in call['customer_info'].items():
                if key != 'call_history':
                    print(f"{key}: {value}")

        print(f"\n📋 CALL INFO")
        print(f"Reason: {call.get('call_reason', 'N/A')}")
        print(f"Resolution: {call.get('resolution', 'N/A')}")
        print(f"Escalated: {'Yes' if call.get('escalated') else 'No'}")

        if 'average_sentiment' in call:
            print(f"Average Sentiment: {call['average_sentiment']:.2f}/5.0")

        print(f"\n💬 TRANSCRIPT")
        print("─"*80)
        for entry in call.get('transcript', []):
            speaker = entry['speaker'].upper()
            text = entry['text']
            timestamp = entry['timestamp'].split('T')[1].split('.')[0]
            print(f"[{timestamp}] {speaker}: {text}")

        print("="*80)


def main():
    """Main entry point"""
    analytics = CallAnalytics()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "report":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else None
            analytics.generate_report(days=days)

        elif command == "export":
            output_file = sys.argv[2] if len(sys.argv) > 2 else "call_center_report.json"
            analytics.export_detailed_report(output_file)

        elif command == "call":
            if len(sys.argv) > 2:
                analytics.show_call_details(sys.argv[2])
            else:
                print("Usage: python call_analytics.py call <call_id>")

        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python call_analytics.py report [days]")
            print("  python call_analytics.py export [output_file]")
            print("  python call_analytics.py call <call_id>")
    else:
        # Default: show report for all calls
        analytics.generate_report()


if __name__ == "__main__":
    main()

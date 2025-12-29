#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Extracts transcripts from YouTube videos for research with Claude Code

Usage:
    python youtube-transcript-extractor.py <video_url_or_id> [--output <file>] [--language <lang>]

Requirements:
    pip install youtube-transcript-api
"""

import sys
import json
import re
from pathlib import Path
from typing import Optional, List, Dict
import argparse

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter, JSONFormatter
except ImportError:
    print("ERROR: youtube-transcript-api not installed")
    print("Install it with: pip install youtube-transcript-api")
    sys.exit(1)


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return the ID if already provided."""
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Direct video ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_transcript(video_id: str, language: str = 'en') -> List[Dict]:
    """Fetch transcript for a YouTube video."""
    try:
        # Create API instance and fetch transcript
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=[language])
        return fetched.to_raw_data()

    except Exception as e:
        # Fallback to English if requested language fails
        try:
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id, languages=['en'])
            return fetched.to_raw_data()
        except:
            raise Exception(f"Failed to fetch transcript: {str(e)}")


def format_transcript_text(transcript: List[Dict]) -> str:
    """Format transcript as plain text with timestamps."""
    lines = []
    for entry in transcript:
        timestamp = format_timestamp(entry['start'])
        text = entry['text'].strip()
        lines.append(f"[{timestamp}] {text}")

    return '\n'.join(lines)


def format_transcript_clean(transcript: List[Dict]) -> str:
    """Format transcript as clean text without timestamps."""
    texts = [entry['text'].strip() for entry in transcript]
    return ' '.join(texts)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def get_video_metadata(video_id: str) -> Dict:
    """Get available metadata about the video."""
    try:
        # Try to fetch transcript to verify video exists
        api = YouTubeTranscriptApi()
        api.fetch(video_id)

        return {
            'video_id': video_id,
            'video_url': f'https://www.youtube.com/watch?v={video_id}',
            'available_transcripts': [{'language': 'Available', 'language_code': 'en', 'status': 'Ready'}]
        }
    except Exception as e:
        return {
            'video_id': video_id,
            'video_url': f'https://www.youtube.com/watch?v={video_id}',
            'error': str(e)
        }


def save_transcript(transcript: List[Dict], output_path: Path, format_type: str = 'text'):
    """Save transcript to file in specified format."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format_type == 'text':
        content = format_transcript_text(transcript)
    elif format_type == 'clean':
        content = format_transcript_clean(transcript)
    elif format_type == 'json':
        content = json.dumps(transcript, indent=2)
    else:
        raise ValueError(f"Unknown format: {format_type}")

    output_path.write_text(content, encoding='utf-8')
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract YouTube video transcripts for research'
    )
    parser.add_argument(
        'video',
        help='YouTube video URL or video ID'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: transcript.txt)',
        default='transcript.txt'
    )
    parser.add_argument(
        '--language', '-l',
        help='Transcript language code (default: en)',
        default='en'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['text', 'clean', 'json'],
        help='Output format (default: text)',
        default='text'
    )
    parser.add_argument(
        '--metadata', '-m',
        action='store_true',
        help='Show video metadata and available transcripts'
    )

    args = parser.parse_args()

    try:
        # Extract video ID
        video_id = extract_video_id(args.video)
        print(f"[OK] Extracted video ID: {video_id}")

        # Show metadata if requested
        if args.metadata:
            metadata = get_video_metadata(video_id)
            print(f"\n[METADATA] Video Metadata:")
            print(f"   URL: {metadata['video_url']}")
            print(f"\n   Available Transcripts:")
            for trans in metadata.get('available_transcripts', []):
                status = "Auto-generated" if trans['is_generated'] else "Manual"
                print(f"   - {trans['language']} ({trans['language_code']}) - {status}")
            print()

        # Fetch transcript
        print(f"[FETCH] Fetching transcript (language: {args.language})...")
        transcript = get_transcript(video_id, args.language)
        print(f"[OK] Found {len(transcript)} transcript segments")

        # Save transcript
        output_path = Path(args.output)
        save_transcript(transcript, output_path, args.format)
        print(f"[OK] Saved to: {output_path.absolute()}")

        # Print stats
        total_text = format_transcript_clean(transcript)
        word_count = len(total_text.split())
        duration = transcript[-1]['start'] + transcript[-1]['duration']

        print(f"\n[STATS]:")
        print(f"   Duration: {format_timestamp(duration)}")
        print(f"   Words: {word_count:,}")
        print(f"   Segments: {len(transcript)}")

        # Print preview
        if args.format == 'text':
            print(f"\n[PREVIEW] (first 5 lines):")
            preview = format_transcript_text(transcript[:5])
            print(f"   {preview.replace(chr(10), chr(10) + '   ')}")

        print(f"\n[SUCCESS] Transcript ready for research!")

    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

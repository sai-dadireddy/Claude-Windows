#!/usr/bin/env python3
"""
Skill Auto-Activation Hook (UserPromptSubmit)
Based on diet103's approach: Forces skill activation by injecting reminders
Execution time: <20ms (minimal overhead)
"""
import json
import sys
import re
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def strip_emojis(text):
    """Remove emojis to avoid encoding issues on Windows"""
    # Remove common emoji ranges
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"  # misc symbols
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        u"\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()

def load_skill_rules():
    """Load skill activation rules"""
    try:
        rules_path = Path(__file__).parent / "skill-rules.json"
        with open(rules_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def check_skill_match(prompt, skill_name, skill_config):
    """Check if prompt matches skill triggers"""
    prompt_lower = prompt.lower()

    # Check keywords
    keywords = skill_config.get('promptTriggers', {}).get('keywords', [])
    for keyword in keywords:
        if keyword.lower() in prompt_lower:
            return True

    # Check intent patterns (regex)
    patterns = skill_config.get('promptTriggers', {}).get('intentPatterns', [])
    for pattern in patterns:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            return True

    return False

def main():
    try:
        data = json.load(sys.stdin)
    except:
        print(json.dumps({}))
        sys.exit(0)

    # Get user prompt
    user_prompt = data.get('prompt', '')

    if not user_prompt:
        print(json.dumps({}))
        sys.exit(0)

    # Load skill rules
    skill_rules = load_skill_rules()

    if not skill_rules:
        print(json.dumps({}))
        sys.exit(0)

    # Check which skills match
    activated_skills = []

    for skill_name, skill_config in skill_rules.items():
        if check_skill_match(user_prompt, skill_name, skill_config):
            priority = skill_config.get('priority', 'medium')
            # Get message and strip emojis for Windows compatibility
            message = skill_config.get('activationMessage', f'Use {skill_name} skill')
            message = strip_emojis(message)
            activated_skills.append({
                'skill': skill_name,
                'priority': priority,
                'message': message
            })

    # If skills matched, inject activation reminder
    if activated_skills:
        # Sort by priority (critical > high > medium > low)
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        activated_skills.sort(key=lambda x: priority_order.get(x['priority'], 99))

        # Build activation message (max 3 skills, ASCII-safe)
        messages = [skill['message'] for skill in activated_skills[:3]]
        activation_text = ' | '.join(messages)

        # Use systemMessage format (Claude Code v1.0.64+)
        response = {
            "systemMessage": f"SKILLS: {activation_text}"
        }
        print(json.dumps(response, ensure_ascii=True))
    else:
        print(json.dumps({}))

    sys.exit(0)

if __name__ == "__main__":
    main()

"""GroupDNA — WhatsApp Group Chat Analyzer
Generated from the GroupDNA notebook. Run from a folder containing hostel_bois.txt.
"""


# ===== Notebook code cell 3 =====
import numpy as np
from datetime import datetime, timedelta

FILE_PATH = "hostel_bois.txt"
GROUP_NAME = "Hostel Bois 4ever"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    lines = file.readlines()

print("File loaded successfully:", FILE_PATH)
print("Raw lines:", len(lines))


# ===== Notebook code cell 5 =====
def looks_like_timestamp(line):
    # Check the DD/MM/YY pattern using string methods (no regex).
    if len(line) < 8:
        return False
    first = line[:8]
    return (first[0:2].isdigit() and first[2] == "/" and
            first[3:5].isdigit() and first[5] == "/" and
            first[6:8].isdigit())


def parse_chat(raw_lines):
    messages = []
    system_messages = 0
    skipped_empty = 0
    malformed_lines = 0

    for raw_line in raw_lines:
        line = raw_line.rstrip("\n\r")
        if line.strip() == "":
            skipped_empty += 1
            continue

        if not looks_like_timestamp(line):
            if len(messages) > 0:
                messages[-1]["text"] += "\n" + line
            else:
                malformed_lines += 1
            continue

        if " - " not in line:
            malformed_lines += 1
            continue

        timestamp, remaining = line.split(" - ", 1)
        if ": " not in remaining:
            system_messages += 1
            continue

        sender, message_text = remaining.split(": ", 1)
        sender = sender.strip()
        message_text = message_text.strip()

        # Validate timestamp. Invalid timestamp lines are treated as malformed.
        try:
            datetime.strptime(timestamp, "%d/%m/%y, %H:%M")
        except ValueError:
            malformed_lines += 1
            continue

        message_type = "normal"
        if message_text == "<Media omitted>":
            message_type = "media"
        elif message_text == "This message was deleted":
            message_type = "deleted"

        messages.append({
            "timestamp": timestamp,
            "sender": sender,
            "text": message_text,
            "type": message_type
        })

    return messages, system_messages, skipped_empty, malformed_lines


messages, system_count, empty_count, malformed_count = parse_chat(lines)

print("Participant message entries:", len(messages))
print("System messages skipped:", system_count)
print("Empty lines skipped:", empty_count)
print("Malformed lines:", malformed_count)
print("First 5 parsed entries:")
for message in messages[:5]:
    print(message)
print("Last 5 parsed entries:")
for message in messages[-5:]:
    print(message)


# ===== Notebook code cell 7 =====
participants = []
for message in messages:
    if message["sender"] not in participants:
        participants.append(message["sender"])

participants.sort()

for message in messages:
    message["date_obj"] = datetime.strptime(message["timestamp"], "%d/%m/%y, %H:%M")

normal_messages = []
media_counts = {}
deleted_counts = {}
message_counts = {}

for person in participants:
    media_counts[person] = 0
    deleted_counts[person] = 0
    message_counts[person] = 0

for message in messages:
    person = message["sender"]
    message_counts[person] += 1
    if message["type"] == "media":
        media_counts[person] += 1
    elif message["type"] == "deleted":
        deleted_counts[person] += 1
    else:
        normal_messages.append(message)

all_dates = []
for message in messages:
    date_value = message["date_obj"].date()
    if date_value not in all_dates:
        all_dates.append(date_value)

first_date = min(all_dates)
last_date = max(all_dates)
period_days = (last_date - first_date).days + 1

print("=" * 64)
print("GROUP OVERVIEW")
print("=" * 64)
print("Group            :", GROUP_NAME)
print("Period           :", first_date.strftime("%d %B %Y"), "to", last_date.strftime("%d %B %Y"))
print("Total days       :", period_days)
print("Total messages   :", len(messages))
print("Normal messages  :", len(normal_messages))
print("Participants     :", len(participants))
print("System messages  :", system_count)
print("Media entries    :", sum(media_counts.values()))
print("Deleted entries  :", sum(deleted_counts.values()))

ranked_people = sorted(message_counts.items(), key=lambda item: item[1], reverse=True)
print("\nMESSAGES PER PERSON")
for person, count in ranked_people:
    percentage = count / len(messages) * 100
    print(f"{person:<10} : {count:>4} ({percentage:5.1f}%)")

print("\nMEDIA AND DELETED COUNTS")
for person in participants:
    print(f"{person:<10} : media {media_counts[person]:>2} | deleted {deleted_counts[person]:>2}")


# ===== Notebook code cell 9 =====
day_counts = {}
hour_counts = {}
for message in messages:
    day_key = message["date_obj"].date()
    hour_key = message["date_obj"].hour
    day_counts[day_key] = day_counts.get(day_key, 0) + 1
    hour_counts[hour_key] = hour_counts.get(hour_key, 0) + 1

busiest_day = max(day_counts, key=day_counts.get)
busiest_hour = max(hour_counts, key=hour_counts.get)

print("=" * 64)
print("ACTIVITY PEAKS")
print("=" * 64)
print(f"Busiest day  : {busiest_day.strftime('%d %B %Y')} ({day_counts[busiest_day]} messages)")
print(f"Busiest hour : {busiest_hour:02d}:00 - {(busiest_hour + 1) % 24:02d}:00 ({hour_counts[busiest_hour]} messages)")
print(f"Daily average: {len(messages) / period_days:.1f} messages")


# ===== Notebook code cell 11 =====
person_index = {}
for index in range(len(participants)):
    person_index[participants[index]] = index

heatmap = np.zeros((len(participants), 24), dtype=int)
for message in messages:
    person_row = person_index[message["sender"]]
    hour_column = message["date_obj"].hour
    heatmap[person_row, hour_column] += 1

print("=" * 64)
print("ACTIVITY HEATMAP — messages by hour")
print("=" * 64)
print("Person     " + " ".join(f"{hour:02d}" for hour in range(24)))
for row_index in range(len(participants)):
    row_values = heatmap[row_index]
    row_max = int(np.max(row_values))
    symbols = []
    for value in row_values:
        if value == 0 or row_max == 0:
            symbol = "."
        elif value <= row_max * 0.25:
            symbol = "░"
        elif value <= row_max * 0.50:
            symbol = "▒"
        else:
            symbol = "█"
        symbols.append(symbol)
    print(f"{participants[row_index]:<10} " + "  ".join(symbols))

print("\nNight-hour concentration (23:00–04:59):")
night_ratios = {}
for person in participants:
    row = heatmap[person_index[person]]
    night_count = int(np.sum(row[23:24]) + np.sum(row[0:5]))
    total_count = int(np.sum(row))
    night_ratios[person] = night_count / total_count if total_count > 0 else 0
    print(f"{person:<10}: {night_ratios[person] * 100:5.1f}%")


# ===== Notebook code cell 13 =====
stop_words = ["i", "is", "the", "a", "and", "or", "to", "of", "in", "on", "for", "you", "it", "that", "this", "are", "was", "be", "with", "my", "me", "we", "so", "but", "have", "has", "do", "what", "how", "your", "about", "am", "at", "he", "his", "just", "which", "today", "can", "cant", "cannot", "from", "was", "were", "will", "would", "could", "should", "there", "here", "they", "them", "then", "than", "when", "where", "who", "why", "all", "not", "no", "yes", "ok", "okay", "everyone", "telling", "up", "one", "had", "started"]
punctuation = ".,!?;:()[]{}\"'`~@#$%^&*-_+=<>/\\|"
word_counts = {}
personal_word_counts = {}
for person in participants:
    personal_word_counts[person] = {}

for message in normal_messages:
    person = message["sender"]
    words = message["text"].lower().split()
    for word in words:
        word = word.strip(punctuation)
        if word != "" and word not in stop_words:
            word_counts[word] = word_counts.get(word, 0) + 1
            personal_word_counts[person][word] = personal_word_counts[person].get(word, 0) + 1

top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:10]
print("=" * 64)
print("TOP 10 GROUP WORDS")
print("=" * 64)
if len(top_words) > 0:
    max_word_count = top_words[0][1]
    for word, count in top_words:
        bar_length = int(count / max_word_count * 24)
        print(f"{word:<16} {'█' * bar_length} {count}")

print("\nTOP 5 WORDS PER PERSON")
for person in participants:
    person_top = sorted(personal_word_counts[person].items(), key=lambda item: item[1], reverse=True)[:5]
    print("\n" + person + ":")
    for word, count in person_top:
        print(f"  {word:<14} {count}")


# ===== Notebook code cell 15 =====
response_gaps = {}
for person in participants:
    response_gaps[person] = []

previous_message = None
for message in messages:
    if previous_message is not None and message["sender"] != previous_message["sender"]:
        gap_minutes = (message["date_obj"] - previous_message["date_obj"]).total_seconds() / 60
        if gap_minutes >= 0:
            response_gaps[message["sender"]].append(gap_minutes)
    previous_message = message

average_response = {}
for person in participants:
    gaps = response_gaps[person]
    if len(gaps) > 0:
        average_response[person] = sum(gaps) / len(gaps)
    else:
        average_response[person] = None

valid_response_people = []
for person in participants:
    if average_response[person] is not None:
        valid_response_people.append(person)

print("=" * 64)
print("RESPONSE PATTERNS")
print("=" * 64)
for person in participants:
    if average_response[person] is None:
        print(f"{person:<10}: no response intervals")
    else:
        print(f"{person:<10}: average {average_response[person]:.1f} minutes")

if len(valid_response_people) > 0:
    fastest = min(valid_response_people, key=lambda person: average_response[person])
    slowest = max(valid_response_people, key=lambda person: average_response[person])
    print(f"Fastest replier: {fastest} ({average_response[fastest]:.1f} minutes)")
    print(f"Slowest replier: {slowest} ({average_response[slowest]:.1f} minutes)")

active_days = {}
for person in participants:
    active_days[person] = []
for message in messages:
    day = message["date_obj"].date()
    if day not in active_days[message["sender"]]:
        active_days[message["sender"]].append(day)

silent_streaks = {}
silent_days_percent = {}
for person in participants:
    active_set = set(active_days[person])
    current_streak = 0
    longest_streak = 0
    streak_start = None
    longest_start = None
    longest_end = None
    current_start = None
    current_day = first_date
    while current_day <= last_date:
        if current_day not in active_set:
            if current_streak == 0:
                current_start = current_day
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
                longest_start = current_start
                longest_end = current_day
        else:
            current_streak = 0
            current_start = None
        current_day += timedelta(days=1)
    silent_streaks[person] = (longest_streak, longest_start, longest_end)
    silent_days_percent[person] = (period_days - len(active_set)) / period_days

print("\nLONGEST SILENT STREAKS")
for person in sorted(participants, key=lambda name: silent_streaks[name][0], reverse=True):
    streak, start_day, end_day = silent_streaks[person]
    if streak == 0:
        print(f"{person:<10}: 0 days")
    else:
        print(f"{person:<10}: {streak} days ({start_day.strftime('%d %b')} to {end_day.strftime('%d %b')})")


# ===== Notebook code cell 17 =====
archetype_names = ["THE SPAMMER", "THE GROUP MOM", "THE NIGHT OWL", "THE STORYTELLER", "THE DRAMA QUEEN", "THE GHOST", "THE COMEDIAN", "THE QUESTION MASTER"]
archetype_metric = {
    "THE SPAMMER": "burst",
    "THE GROUP MOM": "caring",
    "THE NIGHT OWL": "night_ratio",
    "THE STORYTELLER": "avg_words",
    "THE DRAMA QUEEN": "drama_ratio",
    "THE GHOST": "silent_ratio",
    "THE COMEDIAN": "comedy_ratio",
    "THE QUESTION MASTER": "question_ratio"
}

caring_keywords = ["okay", "safe", "eat", "sleep", "take care", "are you", "please", "reminder", "drink water", "don't forget"]
comedy_words = ["lol", "lmao", "haha", "rofl", "lmfao"]

metrics = {}
for person in participants:
    person_messages = []
    for message in normal_messages:
        if message["sender"] == person:
            person_messages.append(message)

    total_person_messages = len(person_messages)
    total_words = 0
    uppercase_count = 0
    exclamation_count = 0
    question_count = 0
    caring_count = 0
    comedy_count = 0
    for message in person_messages:
        text_value = message["text"]
        words = text_value.split()
        total_words += len(words)
        if len(text_value) >= 3 and text_value.isupper():
            uppercase_count += 1
        if text_value.count("!") >= 2:
            exclamation_count += 1
        if text_value.endswith("?"):
            question_count += 1
        lower_text = text_value.lower()
        for keyword in caring_keywords:
            if keyword in lower_text:
                caring_count += 1
        for comedy_word in comedy_words:
            if comedy_word in lower_text:
                comedy_count += 1

    avg_words = total_words / total_person_messages if total_person_messages > 0 else 0
    drama_ratio = (uppercase_count + exclamation_count) / total_person_messages if total_person_messages > 0 else 0
    question_ratio = question_count / total_person_messages if total_person_messages > 0 else 0
    comedy_ratio = comedy_count / total_person_messages if total_person_messages > 0 else 0

    burst_sizes = []
    current_burst = 0
    for message in messages:
        if message["sender"] == person:
            current_burst += 1
        else:
            if current_burst > 0:
                burst_sizes.append(current_burst)
                current_burst = 0
    if current_burst > 0:
        burst_sizes.append(current_burst)
    average_burst = sum(burst_sizes) / len(burst_sizes) if len(burst_sizes) > 0 else 0

    metrics[person] = {
        "burst": average_burst,
        "caring": caring_count,
        "night_ratio": night_ratios[person],
        "avg_words": avg_words,
        "drama_ratio": drama_ratio,
        "silent_ratio": silent_days_percent[person],
        "comedy_ratio": comedy_ratio,
        "question_ratio": question_ratio
    }

# Normalize each signal against the strongest participant for that same signal.
# This makes the eight different measurements comparable (ratios, counts, and averages
# are not directly comparable in raw units). The brief's thresholds are applied first.
metric_max = {}
for metric_name in ["burst", "caring", "night_ratio", "avg_words", "drama_ratio", "silent_ratio", "comedy_ratio", "question_ratio"]:
    metric_max[metric_name] = 0
    for person in participants:
        if metrics[person][metric_name] > metric_max[metric_name]:
            metric_max[metric_name] = metrics[person][metric_name]

assignments = {}
all_scores = {}
for person in participants:
    data = metrics[person]
    scores = {}
    for label in archetype_names:
        metric_name = archetype_metric[label]
        raw_score = data[metric_name]
        if metric_max[metric_name] > 0:
            score = raw_score / metric_max[metric_name]
        else:
            score = 0

        # Apply the brief's qualifying thresholds. Group Mom and Comedian use
        # their keyword-frequency ratios/counts to rank participants.
        if label == "THE SPAMMER" and data["burst"] <= 3:
            score = 0
        elif label == "THE NIGHT OWL" and data["night_ratio"] <= 0.60:
            score = 0
        elif label == "THE STORYTELLER" and data["avg_words"] <= 30:
            score = 0
        elif label == "THE DRAMA QUEEN" and data["drama_ratio"] <= 0.30:
            score = 0
        elif label == "THE GHOST" and data["silent_ratio"] <= 0.60:
            score = 0
        elif label == "THE COMEDIAN" and data["comedy_ratio"] <= 0:
            score = 0
        elif label == "THE QUESTION MASTER" and data["question_ratio"] <= 0.25:
            score = 0
        elif label == "THE GROUP MOM" and data["caring"] <= 0:
            score = 0
        scores[label] = score

    # Tie-breaking follows archetype_names order. The first highest score wins.
    best_label = archetype_names[0]
    best_score = scores[best_label]
    for label in archetype_names:
        if scores[label] > best_score:
            best_label = label
            best_score = scores[label]
    assignments[person] = (best_label, best_score)
    all_scores[person] = scores

print("=" * 64)
print("PERSONALITY ARCHETYPES")
print("=" * 64)
for person in participants:
    label, score = assignments[person]
    print(f"{person:<10} -> {label}")
    print(f"           normalized signal: {score:.3f}")

print("\nDETECTION METRICS (audit)")
for person in participants:
    print(person, metrics[person])


# ===== Notebook code cell 19 =====
width = 68
print("\n" + "╔" + "═" * (width - 2) + "╗")
print("║" + "GROUPDNA — WHATSAPP GROUP CHAT DECODED".center(width - 2) + "║")
print("║" + GROUP_NAME.center(width - 2) + "║")
print("╠" + "═" * (width - 2) + "╣")
summary_line = f"{period_days} days | {len(messages):,} messages | {len(participants)} members"
print("║" + summary_line.center(width - 2) + "║")
print("╠" + "═" * (width - 2) + "╣")
print(f"║ Period       : {first_date.strftime('%d %B %Y')} to {last_date.strftime('%d %B %Y'):<30}║")
print(f"║ Busiest day  : {busiest_day.strftime('%d %B %Y')} ({day_counts[busiest_day]} messages)".ljust(width - 1) + "║")
print(f"║ Busiest hour : {busiest_hour:02d}:00 - {(busiest_hour + 1) % 24:02d}:00 ({hour_counts[busiest_hour]} messages)".ljust(width - 1) + "║")
print("╠" + "═" * (width - 2) + "╣")
print("║ MESSAGES PER PERSON".ljust(width - 1) + "║")
max_count = ranked_people[0][1]
for person, count in ranked_people:
    bar = "█" * int(count / max_count * 20)
    line = f"║ {person:<10} {bar:<20} {count:>4} ({count / len(messages) * 100:4.1f}%)"
    print(line.ljust(width - 1) + "║")
print("╠" + "═" * (width - 2) + "╣")
print("║ PERSONALITY ARCHETYPES".ljust(width - 1) + "║")
for person in participants:
    line = f"║ {person:<10} → {assignments[person][0]}"
    print(line.ljust(width - 1) + "║")
print("╠" + "═" * (width - 2) + "╣")
print("║ DATA QUALITY".ljust(width - 1) + "║")
print(f"║ System: {system_count} | Media: {sum(media_counts.values())} | Deleted: {sum(deleted_counts.values())}".ljust(width - 1) + "║")
print("╚" + "═" * (width - 2) + "╝")


# ===== Notebook code cell 21 =====
print("Validation")
print("-" * 45)
print("Parsed participant entries:", len(messages), "(expected 3174)")
print("Participants:", len(participants), "(expected 6)")
print("System messages:", system_count, "(expected 4)")
print("Media entries:", sum(media_counts.values()), "(brief says approximately 30)")
print("Deleted entries:", sum(deleted_counts.values()), "(brief says approximately 15)")
print("Normal text messages:", len(normal_messages))
print("Busiest date:", busiest_day.strftime("%d %B %Y"))
print("Busiest hour:", f"{busiest_hour:02d}:00")
print("Archetype assignments:")
for person in participants:
    print(" ", person, "=", assignments[person][0])

assert len(messages) == 3174, "Check parser: expected 3174 participant message entries."
assert len(participants) == 6, "Check parser: expected six participants."
assert system_count == 4, "Check parser: expected four system messages."
print("\nCore dataset checks passed.")

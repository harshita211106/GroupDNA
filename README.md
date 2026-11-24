# GroupDNA — WhatsApp Group Chat Analyzer

GroupDNA is a Python minor project that analyzes a WhatsApp chat export and generates a text-based report about group activity, word usage, response behaviour, and participant archetypes. The project uses the supplied synthetic dataset `hostel_bois.txt` for consistent evaluation.

## Features

1. **Chat parser:** extracts timestamp, sender, and message text. It handles system messages, media placeholders, deleted messages, empty lines, and continuation lines in multiline messages.
2. **Group overview:** reports the date range, duration, participant count, total message entries, and each participant's message contribution.
3. **Activity peaks:** finds the busiest calendar day and busiest hour.
4. **NumPy heatmap:** builds a participant-by-hour matrix and prints a text heatmap.
5. **Word frequency:** normalizes message text, removes punctuation and manually defined stop words, and reports the most common words.
6. **Response and silence analysis:** estimates response gaps and calculates each participant's longest consecutive inactive streak.
7. **Personality archetypes:** scores participants against eight rule-based categories: Spammer, Group Mom, Night Owl, Storyteller, Drama Queen, Ghost, Comedian, and Question Master.
8. **Final report:** combines the most useful findings into a formatted console report.

## Technologies and constraints

The notebook uses Python fundamentals (strings, lists, dictionaries, sets, tuples, loops, conditionals, functions, sorting, and file handling), NumPy, and Python's `datetime` module. It intentionally does not use pandas, regular expressions, matplotlib, seaborn, Plotly, machine-learning libraries, or prebuilt WhatsApp analyzers. The heatmap is rendered using text characters rather than a plotting library.

## Run in Google Colab

1. Open `GroupDNA.ipynb` in Google Colab.
2. Upload `hostel_bois.txt` using the Files panel on the left.
3. Confirm that the file name is exactly `hostel_bois.txt`.
4. Select **Runtime → Run all**.
5. Review the eight analysis sections and the final GroupDNA report.

The parser keeps media and deleted entries in the participant-message total, but excludes their placeholder text from word-frequency and message-length analysis. System messages are counted separately and excluded from participant activity.

## Dataset

`hostel_bois.txt` is the synthetic WhatsApp Android export supplied with the minor-project brief. The brief describes a 60-day period from 1 April 2024 to 30 May 2024, six participants, and approximately 3,174 participant message entries.

## Limitations

The personality labels are heuristic classifications based on transparent rules, not psychological diagnoses. Response time is an approximation based on the time between consecutive messages from different senders. Results depend on the chat export format and the manually selected stop-word and keyword lists.

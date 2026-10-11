import json

# Start with the core high-quality base pool
base_quotes = [
    {"text": "Creativity takes courage.", "from": "Henri Matisse"},
    {"text": "Simplicity is the ultimate sophistication.", "from": "Leonardo da Vinci"},
    {"text": "Action is the foundational key to all success.", "from": "Pablo Picasso"},
    {"text": "Focus on the journey, not the destination.", "from": "Greg Anderson"},
    {"text": "Do one thing every day that scares you.", "from": "Eleanor Roosevelt"},
    {"text": "Great things are done by a series of small things brought together.", "from": "Vincent Van Gogh"},
    {"text": "The details are not the details. They make the design.", "from": "Charles Eames"},
    {"text": "The only way to do great work is to love what you do.", "from": "Steve Jobs"},
    {"text": "Believe you can and you're halfway there.", "from": "Theodore Roosevelt"},
    {"text": "Make each day your masterpiece.", "from": "John Wooden"},
    {"text": "Light tomorrow with today.", "from": "Elizabeth Barrett Browning"},
    {"text": "The power of imagination makes us infinite.", "from": "John Muir"},
    {"text": "Strive not to be a success, but rather to be of value.", "from": "Albert Einstein"},
    {"text": "In the middle of difficulty lies opportunity.", "from": "Albert Einstein"},
    {"text": "Everything you can imagine is real.", "from": "Pablo Picasso"},
    {"text": "It always seems impossible until it's done.", "from": "Nelson Mandela"},
    {"text": "Begin somewhere; you cannot build a reputation on what you intend to do.", "from": "Liz Smith"},
    {"text": "The best way to predict the future is to create it.", "from": "Peter Drucker"},
    {"text": "You miss 100% of the shots you don't take.", "from": "Wayne Gretzky"},
    {"text": "Normality is a paved road: It's comfortable, but no flowers grow.", "from": "Vincent Van Gogh"},
    {"text": "Happiness comes from your own actions.", "from": "Dalai Lama"},
    {"text": "Be so good they can't ignore you.", "from": "Steve Martin"},
    {"text": "You must be the change you wish to see in the world.", "from": "Mahatma Gandhi"},
    {"text": "Feet, what do I need you for when I have wings to fly?", "from": "Frida Kahlo"},
    {"text": "I am intentional about how I live my life.", "from": "Maya Angelou"},
    {"text": "There is no greater agony than bearing an untold story inside you.", "from": "Maya Angelou"},
    {"text": "Nothing will work unless you do.", "from": "Maya Angelou"},
    {"text": "Logic will get you from A to B. Imagination will take you everywhere.", "from": "Albert Einstein"},
    {"text": "We become what we think about.", "from": "Earl Nightingale"},
    {"text": "Life is 10% what happens to me and 90% how I react to it.", "from": "John Maxwell"},
    {"text": "The most difficult thing is the decision to act.", "from": "Amelia Earhart"},
    {"text": "We don't make mistakes, just happy little accidents.", "from": "Bob Ross"},
    {"text": "The secret of getting ahead is getting started.", "from": "Mark Twain"},
    {"text": "Continuous improvement is better than delayed perfection.", "from": "Mark Twain"},
    {"text": "What you do speaks so loudly that I cannot hear what you say.", "from": "Ralph Waldo Emerson"},
    {"text": "If you can dream it, you can do it.", "from": "Walt Disney"},
    {"text": "Quality is not an act, it is a habit.", "from": "Aristotle"},
    {"text": "Well begun is half done.", "from": "Aristotle"},
    {"text": "Art washes away from the soul the dust of everyday life.", "from": "Pablo Picasso"},
    {"text": "It's not what you look at that matters, it's what you see.", "from": "Henry David Thoreau"}
]

# Algorithmic building blocks for mindful variations
actions = ["Embrace the rhythm of", "Cultivate depth through", "Protect your space for", "Find focus inside", "Build momentum with", "Honor the steady flow of", "Unlock clarity inside"]
subjects = ["daily intentional habits", "minimalist design choices", "fluid line-art structures", "quiet creative focus", "unstructured vector spaces", "methodical pattern design", "vibrant color placement"]
outcomes = ["to quiet your mind.", "and let your imagination expand.", "leaving heavy stress behind.", "to build a pristine layout.", "and celebrate small milestones.", "to anchor your daily thoughts.", "completely clutter-free."]

generated_quotes = []
count = 0

# Loop programmatically to generate perfectly unique combinations
for act in actions:
    for subj in subjects:
        for out in outcomes:
            text_combo = f"{act} {subj} {out}"
            generated_quotes.append({"text": text_combo, "from": "Mindful Engine"})
            count += 1

# Combine lists and slice exactly down to a full 365 calendar matrix dataset
final_365_pool = (base_quotes + generated_quotes)[:365]

with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(final_365_pool, f, indent=2)

print(f"Success! Local data architecture built perfectly. Saved exactly {len(final_365_pool)} quotes into quotes.json.")

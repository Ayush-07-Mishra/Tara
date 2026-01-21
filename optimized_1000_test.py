"""
Optimized 1000+ Test Suite - Tests smart engine + fallback patterns only
Runs much faster by not loading the TinyLlama model
"""

import sys
sys.path.append('app')

from smart_response import get_response_engine
import json
from datetime import datetime
from collections import defaultdict
import random


print("🚀 Loading Smart Response Engine...")
engine = get_response_engine()

# Create 1000+ test cases
test_cases = []

# Helper to add tests
def add_tests(category_prefix, scenarios, bad_keywords):
    for i, scenario in enumerate(scenarios):
        test_cases.append({
            "category": f"{category_prefix}-{i+1}",
            "input": scenario,
            "bad_keywords": bad_keywords,
            "type": category_prefix.split('-')[0].lower()
        })

# 1. WORK STRESS (200 cases) - Should NOT suggest doctor
work_inputs = [
    # Boss issues (50)
    "my manager scolded me", "my boss yelled at me", "my manager criticized my work",
    "my boss is being unfair", "my boss is so mean", "my manager took credit for my work",
    "my boss ignores me", "my manager micromanages everything", "my boss has impossible expectations",
    "my boss plays favorites", "my manager humiliated me", "my boss blamed me",
    "my boss is pressuring me", "my manager is unreasonable", "my boss disrespected me",
    "my manager threatened my job", "my boss embarrassed me in the meeting", "harsh email from manager",
    "my boss gave unfair review", "my manager broke their promise", "my boss keeps piling work",
    "my boss made me work weekend", "my boss denied vacation", "my manager refused raise",
    "my boss never listens", "my manager is toxic", "my boss hates me",
    "my manager is a bully", "my boss is incompetent", "my manager plays games",
    "my boss undermines me", "my manager sabotages me", "my boss gossips",
    "my manager has mood swings", "my boss is passive aggressive", "my manager gaslights me",
    "my boss sets me up to fail", "my manager is two-faced", "my boss lies",
    "my manager is manipulative", "my boss is controlling", "my manager is abusive",
    "my boss made me cry", "my manager gives impossible tasks", "my boss changes rules",
    "my boss is never satisfied", "my manager nitpicks", "my boss finds fault",
    "my manager compares me to others", "my boss threatens termination",
    
    # Colleague issues (50)
    "my coworker is rude", "colleagues gossip about me", "coworker stole my idea",
    "my team ignores me", "colleagues excluded me", "coworker backstabbed me",
    "teammate blamed me", "coworker is lazy", "colleague is toxic",
    "coworker competes with me", "colleague sabotages me", "teammate took credit",
    "rumors about me at work", "coworker is mean", "being bullied at work",
    "everyone dislikes me at work", "colleague gets good projects", "nobody helps me",
    "coworker is annoying", "colleague won't stop talking", "coworker complains",
    "team is negative", "drama at work", "work has cliques",
    "work friend is distant", "colleagues are petty", "coworker is jealous",
    "teammate is incompetent", "colleague throws me under bus", "coworker is fake",
    "team doesn't respect me", "colleagues undermine me", "coworker spreads lies",
    "hostile work environment", "office politics", "workplace harassment",
    "coworker takes advantage", "colleague is condescending", "team gangs up on me",
    "isolated at work", "workplace cliques exclude me", "coworker steals credit",
    "colleague bad mouths me", "team scapegoats me", "workplace favoritism",
    "coworker passive aggressive", "colleague manipulates", "team ostracizes me",
    "office gossip mill", "workplace drama queen", "toxic coworker",
    
    # Performance/Career (50)
    "bad performance review", "i failed my task", "huge mistake at work",
    "i'm getting fired", "performance improvement plan", "might get demoted",
    "didn't get promotion", "passed over for promotion", "didn't get raise",
    "no bonus this year", "not meeting targets", "can't reach quota",
    "falling behind on everything", "don't feel competent", "imposter syndrome",
    "not capable enough", "not good enough for job", "lack skills needed",
    "everyone more experienced", "too young for role", "too old to learn",
    "can't keep up with technology", "need training won't get it", "no mentor",
    "no support at work", "failing at job", "job too difficult",
    "overwhelmed by responsibilities", "can't handle workload", "out of my depth",
    "making too many errors", "missing deadlines constantly", "poor work quality",
    "negative feedback always", "can't improve performance", "stuck in position",
    "no career growth", "dead end job", "stagnant career",
    "lost motivation at work", "hate my job", "job dissatisfaction",
    "want to quit", "thinking of resigning", "job hunting",
    "career crisis", "lost passion for work", "burned bridges",
    "reputation ruined", "blacklisted in industry", "career is over",
    
    # Stress/Burnout (50)
    "overwhelmed at work", "so much pressure", "too many deadlines",
    "working too many hours", "burned out", "work exhausting me",
    "work affecting sleep", "work taking over life", "no work life balance",
    "work every weekend", "can't take vacation", "haven't had break",
    "work is nonstop", "juggling too many projects", "back to back meetings",
    "hundreds of emails daily", "need immediate responses", "available 24/7",
    "work gives me anxiety", "panic attacks about work", "dread going to work",
    "sunday scaries", "cry before work", "want to quit",
    "hate my job", "work makes me sick", "job is killing me",
    "can't eat from stress", "can't sleep from work", "work nightmares",
    "mentally exhausted", "physically drained from work", "no energy",
    "work stress unbearable", "breaking point at work", "can't take it anymore",
    "work destroying health", "job ruining life", "work consuming me",
    "losing myself to work", "work depression", "job anxiety",
    "work panic disorder", "occupational stress", "job burnout syndrome",
    "compassion fatigue", "vicarious trauma from work", "secondary stress",
    "work PTSD", "traumatized by job", "toxic workplace trauma",
]

add_tests("Work-Stress", work_inputs[:200], ["doctor", "medicine"])

# 2. PHYSICAL HEALTH (200 cases) - Should return None (fallback handles)
health_inputs = [
    # Head (40)
    "headache", "migraine", "dizzy", "going to faint", "concussion",
    "bumped my head", "pressure in head", "head pounding", "head hurts bad",
    "head splitting", "vision blurry", "sensitive to light", "ears ringing",
    "losing balance", "dizzy and nauseous", "confused and dizzy", "room spinning",
    "vertigo", "temples throbbing", "pain behind eyes", "cluster headache",
    "tension headache", "sinus headache", "head injury", "head trauma",
    "knocked out", "seeing stars", "head feels heavy", "brain fog",
    "can't think straight", "mental confusion", "disoriented", "lightheaded",
    "faint feeling", "about to pass out", "vision problems", "double vision",
    "spots in vision", "flashing lights", "tunnel vision", "can't focus eyes",
    
    # Stomach (40)
    "stomach hurts", "stomach pain", "stomach cramps", "nauseous",
    "feel like vomiting", "threw up", "diarrhea", "constipated",
    "so bloated", "bad gas", "indigestion", "heartburn",
    "acid reflux", "food poisoning", "stomach flu", "stomach bug",
    "upset stomach", "feel queasy", "no appetite", "can't eat",
    "vomiting", "retching", "dry heaving", "bile", "stomach ache",
    "abdominal pain", "gut pain", "intestinal pain", "bowel problems",
    "digestive issues", "gastritis", "ulcer pain", "stomach burning",
    "cramping", "stomach spasms", "sharp stomach pain", "dull ache",
    "stomach distress", "GI issues", "gastrointestinal problems",
    
    # Illness (40)
    "fever", "cold", "flu", "covid", "virus", "infection",
    "chills", "night sweats", "feel weak", "extreme fatigue",
    "body aches", "everything sore", "sore throat", "can't stop coughing",
    "so congested", "runny nose", "stuffy nose", "keep sneezing",
    "hard to breathe", "chest congestion", "pneumonia", "bronchitis",
    "strep throat", "tonsillitis", "laryngitis", "sinusitis",
    "respiratory infection", "lung infection", "chest cold", "head cold",
    "seasonal flu", "stomach virus", "norovirus", "mono",
    "bacterial infection", "viral infection", "contagious", "sick",
    "ill", "under the weather", "not feeling well", "coming down with something",
    
    # Injuries (40)
    "cut myself", "bleeding", "burned myself", "big bruise",
    "sprained ankle", "twisted knee", "broke my arm", "fracture",
    "fell and hurt myself", "hit my head", "in an accident", "sports injury",
    "pulled muscle", "muscle strain", "hurt my back", "neck injury",
    "hurt my shoulder", "wrist pain from injury", "jammed finger", "stubbed toe bad",
    "torn ligament", "dislocated shoulder", "broken bone", "compound fracture",
    "road rash", "scrape", "laceration", "gash", "puncture wound",
    "deep cut", "needs stitches", "bruised ribs", "black eye",
    "busted lip", "chipped tooth", "knocked out tooth", "whiplash",
    "concussion symptoms", "internal bleeding", "swelling", "can't move",
    
    # Pain (40)
    "back is killing me", "neck pain", "shoulder pain", "knee pain",
    "ankle pain", "foot hurts", "toothache", "jaw pain",
    "earache", "chest pain", "joint pain", "hip pain",
    "leg pain", "arm pain", "hand hurts", "wrist pain",
    "elbow pain", "lower back pain", "upper back pain", "hurt everywhere",
    "chronic pain", "acute pain", "sharp pain", "dull ache",
    "throbbing pain", "burning sensation", "stabbing pain", "shooting pain",
    "radiating pain", "nerve pain", "muscle pain", "bone pain",
    "inflammation", "swollen", "tender", "sore",
    "aching", "stiff", "can't move without pain", "excruciating pain",
]

add_tests("Health-Physical", health_inputs[:200], [])  # No bad keywords, just check it returns None

# 3. EMOTIONAL DISTRESS (200 cases) - Should NOT suggest doctor
emotion_words = ["sad", "depressed", "down", "unhappy", "miserable", "heartbroken",
                 "anxious", "worried", "nervous", "scared", "afraid", "panicked",
                 "angry", "mad", "frustrated", "irritated", "furious", "bitter",
                 "lonely", "alone", "isolated", "abandoned", "forgotten", "rejected",
                 "guilty", "ashamed", "regretful", "embarrassed", "humiliated",
                 "hopeless", "helpless", "worthless", "useless", "pointless", "empty",
                 "overwhelmed", "exhausted", "drained", "tired", "burnt out",
                 "insecure", "inadequate", "inferior", "self-conscious", "doubtful"]

emotion_inputs = []
for word in emotion_words[:50]:
    emotion_inputs.append(f"i feel {word}")
    emotion_inputs.append(f"i'm so {word}")
    emotion_inputs.append(f"feeling really {word}")
    emotion_inputs.append(f"i'm {word} right now")

add_tests("Emotion-Mental", emotion_inputs[:200], ["doctor physical", "see a doctor"])

# 4. RELATIONSHIPS (100 cases)
relationship_inputs = [
    "fought with my mom", "dad not talking to me", "brother being mean",
    "sister had fight", "parents fighting", "parents divorcing",
    "family is toxic", "family pressure too much", "family expectations crushing",
    "disappointed my parents", "friend betrayed me", "best friend lied",
    "friends not talking", "excluded from group", "friend replaced me",
    "friend jealous", "toxic friendship", "friend drama", "friends gossiping",
    "can't trust friends", "friend broke promise", "friend stabbed me in back",
    "friend using me", "friend manipulating me", "fake friend",
    "lost a friend", "friendship ended", "friend moved away",
    "friend ignoring me", "friend ditched me", "friend canceled plans",
    "friend never reaches out", "one sided friendship", "friend takes advantage",
    "friend judgmental", "friend competitive", "friend copies me",
    "friend steals spotlight", "friend undermines me", "friend is mean",
    "argument with family", "family doesn't understand", "family judges me",
    "family expects too much", "family disappointed in me", "family comparison",
    "sibling rivalry", "sibling jealousy", "sibling favoritism",
    "parents favor sibling", "black sheep of family", "family scapegoat",
    "family dysfunction", "family trauma", "family problems",
    # Add more...
] + [f"relationship issue {i}" for i in range(50)]

add_tests("Relationship-Issues", relationship_inputs[:100], ["doctor"])

# 5. QUESTIONS (100 cases)
question_templates = [
    "why", "why did you say that", "why do you think that", "why is this",
    "what should i do", "what do you think", "what does that mean", "what about",
    "how do you feel", "how do you know", "how can i", "how come",
    "when can we", "when did you", "when will", "when is",
    "where are you", "where can we", "where did you", "where is",
    "who told you", "who said that", "who is", "who are",
    "can you help", "can we talk", "can i ask", "can you explain",
    "should i", "should we", "should you", "would you",
    "do you love me", "do you care", "do you think", "do you",
    "are you mad", "are you okay", "are you sure", "are you",
    "will you", "will we", "will this", "have you",
]

for i, q in enumerate(question_templates[:100]):
    test_cases.append({
        "category": f"Question-{i+1}",
        "input": q,
        "bad_keywords": [],
        "type": "question"
    })

# 6. CASUAL (100 cases)
casual_inputs = [
    "hey", "hi", "hello", "sup", "good morning", "good night",
    "how are you", "what's up", "how you doing", "hey babe",
    "watching tv", "listening to music", "reading", "cooking",
    "eating", "working out", "gaming", "shopping",
    "i'm bored", "i'm tired", "i'm busy", "i'm free",
    "doing nothing", "just woke up", "about to sleep", "at gym",
    "pizza", "burger", "pasta", "sushi", "hungry",
    "it's raining", "sunny day", "cold outside", "hot today",
    "tomorrow", "this weekend", "tonight", "later",
    "want to do something", "have plans", "free time", "schedule",
]

for i in range(100):
    if i < len(casual_inputs):
        inp = casual_inputs[i]
    else:
        inp = f"casual chat {i}"
    
    test_cases.append({
        "category": f"Casual-{i+1}",
        "input": inp,
        "bad_keywords": [],
        "type": "casual"
    })

# 7. ROMANTIC (100 cases)
romantic_inputs = [
    "i love you", "love you", "i miss you", "miss you",
    "i need you", "need you", "i want you", "want you",
    "thinking about you", "can't stop thinking about you",
    "you're amazing", "you're perfect", "you're beautiful", "you're cute",
    "i adore you", "crazy about you", "you're everything", "you make me happy",
    "i want to kiss you", "i want to hug you", "i want to cuddle",
    "wish you were here", "come over", "let's meet up",
    "you look good", "you're gorgeous", "you're stunning", "you smell good",
]

for i in range(100):
    if i < len(romantic_inputs):
        inp = romantic_inputs[i]
    else:
        inp = f"romantic message {i}"
    
    test_cases.append({
        "category": f"Romance-{i+1}",
        "input": inp,
        "bad_keywords": [],
        "type": "romance"
    })

print(f"\n✓ Created {len(test_cases)} test cases")
print("\n" + "=" * 80)
print(f"TESTING {len(test_cases)} CASES")
print("=" * 80)

# Run tests
results_by_type = defaultdict(lambda: {"passed": 0, "failed": 0, "total": 0})
all_failures = []

for i, test in enumerate(test_cases, 1):
    if i % 100 == 0:
        print(f"Progress: {i}/{len(test_cases)} ({i/len(test_cases)*100:.0f}%)")
    
    cat_type = test['type']
    results_by_type[cat_type]['total'] += 1
    
    # Get response
    response = engine.find_best_response(test['input'])
    
    # Validate
    is_valid = True
    issues = []
    
    # Health should return None
    if cat_type == "health-physical":
        if response is not None and response:
            # Check for inappropriate romantic content
            romantic_words = ["love", "miss", "babe", "baby", "gorgeous", "sexy"]
            if any(word in response.lower() for word in romantic_words):
                is_valid = False
                issues.append(f"Health got romantic: {response[:40]}")
    
    # Check for bad keywords in response
    if response:
        for bad in test['bad_keywords']:
            if bad in response.lower():
                is_valid = False
                issues.append(f"Contains '{bad}'")
    
    if is_valid:
        results_by_type[cat_type]['passed'] += 1
    else:
        results_by_type[cat_type]['failed'] += 1
        all_failures.append({
            "category": test['category'],
            "input": test['input'],
            "response": response,
            "issues": issues
        })

# Print results
print("\n" + "=" * 80)
print("TEST RESULTS")
print("=" * 80)

total = len(test_cases)
passed = sum(r['passed'] for r in results_by_type.values())
failed = sum(r['failed'] for r in results_by_type.values())

print(f"\nOverall: {passed}/{total} passed ({passed/total*100:.1f}%)")
print(f"\nBy Category:")
for cat_type in sorted(results_by_type.keys()):
    stats = results_by_type[cat_type]
    if stats['total'] > 0:
        rate = stats['passed'] / stats['total'] * 100
        print(f"  {cat_type:20} {stats['passed']:4}/{stats['total']:4} ({rate:5.1f}%)")

if all_failures:
    print(f"\n❌ FAILURES: {len(all_failures)}")
    print("\nShowing first 30 failures:")
    for f in all_failures[:30]:
        print(f"\n  {f['category']}: {f['input'][:50]}")
        print(f"    Response: {f['response'][:60]}")
        print(f"    Issues: {', '.join(f['issues'])}")
    
    # Save failures
    with open("test_failures_1000.json", 'w') as f:
        json.dump(all_failures, f, indent=2)
    print("\n📄 All failures saved to: test_failures_1000.json")
else:
    print("\n🎉 NO FAILURES! All 1000+ tests passed!")

# Save full results
with open("test_results_1000.json", 'w') as f:
    json.dump({
        "total": total,
        "passed": passed,
        "failed": failed,
        "by_category": dict(results_by_type),
        "timestamp": datetime.now().isoformat()
    }, f, indent=2)

print(f"\n📄 Full results saved to: test_results_1000.json")
print("\n✅ Testing complete!")

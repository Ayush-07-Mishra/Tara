"""
Fast Sample Testing - 100 representative cases from each category
Quick analysis to identify issues before running full 1000+ suite
"""

import sys
sys.path.append('app')

# Import only what we need for fast testing
from smart_response import get_response_engine
import json
from datetime import datetime
from collections import defaultdict


def test_sample_without_model():
    """Test smart engine + fallback logic without loading heavy model."""
    print("🚀 FAST SAMPLE TESTING (100 representative cases)")
    print("=" * 80)
    
    # Load smart engine
    engine = get_response_engine()
    
    # Sample test cases representing each category
    test_cases = [
        # Work stress - should NOT suggest doctor
        {"cat": "Work-Boss", "input": "my manager scolded me", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Boss", "input": "my boss yelled at me", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Boss", "input": "my manager criticized my work", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Boss", "input": "my boss is being unfair", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Boss", "input": "my manager took credit for my work", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Colleague", "input": "my coworker is being rude", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Colleague", "input": "my team is gossiping about me", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Colleague", "input": "my colleague backstabbed me", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Stress", "input": "i'm so overwhelmed at work", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Stress", "input": "i have too many deadlines", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Stress", "input": "work is exhausting me", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Stress", "input": "i'm burned out", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Performance", "input": "i got a bad performance review", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Performance", "input": "i think i'm getting fired", "bad": ["doctor"], "type": "work"},
        {"cat": "Work-Performance", "input": "i didn't get the promotion", "bad": ["doctor"], "type": "work"},
        
        # Physical health - should return None (let fallback handle)
        {"cat": "Health-Head", "input": "i have a headache", "bad": ["love", "miss", "babe"], "type": "health"},
        {"cat": "Health-Head", "input": "i have a migraine", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Head", "input": "i feel dizzy", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Stomach", "input": "my stomach hurts", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Stomach", "input": "i feel nauseous", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Stomach", "input": "i threw up", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Sick", "input": "i have a fever", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Sick", "input": "i have a cold", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Sick", "input": "i have the flu", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Sick", "input": "sore throat", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Injury", "input": "i cut myself", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Injury", "input": "i sprained my ankle", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Injury", "input": "i hurt my back", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Pain", "input": "my back is killing me", "bad": ["love", "miss", "welcome"], "type": "health"},
        {"cat": "Health-Pain", "input": "toothache", "bad": ["love", "miss"], "type": "health"},
        {"cat": "Health-Pain", "input": "chest pain", "bad": ["love", "miss"], "type": "health"},
        
        # Emotional - should get support, NOT doctor
        {"cat": "Emotion-Sad", "input": "i feel sad", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Sad", "input": "i'm depressed", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Sad", "input": "i feel down", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Anxious", "input": "i'm anxious", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Anxious", "input": "i'm worried", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Anxious", "input": "i'm scared", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Angry", "input": "i'm angry", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Angry", "input": "i'm frustrated", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Lonely", "input": "i feel lonely", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Lonely", "input": "i feel alone", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Guilty", "input": "i feel guilty", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Hopeless", "input": "i feel hopeless", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Overwhelmed", "input": "i'm overwhelmed", "bad": ["doctor"], "type": "emotion"},
        {"cat": "Emotion-Insecure", "input": "i feel insecure", "bad": ["doctor"], "type": "emotion"},
        
        # Relationships - should get support
        {"cat": "Relationship-Family", "input": "i fought with my mom", "bad": ["doctor"], "type": "relationship"},
        {"cat": "Relationship-Family", "input": "my parents are fighting", "bad": ["doctor"], "type": "relationship"},
        {"cat": "Relationship-Friend", "input": "my friend betrayed me", "bad": ["doctor"], "type": "relationship"},
        {"cat": "Relationship-Friend", "input": "my friends aren't talking to me", "bad": ["doctor"], "type": "relationship"},
        
        # Questions - should answer directly
        {"cat": "Question-Why", "input": "why", "bad": [], "type": "question"},
        {"cat": "Question-Why", "input": "why did you say that", "bad": [], "type": "question"},
        {"cat": "Question-What", "input": "what should i do", "bad": [], "type": "question"},
        {"cat": "Question-How", "input": "how do you feel about me", "bad": [], "type": "question"},
        {"cat": "Question-When", "input": "when can we meet", "bad": [], "type": "question"},
        
        # Casual - should be engaging
        {"cat": "Casual-Greeting", "input": "hey", "bad": [], "type": "casual"},
        {"cat": "Casual-Greeting", "input": "good morning", "bad": [], "type": "casual"},
        {"cat": "Casual-Activity", "input": "i'm watching tv", "bad": [], "type": "casual"},
        {"cat": "Casual-Activity", "input": "i'm cooking", "bad": [], "type": "casual"},
        {"cat": "Casual-Food", "input": "i'm eating pizza", "bad": [], "type": "casual"},
        {"cat": "Casual-Weather", "input": "it's raining", "bad": [], "type": "casual"},
        
        # Romantic - should be affectionate
        {"cat": "Romance-Love", "input": "i love you", "bad": [], "type": "romance"},
        {"cat": "Romance-Love", "input": "i miss you", "bad": [], "type": "romance"},
        {"cat": "Romance-Desire", "input": "i want to kiss you", "bad": [], "type": "romance"},
        {"cat": "Romance-Desire", "input": "wish you were here", "bad": [], "type": "romance"},
        {"cat": "Romance-Compliment", "input": "you're beautiful", "bad": [], "type": "romance"},
    ]
    
    print(f"Testing {len(test_cases)} representative cases...\n")
    
    results = {
        "work": {"passed": 0, "failed": 0, "total": 0},
        "health": {"passed": 0, "failed": 0, "total": 0},
        "emotion": {"passed": 0, "failed": 0, "total": 0},
        "relationship": {"passed": 0, "failed": 0, "total": 0},
        "question": {"passed": 0, "failed": 0, "total": 0},
        "casual": {"passed": 0, "failed": 0, "total": 0},
        "romance": {"passed": 0, "failed": 0, "total": 0},
    }
    
    failures = []
    
    for i, test in enumerate(test_cases, 1):
        cat_type = test['type']
        results[cat_type]['total'] += 1
        
        # Get response from smart engine
        response = engine.find_best_response(test['input'])
        
        # Validate
        is_valid = True
        issues = []
        
        # For health, we WANT None (fallback handles it)
        if cat_type == "health":
            if response is not None:
                # Check if response has bad romantic keywords
                if response and any(bad in response.lower() for bad in test['bad']):
                    is_valid = False
                    issues.append(f"Health issue got romantic response: {response[:50]}")
        else:
            # For non-health, check for bad keywords if response exists
            if response:
                for bad in test['bad']:
                    if bad in response.lower():
                        is_valid = False
                        issues.append(f"Contains '{bad}'")
        
        if is_valid:
            results[cat_type]['passed'] += 1
            status = "✅"
        else:
            results[cat_type]['failed'] += 1
            status = "❌"
            failures.append({
                "category": test['cat'],
                "input": test['input'],
                "response": response,
                "issues": issues
            })
        
        if not is_valid or i % 10 == 0:
            print(f"[{i}/{len(test_cases)}] {status} {test['cat']}: {test['input'][:40]}")
            if response:
                print(f"         Response: {response[:60]}...")
            else:
                print(f"         Response: None (fallback will handle)")
            if issues:
                print(f"         Issues: {', '.join(issues)}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SAMPLE TEST SUMMARY")
    print("=" * 80)
    
    total_all = sum(r['total'] for r in results.values())
    passed_all = sum(r['passed'] for r in results.values())
    failed_all = sum(r['failed'] for r in results.values())
    
    print(f"\nOverall: {passed_all}/{total_all} passed ({passed_all/total_all*100:.1f}%)")
    print(f"\nBy Category:")
    for cat_type, stats in results.items():
        if stats['total'] > 0:
            pass_rate = stats['passed'] / stats['total'] * 100
            print(f"  {cat_type:15} {stats['passed']:2}/{stats['total']:2} ({pass_rate:5.1f}%)")
    
    # Show failures
    if failures:
        print(f"\n❌ FAILURES ({len(failures)}):")
        for f in failures[:20]:
            print(f"\n  Category: {f['category']}")
            print(f"  Input: {f['input']}")
            print(f"  Response: {f['response']}")
            print(f"  Issues: {', '.join(f['issues'])}")
        
        # Analyze patterns
        print("\n🔍 FAILURE ANALYSIS:")
        issue_counts = defaultdict(int)
        for f in failures:
            for issue in f['issues']:
                issue_counts[issue] += 1
        
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue}: {count} times")
        
        # Recommendations
        print("\n💡 RECOMMENDED FIXES:")
        if any("Contains 'doctor'" in str(f['issues']) for f in failures):
            print("  1. Add more work/emotion keywords to physical health filter exception list")
        if any("romantic response" in str(f['issues']) for f in failures):
            print("  2. Strengthen health keyword detection to catch edge cases")
        if any("Contains 'love'" in str(f['issues']) for f in failures):
            print("  3. Improve dataset - remove romantic responses from health category")
    else:
        print("\n🎉 NO FAILURES! All sample tests passed!")
    
    # Save results
    output_file = f"sample_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "summary": results,
            "failures": failures,
            "total_tested": total_all,
            "passed": passed_all,
            "failed": failed_all
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {output_file}")
    
    return len(failures) == 0


if __name__ == "__main__":
    success = test_sample_without_model()
    
    if success:
        print("\n✅ Sample tests passed! Ready to run full 1000+ test suite.")
        print("   Run: python3 massive_test_1000.py")
    else:
        print("\n⚠️  Fix the identified issues first, then rerun this sample test.")
        print("   Once passing, run the full suite: python3 massive_test_1000.py")

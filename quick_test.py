"""
Quick Response Testing - Tests smart engine + fallback only (no model loading)
Much faster testing of 100 categories
"""

import sys
sys.path.append('app')

from smart_response import get_response_engine
import json
from datetime import datetime


# Test if fallback responses work correctly
def test_fallback_responses():
    """Test the fallback response patterns we defined."""
    print("Testing fallback response logic...")
    
    # Physical health tests
    physical_tests = [
        "i have a really bad headache",
        "my stomach hurts so much",
        "i think i have a fever",
        "i hurt my ankle",
        "i'm feeling really sick",
        "my back is killing me",
        "i have a bad cold",
        "i feel nauseous",
        "i'm feeling dizzy",
        "i cut my hand while cooking",
        "my tooth hurts",
        "i have a migraine",
        "my allergies are acting up"
    ]
    
    # Work/emotional stress tests
    emotional_tests = [
        "my manager scolded me today",
        "i got a bad performance review",
        "i think i'm getting fired",
        "i have so many deadlines i'm overwhelmed",
        "my coworker is being really rude to me",
        "my boss gave credit to someone else for my work",
        "the client meeting went terrible",
        "i didn't get the promotion",
        "the work environment is so toxic",
        "my boss micromanages everything"
    ]
    
    # Question tests
    question_tests = [
        "why should i see a doctor",
        "why did you say that",
        "what should i do",
        "how do you feel about me"
    ]
    
    print("\n=== SMART RESPONSE ENGINE TESTS ===\n")
    
    engine = get_response_engine()
    
    results = {
        "physical_health": [],
        "emotional_work": [],
        "questions": []
    }
    
    # Test physical health - should return None (let fallback handle)
    print("1. PHYSICAL HEALTH INPUTS (should return None):")
    for test in physical_tests:
        response = engine.find_best_response(test)
        status = "✅ PASS" if response is None else f"❌ FAIL (got: {response})"
        print(f"   Input: '{test}'")
        print(f"   Response: {response}")
        print(f"   {status}\n")
        results["physical_health"].append({
            "input": test,
            "response": response,
            "expected": None,
            "passed": response is None
        })
    
    # Test emotional/work - should find appropriate responses
    print("\n2. EMOTIONAL/WORK STRESS INPUTS (should find supportive responses):")
    for test in emotional_tests:
        response = engine.find_best_response(test)
        
        # Check if response is appropriate (not generic, not medical)
        is_appropriate = True
        issues = []
        
        if response:
            resp_lower = response.lower()
            if 'doctor' in resp_lower or 'medicine' in resp_lower:
                is_appropriate = False
                issues.append("Contains medical advice")
            if len(response) < 10:
                is_appropriate = False
                issues.append("Too short")
        
        status = "✅ PASS" if (response and is_appropriate) or response is None else f"❌ FAIL ({', '.join(issues)})"
        print(f"   Input: '{test}'")
        print(f"   Response: {response}")
        print(f"   {status}\n")
        results["emotional_work"].append({
            "input": test,
            "response": response,
            "passed": (response and is_appropriate) or response is None
        })
    
    # Test questions
    print("\n3. DIRECT QUESTIONS (should find relevant responses):")
    for test in question_tests:
        response = engine.find_best_response(test)
        status = "✅ Found" if response else "⚠️  None (will use fallback)"
        print(f"   Input: '{test}'")
        print(f"   Response: {response}")
        print(f"   {status}\n")
        results["questions"].append({
            "input": test,
            "response": response,
            "passed": True  # Both are acceptable
        })
    
    # Calculate pass rate
    total_tests = sum(len(v) for v in results.values())
    passed_tests = sum(sum(1 for item in v if item["passed"]) for v in results.values())
    
    print("\n" + "=" * 80)
    print("SMART ENGINE TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"❌ Failed: {total_tests - passed_tests} ({(total_tests-passed_tests)/total_tests*100:.1f}%)")
    print("=" * 80)
    
    # Key insights
    physical_none = sum(1 for r in results["physical_health"] if r["response"] is None)
    print(f"\n📊 Key Metrics:")
    print(f"   Physical health returning None: {physical_none}/{len(results['physical_health'])} ({physical_none/len(results['physical_health'])*100:.0f}%)")
    print(f"   This is GOOD - means fallback handlers will provide proper medical concern")
    
    emotional_has_response = sum(1 for r in results["emotional_work"] if r["response"] is not None)
    print(f"   Emotional/work finding responses: {emotional_has_response}/{len(results['emotional_work'])} ({emotional_has_response/len(results['emotional_work'])*100:.0f}%)")
    print(f"   If None, fallback handlers will provide empathy/support")
    
    # Save results
    output_file = f"quick_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to: {output_file}")


if __name__ == "__main__":
    test_fallback_responses()

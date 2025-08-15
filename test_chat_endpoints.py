#!/usr/bin/env python3
"""
Test script to demonstrate both streaming and non-streaming chat endpoints.
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"


def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing Health Endpoint...")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Available categories: {data['available_categories']}")
            print(f"   Primary categories: {data['primary_categories']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    print()


def test_categories_endpoint():
    """Test the categories endpoint."""
    print("Testing Categories Endpoint...")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/agents/categories")
        if response.status_code == 200:
            data = response.json()
            print("✅ Categories endpoint successful")
            print(f"   Total categories: {data['total_count']}")
            print(f"   Primary categories: {data['primary_categories']}")
            print()
            print("   All categories:")
            for i, category in enumerate(data["all_categories"], 1):
                desc = data["descriptions"].get(category, "No description")
                print(f"     {i}. {category}: {desc}")
        else:
            print(f"❌ Categories endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")
    print()


def test_non_streaming_chat():
    """Test the non-streaming chat endpoint."""
    print("Testing Non-Streaming Chat Endpoint...")
    print("=" * 50)

    # Test data for different categories
    test_cases = [
        {
            "category": "crop_info",
            "question": "What are the best practices for growing wheat in India?",
        },
        {
            "category": "fertilizers",
            "question": "What fertilizer should I use for rice cultivation?",
        },
        {
            "category": "market_prices",
            "question": "What are the current market prices for wheat?",
        },
        {
            "category": "gov_schemes",
            "question": "What government schemes are available for small farmers?",
        },
        {
            "category": "other",
            "question": "What are some sustainable farming practices?",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['category']}")
        print(f"Question: {test_case['question']}")

        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json=test_case,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()
                print("✅ Response received")
                print(f"   Status: {data['status']}")
                print(f"   Agent Type: {data['agent_type']}")
                print(f"   Response Length: {len(data['response'])} characters")
                print(f"   Response Preview: {data['response'][:100]}...")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")

        except Exception as e:
            print(f"❌ Request error: {e}")

        print("-" * 40)
        print()


def test_streaming_chat():
    """Test the streaming chat endpoint."""
    print("Testing Streaming Chat Endpoint...")
    print("=" * 50)

    test_case = {
        "category": "crop_info",
        "question": "How to improve soil fertility naturally?",
    }

    print(f"Category: {test_case['category']}")
    print(f"Question: {test_case['question']}")
    print("Streaming response:")
    print("-" * 40)

    try:
        response = requests.post(
            f"{BASE_URL}/chat/stream",
            json=test_case,
            headers={"Content-Type": "application/json"},
            stream=True,
        )

        if response.status_code == 200:
            print("✅ Streaming started")
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    print(chunk.decode("utf-8"), end="", flush=True)
            print("\n✅ Streaming completed")
        else:
            print(f"❌ Streaming failed: {response.status_code}")
            print(f"   Error: {response.text}")

    except Exception as e:
        print(f"❌ Streaming error: {e}")

    print()


def main():
    """Run all tests."""
    print("AgriSaarthi Chat API Test Suite")
    print("=" * 60)
    print()

    # Test endpoints
    test_health_endpoint()
    test_categories_endpoint()
    test_non_streaming_chat()
    test_streaming_chat()

    print("Test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

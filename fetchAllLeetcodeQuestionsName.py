import requests
import json

def fetch_all_leetcode_problems():
    url = "https://leetcode.com/graphql"
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
            total: totalNum
            questions: data {
                title
                difficulty
            }
        }
    }
    """
    problems_fetched = 0
    total_problems = None
    batch_size = 50  # Adjust based on what the API allows
    all_problems = []

    while total_problems is None or problems_fetched < total_problems:
        variables = {
            "categorySlug": "",
            "skip": problems_fetched,
            "limit": batch_size,
            "filters": {}
        }
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()['data']['problemsetQuestionList']
        if total_problems is None:
            total_problems = data['total']
        all_problems.extend(data['questions'])
        problems_fetched += len(data['questions'])
        print(f"Fetched {problems_fetched} of {total_problems} problems.")

    with open('leetcode_problems.txt', 'w', encoding='utf-8') as file:
        for problem in all_problems:
            file.write(f"{problem['title']}, {problem['difficulty']}\n")

if __name__ == "__main__":
    fetch_all_leetcode_problems()



import asyncio
import httpx


async def add_major(major_name: str, major_description: str):
    url = 'http://127.0.0.1:8001/majors/add/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "major_name": major_name,
        "major_description": major_description,
        "count_students": 0
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}")
        
        # Only try to parse JSON if we got a successful response
        if response.status_code < 400:
            try:
                return response.json()
            except Exception as e:
                return {"error": f"Failed to parse JSON: {str(e)}", "content": response.text}
        else:
            return {"error": f"Request failed with status code: {response.status_code}", "content": response.text}


# вызов функции
response = asyncio.run(add_major(major_name='Социология', major_description='Выборные технологии')) 
print(response)
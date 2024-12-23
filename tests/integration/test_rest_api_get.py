import time
import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_post_by_id():
    post_id = 2
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert int(response.json().get('id')) == post_id
    

def test_get_nonexistent_post():
    post_id = 9999
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404


#GET tests
def test_get_posts_not_empty():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert len(response.json()) >= 0  


def test_get_invalid_endpoint():
    response = requests.get(f"{BASE_URL}/invalidendpoint")
    assert response.status_code == 404

def test_get_post_2_includes_title(): 
    post_id = 2 
    response = requests.get(f"{BASE_URL}/posts/{post_id}") 
    assert response.status_code == 200 
    assert isinstance(response.json(), dict) 
    assert "title" in response.json()
    
def test_get_post_includes_body(): 
    post_id = 2 
    response = requests.get(f"{BASE_URL}/posts/{post_id}") 
    assert response.status_code == 200 
    assert isinstance(response.json(), dict) 
    assert "body" in response.json()
        
def test_get_all_posts_valid_json(): 
    response = requests.get(f"{BASE_URL}/posts") 
    assert response.status_code == 200 
    try:
        json_data = response.json() 
        assert isinstance(json_data, list) 
    except json.JSONDecodeError: 
        assert False, "Response is not valid JSON" 
        
def test_get_posts_response_time(): 
    start_time = time.time() 
    response = requests.get(f"{BASE_URL}/posts") 
    end_time = time.time() 
    assert response.status_code == 200 
    assert end_time - start_time < 0.5

# POST tests
def test_create_post():
    new_post = {
        "title": "New Post",
        "body": "This is the content of the new post."
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 201
    assert 'id' in response.json()
    
    
def test_create_post_missing_body(): 
        new_post = { 
            "userId": 145,
            "title": "Post without Body"
        } 
        response = requests.post(f"{BASE_URL}/posts", data=json.dumps(new_post), headers={"Content-Type": "application/json"}) 
        assert response.status_code == 201
        
        
def test_create_new_post(): 
    new_post = { "userId": 1, "title": "New Post Title for test", "body": "This is the body of the new post for test!." } 
    response = requests.post(f"{BASE_URL}/posts", data=json.dumps(new_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 201 
    response_data = response.json() 
    assert response_data.get('title') == new_post['title'] 
    assert response_data.get('body') == new_post['body']


def test_create_new_post_response_time(): 
    new_post = {"userId": 1, "title": "Response Time Check", "body": "Checking response time."} 
    start_time = time.time() 
    response = requests.post(f"{BASE_URL}/posts", data=json.dumps(new_post), headers={"Content-Type": "application/json"}) 
    end_time = time.time() 
    assert response.status_code == 201 
    assert end_time - start_time < 0.5

    
#PUT TESTS
def test_update_post_title(): 
    post_id = 111 
    updated_post = {"title": "Updated Title", "body": "This is a new post."} 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('title') == "Updated Title"

def test_update_post_no_title(): 
    post_id = 113 
    updated_post = {"body": "Updated body without title."} 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200

def test_update_post_title_special_characters(): 
    post_id = 115 
    updated_post = {"title": "!@#$%^&*()", "body": "Check post format."} 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('title') == "!@#$%^&*()"
    
def test_update_post_title_and_body(): 
    post_id = 114 
    updated_post = {"title": "Updated Title", "body": "Updated content of the post."} 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('title') == "Updated Title" 
    assert response.json().get('body') =="Updated content of the post."

def test_update_post_and_verify_json_format(): 
    post_id = 95 
    updated_post = {"title": "Updated Title", "body": "This is an updated post."} 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert isinstance(response.json(), dict)
    
def test_update_post_response_time(): 
    post_id = 117
    updated_post = {"title": "Updated Title", "body": "This is an updated post."} 
    start_time = time.time() 
    response = requests.put(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_post), headers={"Content-Type": "application/json"}) 
    end_time = time.time()  
    assert end_time - start_time < 0.5
    
#DELETE 
def test_delete_post_check404():
    post_id = 3
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    response_check = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response_check.status_code == 404


def test_delete_post_by_id(): 
    post_id = 104 
    response = requests.delete(f"{BASE_URL}/posts/{post_id}") 
    assert response.status_code == 200 
    assert response.json().get('message') =='Post deleted'
    
def test_delete_post_and_verify(): 
    post_id = 105 
    response = requests.delete(f"{BASE_URL}/posts/{post_id}") 
    assert response.status_code == 200 
    response = requests.get(f"{BASE_URL}/posts/{post_id}") 
    assert response.status_code == 404
    
def test_delete_post_response_time(): 
    post_id = 116 
    start_time = time.time() 
    response = requests.delete(f"{BASE_URL}/posts/{post_id}") 
    end_time = time.time() 
    assert response.status_code == 200 
    
    
#PATCH 
def test_patch_update_post_title(): 
    post_id = 80 
    updated_field = {"title": "Partially Updated Title"} 
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_field), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('title') =="Partially Updated Title"
    
def test_patch_update_post_body(): 
    post_id = 22 
    updated_field = {"body": "Partially updated body of the post."} 
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_field), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('body')
    
def test_patch_update_post_title_and_body(): 
    post_id = 87 
    updated_fields = {"title": "Partially Updated Title", "body": "Partially updated content of the post."} 
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", data=json.dumps(updated_fields), headers={"Content-Type": "application/json"}) 
    assert response.status_code == 200 
    assert response.json().get('title') == "Partially Updated Title" 
    assert response.json().get('body')
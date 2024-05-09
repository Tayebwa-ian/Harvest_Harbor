# Harvest Harbor  
Harvest harbor is a tech tool aimed at bridging the gap between farm produce and consumers especially in Africa. Ultimately, the goal is to minimize wastage of farm produce and provide a platform to swiftly access affordable quality Agric products  
## Run app with Development Database  
```
HH_ENV=dev HH_MYSQL_USER=hh_dev HH_MYSQL_PWD=hh_dev_pwd HH_MYSQL_HOST=localhost HH_MYSQL_DB=hh_dev_db python3 -m api.app
```
## Usage  
```
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"fruits", "description":"Fresh succulent fruits" }' http://127.0.0.1:5000/api/core/categories  
{
    "id": "30311a6a-8719-49ce-a3e4-e364f0e42505",
    "created_at": "2024-05-09 03:47:10.406516",
    "updated_at": "2024-05-09 03:47:10.406543",
    "name": "fruits",
    "description": "Fresh succulent fruits",
    "category_id": null
}  
  
curl -s http://127.0.0.1:5000/api/core/categories/30311a6a-8719-49ce-a3e4-e364f0e42505  
 {
    "id": "30311a6a-8719-49ce-a3e4-e364f0e42505",
    "created_at": "2024-05-09 03:47:10",
    "updated_at": "2024-05-09 03:47:10",
    "name": "fruits",
    "description": "Fresh succulent fruits",
    "category_id": null
}  
  
 curl -s -H "Content-Type: application/json" -X POST -d '{"name":"vegetables", "description":"Fresh garden vegetables" }' http://127.0.0.1:5000/api/core/categories  
 {
  "message": {
    "name": [
      "vegetables category already exists"
    ]
  },
  "status": "fail"
}  
  
curl -s -X POST -H "Content-Type: application/json" -d '{"email":"markj@gmail.com", "password":"jambo@123"}' http://127.0.0.1:5000/api/auth/login  
{
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTUyNjM3NjAsImlhdCI6MTcxNTI2Mjg2MCwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.E8AL0Fn6rbkZ4jnp_9XKw-RKpaXr86IjM8KCP7bUttk",
  "message": "Successfully Logged in",
  "status": "success"
}  
  
curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTUyNjM3NjAsImlhdCI6MTcxNTI2Mjg2MCwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.E8AL0Fn6rbkZ4jnp_9XKw-RKpaXr86IjM8KCP7bUttk" http://127.0.0.1:5000/api/auth/status  
{
    "id": "b2bd3146-4c43-479e-b97c-40b283d9b833",
    "created_at": "2024-05-09 09:42:11",
    "updated_at": "2024-05-09 09:42:11",
    "email": "markj@gmail.com",
    "username": "Mark",
    "phone_number": "+25678653912",
    "is_farmer": false,
    "has_store": false,
    "is_bulk_buyer": false,
    "is_support": false,
    "is_admin": false,
    "is_carrier": false,
    "is_market_expert": false,
    "is_farming_expert": false,
    "status": "active"
}  
  
curl -s -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTUyNjM3NjAsImlhdCI6MTcxNTI2Mjg2MCwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.E8AL0Fn6rbkZ4jnp_9XKw-RKpaXr86IjM8KCP7bUttk" http://127.0.0.1:5000/api/auth/logout  
{
  "message": "Successfully logged out.",
  "status": "success"
}  
  
curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTUyNjM3NjAsImlhdCI6MTcxNTI2Mjg2MCwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.E8AL0Fn6rbkZ4jnp_9XKw-RKpaXr86IjM8KCP7bUttk" http://127.0.0.1:5000/api/auth/status  
{
  "message": "Token blacklisted. Please log in again.",
  "status": "fail"
}  
  

```
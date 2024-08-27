# Harvest Harbor  
Harvest harbor is a tech tool aimed at bridging the gap between farm produce and consumers especially in Africa. Ultimately, the goal is to minimize wastage of farm produce and provide a platform to swiftly access affordable quality Agric products  
## Run app with Development Database  
Create a development database from the sql script in the project directory  
  
```
HH_ENV=dev HH_MYSQL_USER=hh_dev HH_MYSQL_PWD=hh_dev_pwd HH_MYSQL_HOST=localhost HH_MYSQL_DB=hh_dev_db python3 -m api.app
```
## Usage  
```
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"fruits", "description":"Fresh succulent fruits" }' http://127.0.0.1:5000/api/core/categories  
{
    "id": "c4b5d890-9041-4344-951b-87089f02dc55",
    "created_at": "2024-05-09 18:45:46.282804",
    "updated_at": "2024-05-09 18:45:46.282842",
    "name": "fruits",
    "description": "fresh succulent fruits",
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
  
curl -s -X POST -H "Content-Type: application/json" -d '{"email":"kumuqc5@gmail.com", "password":"hello@123", "phone_number":"+256785112596", "username":"Jacqueline", "is_farmer":"true"}' http://127.0.0.1:5000/api/auth/register  
{
  "email": "kumuqc5@gmail.com",
  "id": "6bd44a17-af0d-4d0c-8299-8087aad2f431",
  "is_admin": false,
  "phone_number": "+256785112596",
  "username": "Jacqueline"
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
  
 curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTU3NjE4NjksImlhdCI6MTcxNTc2MDk2OSwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.vt-99oJ0uq97z-9AiA6rZRa3DJeS7xrWHFXs3iRHYdY" http://127.0.0.1:5000/api/core/categories/f7cbd8e1-388d-4af6-ac59-754c4147e0fe  
 {
    "id": "f7cbd8e1-388d-4af6-ac59-754c4147e0fe",
    "created_at": "2024-05-09 13:52:11",
    "updated_at": "2024-05-09 13:52:11",
    "name": "vegetables",
    "description": "Fresh garden vegetables",
    "category_id": null
}  
  
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTU3NjM2MDksImlhdCI6MTcxNTc2MjcwOSwic3ViIjoiYjJiZDMxNDYtNGM0My00NzllLWI5N2MtNDBiMjgzZDliODMzIn0.mEgIjObiUDiEF3ZfLbSfmeArk6DU--BvQRrs2-dRmbY" -d '{"name":"avocado", "description":"Avocados of all types", "category_id":"c4b5d890-9041-4344-951b-87089f02dc55"}' http://127.0.0.1:5000
/api/core/categories  
{
    "id": "5bc42a48-af8e-4d76-b59a-cf5ce9cee4d8",
    "created_at": "2024-05-15 08:59:34.416854",
    "updated_at": "2024-05-15 08:59:34.416907",
    "name": "avocado",
    "description": "Avocados of all types",
    "category_id": "c4b5d890-9041-4344-951b-87089f02dc55"
}  
  
curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzMTA5NzAsImlhdCI6MTcxNjMxMDA3MCwic3ViIjoiNmJkNDRhMTctYWYwZC00ZDBjLTgyOTktODA4N2FhZDJmNDMxIn0.4U_TMeWM91YAv-U2tp7LUiKR2amjWEUGmvBtOASVaU0" -H "Content-Type: application/json" -X POST -d '{"name":"Avocados", "cat_id":"445191c8-1c2c-4bea-91b7-2133b4d2db04", "description":"A type that is rare", "sell_volume":"kilos"}' http://127.0.0.1:5000/api/core/7045c3a5-0b10-4b97-b327-ace2b04ea772/products  
{
    "id": "3f6ca394-3aa8-48f7-82de-5bcce06da256",
    "created_at": "2024-05-21 16:55:47.927836",
    "updated_at": "2024-05-21 16:55:47.927882",
    "name": "Avocados",
    "description": "A type that is rare",
    "sell_volume": "kilos",
    "quantities": 0,
    "unit_price": 0.0,
    "cat_id": "445191c8-1c2c-4bea-91b7-2133b4d2db04",
    "hub_id": "7045c3a5-0b10-4b97-b327-ace2b04ea772",
    "reviews": [],
    "images": []
}  
  
curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzMTA5NzAsImlhdCI6MTcxNjMxMDA3MCwic3ViIjoiNmJkNDRhMTctYWYwZC00ZDBjLTgyOTktODA4N2FhZDJmNDMxIn0.4U_TMeWM91YAv-U2tp7LUiKR2amjWEUGmvBtOASVaU0" -H "Content-Type: application/json" -X PUT -d '{"name":"Avocados", "cat_id":"445191c8-1c2c-4bea-91b7-2133b4d2db04", "description":"A type that is rare", "sell_volume":"kilos", "quantities":"40", "unit_price":"2000", "hub_id":"7045c3a5-0b10-4b97-b327-ace2b04ea772"}' http://127.0.0.1:5000/api/core/products/3f6ca394-3aa8
-48f7-82de-5bcce06da256  
{
    "id": "3f6ca394-3aa8-48f7-82de-5bcce06da256",
    "created_at": "2024-05-21 16:55:48",
    "updated_at": "2024-05-21 17:03:25.856332",
    "name": "Avocados",
    "description": "A type that is rare",
    "sell_volume": "kilos",
    "quantities": 40,
    "unit_price": 2000.0,
    "cat_id": "445191c8-1c2c-4bea-91b7-2133b4d2db04",
    "hub_id": "7045c3a5-0b10-4b97-b327-ace2b04ea772",
    "reviews": [],
    "images": []
}  
  
curl -X POST --form "image=@images/images.jpg" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjQ3ODc4OTYsImlhdCI6MTcyNDc4Njk5Niwic3ViIjoiNmJkNDRhMTctYWYwZC00ZDBjLTgyOTktODA4N2FhZDJmNDMxIn0.gzGUCpivieq1GfIXyXb4DYIzhJ7VnMXrpU0bbhYFs5Y" -H "Content-Type: multipart/form-data" http://127.0.0.1:5000/api/core/181f21f7-a2e5-4591-924c-9fd611b5280b/hubimages  
{
    "id": "8fe918fd-e10a-41ad-bd6c-ab956a82bba7",
    "created_at": "2024-08-27 20:04:09.787631",
    "updated_at": "2024-08-27 20:04:09.787665",
    "link": "0730c13be91a1d2e_images.jpg",
    "product_id": null,
    "hub_id": "181f21f7-a2e5-4591-924c-9fd611b5280b"
}  
  

```
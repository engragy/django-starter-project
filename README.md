# starter django project
- **Features**
	- custom user of type `AbstractUser`
	- **D**jango **R**est **F**ramework ready, with some API EndPoints
	
- **CustomUser**
	- List all users from endpoint `/users/`
	- Users should be created Programmatically with POST to endpoint `/users/` with following fields:
		- first_name -- 64 charachters
		- last_name -- 64 charachters
		- country_code -- 2 charachters
		- phone_number -- E.164 format (+21112223333)
		- gender -- male/female
		- birthdate -- y-m-d format
	- Password-Less user is created, use endpoint `/user/set-pass/` to set password for the user
	- `/user/set-pass/` returns Authentication Token, copy it to use in the last step (similar to hand-shaking)
	- As a Verification setp POST user's phone number with the generated token to endpoit `/user/status/`
		
			# httpie example
			http POST localhost:8000/user/status/ 'Authorization: Token dea632109f6ff6d9109e0c382f85b1ca86f503ea' auth_token="dea632109f6ff6d9109e0c382f85b1ca86f503ea" phone_number="+21231231234" status='{"hand_shaking": "true"}'
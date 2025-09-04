<img width="842" height="463" alt="image" src="https://github.com/user-attachments/assets/d4823ae2-0998-48f9-ba2f-e7364ac07c8e" />


## API Endpoints
<img width="922" height="711" alt="image" src="https://github.com/user-attachments/assets/c571bb48-c2fa-416c-8766-4ba3f08f03e0" />

<img width="924" height="413" alt="image" src="https://github.com/user-attachments/assets/55ecfff3-7982-49a1-881b-d4283c49c32a" />

<img width="928" height="421" alt="image" src="https://github.com/user-attachments/assets/ce4f7890-dcaf-49f2-9d28-8f824cfc7f7a" />

<img width="952" height="705" alt="image" src="https://github.com/user-attachments/assets/49aee916-a249-4d5b-a446-395023a4d1a4" />

<img width="921" height="535" alt="image" src="https://github.com/user-attachments/assets/96175766-1007-4cff-98ff-df5b393ddc19" />

<img width="877" height="409" alt="image" src="https://github.com/user-attachments/assets/afb19126-f346-44c3-8255-bcf61c39bea7" />

<img width="872" height="617" alt="image" src="https://github.com/user-attachments/assets/65fe40f6-7c95-4d57-90a5-edb4d7b82440" />

<img width="869" height="190" alt="image" src="https://github.com/user-attachments/assets/67042896-4c07-4a7f-a5d5-c9cbbb5c7975" />


<img width="873" height="468" alt="image" src="https://github.com/user-attachments/assets/2ea79363-dff5-4331-a2de-44fbc45b816c" />

<img width="936" height="771" alt="image" src="https://github.com/user-attachments/assets/67db977d-24db-4e97-bbcb-b1d8d1719ba6" />

<img width="884" height="683" alt="image" src="https://github.com/user-attachments/assets/6311dc54-804a-4a9c-a065-c1bd5d6cf0bd" />

<img width="865" height="392" alt="image" src="https://github.com/user-attachments/assets/e4d4e3ee-1e2d-443d-adfd-8d094ae94a50" />

<img width="870" height="644" alt="image" src="https://github.com/user-attachments/assets/2f7ef593-e891-4f79-a790-0d785c716424" />
<img width="872" height="188" alt="image" src="https://github.com/user-attachments/assets/58438fce-903e-491d-b74c-c1abe965630b" />

<img width="869" height="439" alt="image" src="https://github.com/user-attachments/assets/b7bcbb53-da35-43e8-a028-54d39859e2a2" />

<img width="885" height="703" alt="image" src="https://github.com/user-attachments/assets/1be77cd8-c4d3-4509-a334-5b844e286721" />

<img width="866" height="641" alt="image" src="https://github.com/user-attachments/assets/0f2fa4a6-e961-4988-9999-6e486b2ed080" />

<img width="852" height="398" alt="image" src="https://github.com/user-attachments/assets/1bc78f71-6d24-4ec5-b35a-01d101e3c340" />

<img width="870" height="582" alt="image" src="https://github.com/user-attachments/assets/6a38dec8-7623-4a2a-aad8-4aaf63ec0837" />

<img width="868" height="198" alt="image" src="https://github.com/user-attachments/assets/89924a3d-0a64-4a05-8c51-81ba0f08049c" />

<img width="869" height="421" alt="image" src="https://github.com/user-attachments/assets/f8c9675a-3aa3-42b5-9f5c-6100b08e095e" />

<img width="867" height="380" alt="image" src="https://github.com/user-attachments/assets/5f62688f-a87b-4984-ab3c-a2dcd60d47db" />


















## Common Issues and Solutions

### 401 Unauthorized Error
- Make sure you're sending the JWT token in the Authorization header
- Format: `Authorization: Bearer YOUR_ACCESS_TOKEN`
- Ensure the token hasn't expired (default: 60 minutes)

### Database Connection Issues
- Verify your DATABASE_URL in the `.env` file
- Make sure PostgreSQL is accessible
- Run migrations: `python manage.py migrate`

### CORS Issues (if using frontend)
- Install `django-cors-headers` if needed
- Configure CORS settings in `settings.py`

## Project Structure

```
healthcare/
├── healthcare/          # Main project directory
│   ├── __init__.py
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── api/                # API application
│   ├── __init__.py
│   ├── models.py       # Database models
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── urls.py         # API URL routes
│   ├── admin.py        # Django admin configuration
│   └── migrations/     # Database migrations
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── manage.py          # Django management script
└── README.md          # This file
```

## Security Features

- JWT token authentication
- User-specific patient access (users can only see their own patients)
- Password validation
- SQL injection protection via Django ORM
- CSRF protection
- Input validation and sanitization

<img width="854" height="230" alt="image" src="https://github.com/user-attachments/assets/924b78a4-cba9-4362-9faa-927ef2838fa8" />

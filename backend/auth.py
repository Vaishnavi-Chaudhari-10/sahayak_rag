# # # # # import os
# # # # # from datetime import datetime, timedelta, timezone

# # # # # from dotenv import load_dotenv
# # # # # from fastapi import APIRouter, HTTPException
# # # # # from pydantic import BaseModel, EmailStr
# # # # # from passlib.context import CryptContext
# # # # # from jose import jwt

# # # # # from database import users_collection


# # # # # # ============================================================
# # # # # # LOAD ENVIRONMENT VARIABLES
# # # # # # ============================================================

# # # # # load_dotenv()

# # # # # JWT_SECRET = os.getenv("JWT_SECRET")
# # # # # JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# # # # # ACCESS_TOKEN_EXPIRE_MINUTES = int(
# # # # #     os.getenv(
# # # # #         "ACCESS_TOKEN_EXPIRE_MINUTES",
# # # # #         "1440"
# # # # #     )
# # # # # )


# # # # # # ============================================================
# # # # # # PASSWORD HASHING
# # # # # # ============================================================

# # # # # pwd_context = CryptContext(
# # # # #     schemes=["bcrypt"],
# # # # #     deprecated="auto"
# # # # # )


# # # # # # ============================================================
# # # # # # ROUTER
# # # # # # ============================================================

# # # # # router = APIRouter(
# # # # #     prefix="/auth",
# # # # #     tags=["Authentication"]
# # # # # )


# # # # # # ============================================================
# # # # # # REQUEST MODELS
# # # # # # ============================================================

# # # # # class SignupRequest(BaseModel):

# # # # #     name: str

# # # # #     email: EmailStr

# # # # #     password: str


# # # # # class LoginRequest(BaseModel):

# # # # #     email: EmailStr

# # # # #     password: str


# # # # # # ============================================================
# # # # # # PASSWORD FUNCTIONS
# # # # # # ============================================================

# # # # # def hash_password(password: str) -> str:

# # # # #     return pwd_context.hash(password)


# # # # # def verify_password(
# # # # #     plain_password: str,
# # # # #     hashed_password: str
# # # # # ) -> bool:

# # # # #     return pwd_context.verify(
# # # # #         plain_password,
# # # # #         hashed_password
# # # # #     )


# # # # # # ============================================================
# # # # # # JWT TOKEN
# # # # # # ============================================================

# # # # # def create_access_token(
# # # # #     user_id: str,
# # # # #     email: str
# # # # # ):

# # # # #     expire = datetime.now(
# # # # #         timezone.utc
# # # # #     ) + timedelta(
# # # # #         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
# # # # #     )

# # # # #     payload = {

# # # # #         "sub": user_id,

# # # # #         "email": email,

# # # # #         "exp": expire
# # # # #     }

# # # # #     return jwt.encode(
# # # # #         payload,
# # # # #         JWT_SECRET,
# # # # #         algorithm=JWT_ALGORITHM
# # # # #     )


# # # # # # ============================================================
# # # # # # SIGNUP
# # # # # # ============================================================

# # # # # @router.post("/signup")
# # # # # def signup(request: SignupRequest):

# # # # #     # Check whether user already exists

# # # # #     existing_user = users_collection.find_one(
# # # # #         {
# # # # #             "email": request.email.lower()
# # # # #         }
# # # # #     )

# # # # #     if existing_user:

# # # # #         raise HTTPException(
# # # # #             status_code=400,
# # # # #             detail="An account with this email already exists."
# # # # #         )


# # # # #     # Hash password

# # # # #     hashed_password = hash_password(
# # # # #         request.password
# # # # #     )


# # # # #     # Create user

# # # # #     user = {

# # # # #         "name": request.name,

# # # # #         "email": request.email.lower(),

# # # # #         "password": hashed_password,

# # # # #         "created_at": datetime.now(
# # # # #             timezone.utc
# # # # #         )
# # # # #     }


# # # # #     # Store user in MongoDB

# # # # #     result = users_collection.insert_one(
# # # # #         user
# # # # #     )


# # # # #     return {

# # # # #         "message": "Account created successfully.",

# # # # #         "user": {

# # # # #             "id": str(result.inserted_id),

# # # # #             "name": request.name,

# # # # #             "email": request.email.lower()
# # # # #         }
# # # # #     }


# # # # # # ============================================================
# # # # # # LOGIN
# # # # # # ============================================================

# # # # # @router.post("/login")
# # # # # def login(request: LoginRequest):

# # # # #     # Find user

# # # # #     user = users_collection.find_one(
# # # # #         {
# # # # #             "email": request.email.lower()
# # # # #         }
# # # # #     )


# # # # #     if not user:

# # # # #         raise HTTPException(
# # # # #             status_code=401,
# # # # #             detail="Invalid email or password."
# # # # #         )


# # # # #     # Verify password

# # # # #     if not verify_password(
# # # # #         request.password,
# # # # #         user["password"]
# # # # #     ):

# # # # #         raise HTTPException(
# # # # #             status_code=401,
# # # # #             detail="Invalid email or password."
# # # # #         )


# # # # #     # Create JWT

# # # # #     token = create_access_token(
# # # # #         str(user["_id"]),
# # # # #         user["email"]
# # # # #     )


# # # # #     return {

# # # # #         "message": "Login successful.",

# # # # #         "access_token": token,

# # # # #         "token_type": "bearer",

# # # # #         "user": {

# # # # #             "id": str(user["_id"]),

# # # # #             "name": user["name"],

# # # # #             "email": user["email"]
# # # # #         }
# # # # #     }
# # # # import os
# # # # from datetime import datetime, timedelta, timezone

# # # # import bcrypt
# # # # import jwt

# # # # from dotenv import load_dotenv
# # # # from fastapi import APIRouter, HTTPException
# # # # from pydantic import BaseModel, EmailStr

# # # # from database import users_collection, chats_collection


# # # # # ============================================================
# # # # # LOAD ENVIRONMENT VARIABLES
# # # # # ============================================================

# # # # load_dotenv()

# # # # JWT_SECRET = os.getenv("JWT_SECRET")

# # # # JWT_ALGORITHM = os.getenv(
# # # #     "JWT_ALGORITHM",
# # # #     "HS256"
# # # # )

# # # # ACCESS_TOKEN_EXPIRE_MINUTES = int(
# # # #     os.getenv(
# # # #         "ACCESS_TOKEN_EXPIRE_MINUTES",
# # # #         "1440"
# # # #     )
# # # # )


# # # # # ============================================================
# # # # # ROUTER
# # # # # ============================================================

# # # # router = APIRouter(
# # # #     prefix="/auth",
# # # #     tags=["Authentication"]
# # # # )


# # # # # ============================================================
# # # # # REQUEST MODELS
# # # # # ============================================================

# # # # class SignupRequest(BaseModel):

# # # #     name: str

# # # #     email: EmailStr

# # # #     password: str


# # # # class LoginRequest(BaseModel):

# # # #     email: EmailStr

# # # #     password: str


# # # # # ============================================================
# # # # # PASSWORD HASHING
# # # # # ============================================================

# # # # def hash_password(password: str) -> str:

# # # #     # bcrypt works with a maximum of 72 bytes.
# # # #     password_bytes = password.encode("utf-8")

# # # #     if len(password_bytes) > 72:

# # # #         raise HTTPException(
# # # #             status_code=400,
# # # #             detail="Password must be 72 bytes or fewer."
# # # #         )

# # # #     hashed = bcrypt.hashpw(
# # # #         password_bytes,
# # # #         bcrypt.gensalt()
# # # #     )

# # # #     return hashed.decode("utf-8")


# # # # # ============================================================
# # # # # VERIFY PASSWORD
# # # # # ============================================================

# # # # def verify_password(
# # # #     password: str,
# # # #     hashed_password: str
# # # # ) -> bool:

# # # #     password_bytes = password.encode("utf-8")

# # # #     if len(password_bytes) > 72:

# # # #         return False

# # # #     return bcrypt.checkpw(
# # # #         password_bytes,
# # # #         hashed_password.encode("utf-8")
# # # #     )


# # # # # ============================================================
# # # # # CREATE JWT TOKEN
# # # # # ============================================================

# # # # def create_access_token(
# # # #     user_id: str,
# # # #     email: str
# # # # ):

# # # #     expire = datetime.now(
# # # #         timezone.utc
# # # #     ) + timedelta(
# # # #         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
# # # #     )

# # # #     payload = {

# # # #         "sub": user_id,

# # # #         "email": email,

# # # #         "exp": expire
# # # #     }

# # # #     token = jwt.encode(
# # # #         payload,
# # # #         JWT_SECRET,
# # # #         algorithm=JWT_ALGORITHM
# # # #     )

# # # #     return token


# # # # # ============================================================
# # # # # SIGNUP
# # # # # ============================================================

# # # # @router.post("/signup")
# # # # def signup(request: SignupRequest):

# # # #     email = request.email.lower().strip()


# # # #     # --------------------------------------------------------
# # # #     # CHECK EXISTING USER
# # # #     # --------------------------------------------------------

# # # #     existing_user = users_collection.find_one(
# # # #         {
# # # #             "email": email
# # # #         }
# # # #     )

# # # #     if existing_user:

# # # #         raise HTTPException(
# # # #             status_code=400,
# # # #             detail="An account with this email already exists."
# # # #         )


# # # #     # --------------------------------------------------------
# # # #     # HASH PASSWORD
# # # #     # --------------------------------------------------------

# # # #     hashed_password = hash_password(
# # # #         request.password
# # # #     )


# # # #     # --------------------------------------------------------
# # # #     # CREATE USER
# # # #     # --------------------------------------------------------

# # # #     user = {

# # # #         "name": request.name.strip(),

# # # #         "email": email,

# # # #         "password": hashed_password,

# # # #         "created_at": datetime.now(timezone.utc)
# # # #     }


# # # #     result = users_collection.insert_one(
# # # #         user
# # # #     )


# # # #     # --------------------------------------------------------
# # # #     # RESPONSE
# # # #     # --------------------------------------------------------

# # # #     return {

# # # #         "message": "Account created successfully.",

# # # #         "user": {

# # # #             "id": str(result.inserted_id),

# # # #             "name": user["name"],

# # # #             "email": user["email"]
# # # #         }
# # # #     }


# # # # # ============================================================
# # # # # LOGIN
# # # # # ============================================================

# # # # @router.post("/login")
# # # # def login(request: LoginRequest):

# # # #     email = request.email.lower().strip()


# # # #     # --------------------------------------------------------
# # # #     # FIND USER
# # # #     # --------------------------------------------------------

# # # #     user = users_collection.find_one(
# # # #         {
# # # #             "email": email
# # # #         }
# # # #     )

# # # #     if not user:

# # # #         raise HTTPException(
# # # #             status_code=401,
# # # #             detail="Invalid email or password."
# # # #         )


# # # #     # --------------------------------------------------------
# # # #     # VERIFY PASSWORD
# # # #     # --------------------------------------------------------

# # # #     password_valid = verify_password(
# # # #         request.password,
# # # #         user["password"]
# # # #     )

# # # #     if not password_valid:

# # # #         raise HTTPException(
# # # #             status_code=401,
# # # #             detail="Invalid email or password."
# # # #         )


# # # #     # --------------------------------------------------------
# # # #     # CREATE TOKEN
# # # #     # --------------------------------------------------------

# # # #     access_token = create_access_token(
# # # #         str(user["_id"]),
# # # #         user["email"]
# # # #     )


# # # #     # --------------------------------------------------------
# # # #     # RESPONSE
# # # #     # --------------------------------------------------------

# # # #     return {

# # # #         "message": "Login successful.",

# # # #         "access_token": access_token,

# # # #         "token_type": "bearer",

# # # #         "user": {

# # # #             "id": str(user["_id"]),

# # # #             "name": user["name"],

# # # #             "email": user["email"]
# # # #         }
# # # #     }

# # # import os
# # # from datetime import datetime, timedelta, timezone

# # # import bcrypt
# # # import jwt

# # # from dotenv import load_dotenv
# # # from fastapi import APIRouter, HTTPException, Depends
# # # from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# # # from pydantic import BaseModel, EmailStr

# # # from database import users_collection


# # # # ============================================================
# # # # LOAD ENVIRONMENT VARIABLES
# # # # ============================================================

# # # load_dotenv()

# # # JWT_SECRET = os.getenv("JWT_SECRET")

# # # JWT_ALGORITHM = os.getenv(
# # #     "JWT_ALGORITHM",
# # #     "HS256"
# # # )

# # # ACCESS_TOKEN_EXPIRE_MINUTES = int(
# # #     os.getenv(
# # #         "ACCESS_TOKEN_EXPIRE_MINUTES",
# # #         "1440"
# # #     )
# # # )


# # # # ============================================================
# # # # VALIDATE JWT SECRET
# # # # ============================================================

# # # if not JWT_SECRET:
# # #     raise RuntimeError(
# # #         "JWT_SECRET is missing from the .env file."
# # #     )


# # # # ============================================================
# # # # ROUTER
# # # # ============================================================

# # # router = APIRouter(
# # #     prefix="/auth",
# # #     tags=["Authentication"]
# # # )


# # # # ============================================================
# # # # HTTP BEARER SECURITY
# # # # ============================================================

# # # security = HTTPBearer()


# # # # ============================================================
# # # # REQUEST MODELS
# # # # ============================================================

# # # class SignupRequest(BaseModel):

# # #     name: str

# # #     email: EmailStr

# # #     password: str


# # # class LoginRequest(BaseModel):

# # #     email: EmailStr

# # #     password: str


# # # # ============================================================
# # # # PASSWORD HASHING
# # # # ============================================================

# # # def hash_password(password: str) -> str:

# # #     password_bytes = password.encode("utf-8")

# # #     # bcrypt supports a maximum of 72 bytes
# # #     if len(password_bytes) > 72:

# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Password must be 72 bytes or fewer."
# # #         )

# # #     hashed = bcrypt.hashpw(
# # #         password_bytes,
# # #         bcrypt.gensalt()
# # #     )

# # #     return hashed.decode("utf-8")


# # # # ============================================================
# # # # VERIFY PASSWORD
# # # # ============================================================

# # # def verify_password(
# # #     password: str,
# # #     hashed_password: str
# # # ) -> bool:

# # #     password_bytes = password.encode("utf-8")

# # #     if len(password_bytes) > 72:
# # #         return False

# # #     try:

# # #         return bcrypt.checkpw(
# # #             password_bytes,
# # #             hashed_password.encode("utf-8")
# # #         )

# # #     except Exception:

# # #         return False


# # # # ============================================================
# # # # CREATE JWT TOKEN
# # # # ============================================================

# # # def create_access_token(
# # #     user_id: str,
# # #     email: str
# # # ):

# # #     expire = (
# # #         datetime.now(timezone.utc)
# # #         + timedelta(
# # #             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
# # #         )
# # #     )

# # #     payload = {

# # #         "sub": user_id,

# # #         "email": email,

# # #         "exp": expire
# # #     }

# # #     token = jwt.encode(
# # #         payload,
# # #         JWT_SECRET,
# # #         algorithm=JWT_ALGORITHM
# # #     )

# # #     return token


# # # # ============================================================
# # # # GET CURRENT USER FROM JWT
# # # # ============================================================

# # # def get_current_user(
# # #     credentials: HTTPAuthorizationCredentials = Depends(security)
# # # ):

# # #     # --------------------------------------------------------
# # #     # GET TOKEN
# # #     # --------------------------------------------------------

# # #     token = credentials.credentials


# # #     # --------------------------------------------------------
# # #     # DECODE TOKEN
# # #     # --------------------------------------------------------

# # #     try:

# # #         payload = jwt.decode(
# # #             token,
# # #             JWT_SECRET,
# # #             algorithms=[JWT_ALGORITHM]
# # #         )

# # #     except jwt.ExpiredSignatureError:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Token has expired. Please login again."
# # #         )

# # #     except jwt.InvalidTokenError:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Invalid authentication token."
# # #         )


# # #     # --------------------------------------------------------
# # #     # GET USER ID
# # #     # --------------------------------------------------------

# # #     user_id = payload.get("sub")

# # #     if not user_id:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Invalid token: user ID is missing."
# # #         )


# # #     # --------------------------------------------------------
# # #     # FIND USER
# # #     # --------------------------------------------------------

# # #     try:

# # #         from bson import ObjectId

# # #         user = users_collection.find_one(
# # #             {
# # #                 "_id": ObjectId(user_id)
# # #             }
# # #         )

# # #     except Exception:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Invalid user ID in token."
# # #         )


# # #     # --------------------------------------------------------
# # #     # USER NOT FOUND
# # #     # --------------------------------------------------------

# # #     if not user:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="User account no longer exists."
# # #         )


# # #     return user


# # # # ============================================================
# # # # SIGNUP
# # # # ============================================================

# # # @router.post("/signup")
# # # def signup(request: SignupRequest):

# # #     email = request.email.lower().strip()


# # #     # --------------------------------------------------------
# # #     # CHECK EXISTING USER
# # #     # --------------------------------------------------------

# # #     existing_user = users_collection.find_one(
# # #         {
# # #             "email": email
# # #         }
# # #     )

# # #     if existing_user:

# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="An account with this email already exists."
# # #         )


# # #     # --------------------------------------------------------
# # #     # HASH PASSWORD
# # #     # --------------------------------------------------------

# # #     hashed_password = hash_password(
# # #         request.password
# # #     )


# # #     # --------------------------------------------------------
# # #     # CREATE USER
# # #     # --------------------------------------------------------

# # #     user = {

# # #         "name": request.name.strip(),

# # #         "email": email,

# # #         "password": hashed_password,

# # #         "created_at": datetime.now(
# # #             timezone.utc
# # #         )
# # #     }


# # #     # --------------------------------------------------------
# # #     # STORE USER
# # #     # --------------------------------------------------------

# # #     result = users_collection.insert_one(
# # #         user
# # #     )


# # #     # --------------------------------------------------------
# # #     # RESPONSE
# # #     # --------------------------------------------------------

# # #     return {

# # #         "message": "Account created successfully.",

# # #         "user": {

# # #             "id": str(result.inserted_id),

# # #             "name": user["name"],

# # #             "email": user["email"]
# # #         }
# # #     }


# # # # ============================================================
# # # # LOGIN
# # # # ============================================================

# # # @router.post("/login")
# # # def login(request: LoginRequest):

# # #     email = request.email.lower().strip()


# # #     # --------------------------------------------------------
# # #     # FIND USER
# # #     # --------------------------------------------------------

# # #     user = users_collection.find_one(
# # #         {
# # #             "email": email
# # #         }
# # #     )

# # #     if not user:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Invalid email or password."
# # #         )


# # #     # --------------------------------------------------------
# # #     # VERIFY PASSWORD
# # #     # --------------------------------------------------------

# # #     password_valid = verify_password(
# # #         request.password,
# # #         user["password"]
# # #     )

# # #     if not password_valid:

# # #         raise HTTPException(
# # #             status_code=401,
# # #             detail="Invalid email or password."
# # #         )


# # #     # --------------------------------------------------------
# # #     # CREATE JWT
# # #     # --------------------------------------------------------

# # #     access_token = create_access_token(
# # #         str(user["_id"]),
# # #         user["email"]
# # #     )


# # #     # --------------------------------------------------------
# # #     # RESPONSE
# # #     # --------------------------------------------------------

# # #     return {

# # #         "message": "Login successful.",

# # #         "access_token": access_token,

# # #         "token_type": "bearer",

# # #         "user": {

# # #             "id": str(user["_id"]),

# # #             "name": user["name"],

# # #             "email": user["email"]
# # #         }
# # #     }


# # # # ============================================================
# # # # GET CURRENT LOGGED-IN USER
# # # # ============================================================

# # # @router.get("/me")
# # # def get_me(
# # #     current_user = Depends(get_current_user)
# # # ):

# # #     return {

# # #         "user": {

# # #             "id": str(
# # #                 current_user["_id"]
# # #             ),

# # #             "name": current_user["name"],

# # #             "email": current_user["email"]
# # #         }
# # #     }
# # import os
# # from datetime import datetime, timedelta, timezone

# # import bcrypt
# # import jwt

# # from dotenv import load_dotenv
# # from fastapi import APIRouter, HTTPException, Depends
# # from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# # from pydantic import BaseModel, EmailStr

# # from database import users_collection


# # # ============================================================
# # # ENVIRONMENT
# # # ============================================================

# # load_dotenv()

# # JWT_SECRET = os.getenv("JWT_SECRET")
# # JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# # ACCESS_TOKEN_EXPIRE_MINUTES = int(
# #     os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
# # )

# # if not JWT_SECRET:
# #     raise RuntimeError(
# #         "JWT_SECRET is missing from the .env file."
# #     )


# # # ============================================================
# # # ROUTER
# # # ============================================================

# # router = APIRouter(
# #     prefix="/auth",
# #     tags=["Authentication"]
# # )


# # # ============================================================
# # # SECURITY
# # # ============================================================

# # security = HTTPBearer()


# # # ============================================================
# # # REQUEST MODELS
# # # ============================================================

# # class SignupRequest(BaseModel):
# #     name: str
# #     email: EmailStr
# #     password: str


# # class LoginRequest(BaseModel):
# #     email: EmailStr
# #     password: str


# # # ============================================================
# # # PASSWORD HASHING
# # # ============================================================

# # def hash_password(password: str) -> str:

# #     password_bytes = password.encode("utf-8")

# #     if len(password_bytes) > 72:
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Password must be 72 bytes or fewer."
# #         )

# #     hashed = bcrypt.hashpw(
# #         password_bytes,
# #         bcrypt.gensalt()
# #     )

# #     return hashed.decode("utf-8")


# # # ============================================================
# # # VERIFY PASSWORD
# # # ============================================================

# # def verify_password(
# #     password: str,
# #     hashed_password: str
# # ) -> bool:

# #     password_bytes = password.encode("utf-8")

# #     if len(password_bytes) > 72:
# #         return False

# #     try:

# #         return bcrypt.checkpw(
# #             password_bytes,
# #             hashed_password.encode("utf-8")
# #         )

# #     except Exception:

# #         return False


# # # ============================================================
# # # CREATE JWT
# # # ============================================================

# # def create_access_token(
# #     user_id: str,
# #     email: str
# # ):

# #     expire = (
# #         datetime.now(timezone.utc)
# #         + timedelta(
# #             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
# #         )
# #     )

# #     payload = {
# #         "sub": user_id,
# #         "email": email,
# #         "exp": expire
# #     }

# #     return jwt.encode(
# #         payload,
# #         JWT_SECRET,
# #         algorithm=JWT_ALGORITHM
# #     )


# # # ============================================================
# # # GET CURRENT USER FROM JWT
# # # ============================================================

# # def get_current_user(
# #     credentials: HTTPAuthorizationCredentials = Depends(security)
# # ):

# #     token = credentials.credentials

# #     # --------------------------------------------------------
# #     # DECODE JWT
# #     # --------------------------------------------------------

# #     try:

# #         payload = jwt.decode(
# #             token,
# #             JWT_SECRET,
# #             algorithms=[JWT_ALGORITHM]
# #         )

# #     except jwt.ExpiredSignatureError:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Token has expired. Please login again."
# #         )

# #     except jwt.InvalidTokenError:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid authentication token."
# #         )

# #     # --------------------------------------------------------
# #     # GET USER ID
# #     # --------------------------------------------------------

# #     user_id = payload.get("sub")

# #     if not user_id:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid token: user ID is missing."
# #         )

# #     # --------------------------------------------------------
# #     # FIND USER
# #     # --------------------------------------------------------

# #     try:

# #         from bson import ObjectId

# #         user = users_collection.find_one(
# #             {
# #                 "_id": ObjectId(user_id)
# #             }
# #         )

# #     except Exception:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid user ID in token."
# #         )

# #     # --------------------------------------------------------
# #     # USER DOES NOT EXIST
# #     # --------------------------------------------------------

# #     if not user:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="User account no longer exists."
# #         )

# #     return user


# # # ============================================================
# # # SIGNUP
# # # ============================================================

# # @router.post("/signup")
# # def signup(request: SignupRequest):

# #     name = request.name.strip()
# #     email = request.email.lower().strip()

# #     if not name:

# #         raise HTTPException(
# #             status_code=400,
# #             detail="Name is required."
# #         )

# #     if len(request.password) < 6:

# #         raise HTTPException(
# #             status_code=400,
# #             detail="Password must contain at least 6 characters."
# #         )

# #     # --------------------------------------------------------
# #     # CHECK EXISTING USER
# #     # --------------------------------------------------------

# #     existing_user = users_collection.find_one(
# #         {
# #             "email": email
# #         }
# #     )

# #     if existing_user:

# #         raise HTTPException(
# #             status_code=400,
# #             detail="An account with this email already exists."
# #         )

# #     # --------------------------------------------------------
# #     # HASH PASSWORD
# #     # --------------------------------------------------------

# #     hashed_password = hash_password(
# #         request.password
# #     )

# #     # --------------------------------------------------------
# #     # CREATE USER
# #     # --------------------------------------------------------

# #     user = {

# #         "name": name,

# #         "email": email,

# #         "password": hashed_password,

# #         "created_at": datetime.now(
# #             timezone.utc
# #         )
# #     }

# #     # --------------------------------------------------------
# #     # SAVE TO MONGODB
# #     # --------------------------------------------------------

# #     try:

# #         result = users_collection.insert_one(user)

# #     except Exception as e:

# #         # Handles duplicate email race condition
# #         if "duplicate" in str(e).lower():

# #             raise HTTPException(
# #                 status_code=400,
# #                 detail="An account with this email already exists."
# #             )

# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not create account."
# #         )

# #     # --------------------------------------------------------
# #     # RESPONSE
# #     # --------------------------------------------------------

# #     return {

# #         "message": "Account created successfully.",

# #         "user": {

# #             "id": str(result.inserted_id),

# #             "name": name,

# #             "email": email
# #         }
# #     }


# # # ============================================================
# # # LOGIN
# # # ============================================================

# # @router.post("/login")
# # def login(request: LoginRequest):

# #     email = request.email.lower().strip()

# #     # --------------------------------------------------------
# #     # FIND USER
# #     # --------------------------------------------------------

# #     user = users_collection.find_one(
# #         {
# #             "email": email
# #         }
# #     )

# #     if not user:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid email or password."
# #         )

# #     # --------------------------------------------------------
# #     # VERIFY PASSWORD
# #     # --------------------------------------------------------

# #     if not verify_password(
# #         request.password,
# #         user["password"]
# #     ):

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid email or password."
# #         )

# #     # --------------------------------------------------------
# #     # CREATE JWT
# #     # --------------------------------------------------------

# #     access_token = create_access_token(
# #         str(user["_id"]),
# #         user["email"]
# #     )

# #     # --------------------------------------------------------
# #     # RESPONSE
# #     # --------------------------------------------------------

# #     return {

# #         "message": "Login successful.",

# #         "access_token": access_token,

# #         "token_type": "bearer",

# #         "user": {

# #             "id": str(user["_id"]),

# #             "name": user["name"],

# #             "email": user["email"]
# #         }
# #     }


# # # ============================================================
# # # CURRENT USER
# # # ============================================================

# # @router.get("/me")
# # def get_me(
# #     current_user=Depends(get_current_user)
# # ):

# #     return {

# #         "user": {

# #             "id": str(
# #                 current_user["_id"]
# #             ),

# #             "name": current_user["name"],

# #             "email": current_user["email"]
# #         }
# #     }

# import os

# from datetime import (
#     datetime,
#     timedelta,
#     timezone
# )

# import bcrypt
# import jwt

# from dotenv import load_dotenv

# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     status
# )

# from fastapi.security import (
#     HTTPBearer,
#     HTTPAuthorizationCredentials
# )

# from pydantic import (
#     BaseModel,
#     EmailStr
# )

# from database import users_collection


# # ============================================================
# # LOAD ENVIRONMENT VARIABLES
# # ============================================================

# load_dotenv()


# # ============================================================
# # JWT SETTINGS
# # ============================================================

# JWT_SECRET = os.getenv(
#     "JWT_SECRET"
# )

# JWT_ALGORITHM = os.getenv(
#     "JWT_ALGORITHM",
#     "HS256"
# )

# ACCESS_TOKEN_EXPIRE_MINUTES = int(
#     os.getenv(
#         "ACCESS_TOKEN_EXPIRE_MINUTES",
#         "1440"
#     )
# )


# # ============================================================
# # VALIDATE JWT SECRET
# # ============================================================

# if not JWT_SECRET:

#     raise RuntimeError(
#         "JWT_SECRET is missing from the .env file."
#     )


# # ============================================================
# # ROUTER
# # ============================================================

# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )


# # ============================================================
# # HTTP BEARER
# # ============================================================

# security = HTTPBearer(
#     auto_error=False
# )


# # ============================================================
# # REQUEST MODELS
# # ============================================================

# class SignupRequest(BaseModel):

#     name: str

#     email: EmailStr

#     password: str


# class LoginRequest(BaseModel):

#     email: EmailStr

#     password: str


# # ============================================================
# # PASSWORD HASHING
# # ============================================================

# def hash_password(
#     password: str
# ) -> str:

#     password_bytes = password.encode(
#         "utf-8"
#     )


#     # bcrypt maximum = 72 bytes

#     if len(password_bytes) > 72:

#         raise HTTPException(

#             status_code=status.HTTP_400_BAD_REQUEST,

#             detail=(
#                 "Password must be 72 bytes "
#                 "or fewer."
#             )
#         )


#     try:

#         hashed = bcrypt.hashpw(

#             password_bytes,

#             bcrypt.gensalt()
#         )

#         return hashed.decode(
#             "utf-8"
#         )

#     except Exception:

#         raise HTTPException(

#             status_code=500,

#             detail="Could not hash password."
#         )


# # ============================================================
# # VERIFY PASSWORD
# # ============================================================

# def verify_password(
#     password: str,
#     hashed_password: str
# ) -> bool:

#     password_bytes = password.encode(
#         "utf-8"
#     )


#     if len(password_bytes) > 72:

#         return False


#     try:

#         return bcrypt.checkpw(

#             password_bytes,

#             hashed_password.encode(
#                 "utf-8"
#             )
#         )

#     except Exception:

#         return False


# # ============================================================
# # CREATE ACCESS TOKEN
# # ============================================================

# def create_access_token(
#     user_id: str,
#     email: str
# ) -> str:

#     expire = (

#         datetime.now(
#             timezone.utc
#         )

#         + timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     )


#     payload = {

#         "sub": user_id,

#         "email": email,

#         "exp": expire
#     }


#     try:

#         token = jwt.encode(

#             payload,

#             JWT_SECRET,

#             algorithm=JWT_ALGORITHM
#         )

#         return token

#     except Exception:

#         raise HTTPException(

#             status_code=500,

#             detail="Could not create access token."
#         )


# # ============================================================
# # GET CURRENT USER
# # ============================================================

# def get_current_user(

#     credentials: HTTPAuthorizationCredentials = Depends(
#         security
#     )

# ):

#     # --------------------------------------------------------
#     # CHECK AUTHORIZATION HEADER
#     # --------------------------------------------------------

#     if credentials is None:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Authentication required. Please login.",

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )


#     token = credentials.credentials


#     # --------------------------------------------------------
#     # DECODE JWT
#     # --------------------------------------------------------

#     try:

#         payload = jwt.decode(

#             token,

#             JWT_SECRET,

#             algorithms=[
#                 JWT_ALGORITHM
#             ]
#         )

#     except jwt.ExpiredSignatureError:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail=(
#                 "Token has expired. "
#                 "Please login again."
#             ),

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )

#     except jwt.InvalidTokenError:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid authentication token.",

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )


#     # --------------------------------------------------------
#     # GET USER ID
#     # --------------------------------------------------------

#     user_id = payload.get(
#         "sub"
#     )


#     if not user_id:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail=(
#                 "Invalid token: "
#                 "user ID is missing."
#             ),

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )


#     # --------------------------------------------------------
#     # FIND USER
#     # --------------------------------------------------------

#     try:

#         from bson import ObjectId

#         object_id = ObjectId(
#             user_id
#         )

#         user = users_collection.find_one(

#             {
#                 "_id": object_id
#             }
#         )

#     except Exception:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid user ID in token.",

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )


#     # --------------------------------------------------------
#     # USER NOT FOUND
#     # --------------------------------------------------------

#     if not user:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail=(
#                 "User account no longer exists."
#             ),

#             headers={
#                 "WWW-Authenticate": "Bearer"
#             }
#         )


#     return user


# # ============================================================
# # SIGNUP
# # ============================================================

# @router.post("/signup")
# def signup(
#     request: SignupRequest
# ):

#     # --------------------------------------------------------
#     # CLEAN INPUT
#     # --------------------------------------------------------

#     name = request.name.strip()

#     email = request.email.lower().strip()


#     # --------------------------------------------------------
#     # VALIDATE NAME
#     # --------------------------------------------------------

#     if not name:

#         raise HTTPException(

#             status_code=status.HTTP_400_BAD_REQUEST,

#             detail="Name is required."
#         )


#     # --------------------------------------------------------
#     # VALIDATE PASSWORD
#     # --------------------------------------------------------

#     if len(request.password) < 6:

#         raise HTTPException(

#             status_code=status.HTTP_400_BAD_REQUEST,

#             detail=(
#                 "Password must contain "
#                 "at least 6 characters."
#             )
#         )


#     # --------------------------------------------------------
#     # CHECK EXISTING USER
#     # --------------------------------------------------------

#     existing_user = users_collection.find_one(

#         {
#             "email": email
#         }
#     )


#     if existing_user:

#         raise HTTPException(

#             status_code=status.HTTP_400_BAD_REQUEST,

#             detail=(
#                 "An account with this email "
#                 "already exists."
#             )
#         )


#     # --------------------------------------------------------
#     # HASH PASSWORD
#     # --------------------------------------------------------

#     hashed_password = hash_password(
#         request.password
#     )


#     # --------------------------------------------------------
#     # CREATE USER
#     # --------------------------------------------------------

#     user = {

#         "name": name,

#         "email": email,

#         "password": hashed_password,

#         "created_at":
#             datetime.now(
#                 timezone.utc
#             )
#     }


#     # --------------------------------------------------------
#     # SAVE USER
#     # --------------------------------------------------------

#     try:

#         result = users_collection.insert_one(
#             user
#         )

#     except Exception as e:

#         print(
#             "Signup MongoDB error:",
#             e
#         )


#         if (
#             "duplicate"
#             in str(e).lower()
#         ):

#             raise HTTPException(

#                 status_code=400,

#                 detail=(
#                     "An account with this "
#                     "email already exists."
#                 )
#             )


#         raise HTTPException(

#             status_code=500,

#             detail="Could not create account."
#         )


#     # --------------------------------------------------------
#     # RESPONSE
#     # --------------------------------------------------------

#     return {

#         "message":
#             "Account created successfully.",

#         "user": {

#             "id":
#                 str(
#                     result.inserted_id
#                 ),

#             "name":
#                 name,

#             "email":
#                 email
#         }
#     }


# # ============================================================
# # LOGIN
# # ============================================================

# @router.post("/login")
# def login(
#     request: LoginRequest
# ):

#     # --------------------------------------------------------
#     # CLEAN EMAIL
#     # --------------------------------------------------------

#     email = request.email.lower().strip()


#     # --------------------------------------------------------
#     # FIND USER
#     # --------------------------------------------------------

#     try:

#         user = users_collection.find_one(

#             {
#                 "email": email
#             }
#         )

#     except Exception as e:

#         print(
#             "Login MongoDB error:",
#             e
#         )

#         raise HTTPException(

#             status_code=500,

#             detail="Database error during login."
#         )


#     # --------------------------------------------------------
#     # USER NOT FOUND
#     # --------------------------------------------------------

#     if not user:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid email or password."
#         )


#     # --------------------------------------------------------
#     # VERIFY PASSWORD
#     # --------------------------------------------------------

#     password_valid = verify_password(

#         request.password,

#         user.get(
#             "password",
#             ""
#         )
#     )


#     if not password_valid:

#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid email or password."
#         )


#     # --------------------------------------------------------
#     # CREATE JWT
#     # --------------------------------------------------------

#     access_token = create_access_token(

#         str(
#             user["_id"]
#         ),

#         user["email"]
#     )


#     # --------------------------------------------------------
#     # RESPONSE
#     # --------------------------------------------------------

#     return {

#         "message":
#             "Login successful.",

#         "access_token":
#             access_token,

#         "token_type":
#             "bearer",

#         "user": {

#             "id":
#                 str(
#                     user["_id"]
#                 ),

#             "name":
#                 user.get(
#                     "name",
#                     ""
#                 ),

#             "email":
#                 user.get(
#                     "email",
#                     ""
#                 )
#         }
#     }


# # ============================================================
# # CURRENT USER
# # ============================================================

# @router.get("/me")
# def get_me(

#     current_user=Depends(
#         get_current_user
#     )

# ):

#     return {

#         "user": {

#             "id":
#                 str(
#                     current_user["_id"]
#                 ),

#             "name":
#                 current_user.get(
#                     "name",
#                     ""
#                 ),

#             "email":
#                 current_user.get(
#                     "email",
#                     ""
#                 )
#         }
#     }
import os

from datetime import (
    datetime,
    timedelta,
    timezone
)

import bcrypt
import jwt

from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from pydantic import (
    BaseModel,
    EmailStr
)

from database import users_collection


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


JWT_SECRET = os.getenv(
    "JWT_SECRET"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "1440"
    )
)


# ============================================================
# VALIDATE JWT SECRET
# ============================================================

if not JWT_SECRET:

    raise RuntimeError(
        "JWT_SECRET is missing from the .env file."
    )


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# SECURITY
# ============================================================

security = HTTPBearer(
    auto_error=False
)


# ============================================================
# REQUEST MODELS
# ============================================================

class SignupRequest(BaseModel):

    name: str

    email: EmailStr

    password: str


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(
    password: str
) -> str:

    password_bytes = password.encode(
        "utf-8"
    )

    # bcrypt maximum = 72 bytes

    if len(password_bytes) > 72:

        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be 72 bytes "
                "or fewer."
            )
        )

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode(
        "utf-8"
    )


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    password_bytes = password.encode(
        "utf-8"
    )

    if len(password_bytes) > 72:

        return False

    try:

        return bcrypt.checkpw(
            password_bytes,
            hashed_password.encode(
                "utf-8"
            )
        )

    except Exception:

        return False


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    user_id: str,
    email: str
) -> str:

    expire = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {

        "sub": user_id,

        "email": email,

        "exp": expire
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    # ========================================================
    # CHECK AUTHORIZATION HEADER
    # ========================================================

    if credentials is None:

        raise HTTPException(
            status_code=401,
            detail=(
                "Authentication required. "
                "Please login first."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    token = credentials.credentials


    # ========================================================
    # DECODE JWT
    # ========================================================

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail=(
                "Token has expired. "
                "Please login again."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid authentication token."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    # ========================================================
    # GET USER ID
    # ========================================================

    user_id = payload.get(
        "sub"
    )

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid token: "
                "user ID is missing."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    # ========================================================
    # CONVERT USER ID
    # ========================================================

    try:

        from bson import ObjectId

        object_id = ObjectId(
            user_id
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid user ID in token."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    # ========================================================
    # FIND USER
    # ========================================================

    try:

        user = users_collection.find_one(
            {
                "_id": object_id
            }
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to verify user account."
            )
        )


    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if not user:

        raise HTTPException(
            status_code=401,
            detail=(
                "User account no longer exists."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    return user


# ============================================================
# SIGNUP
# ============================================================

@router.post("/signup")
def signup(
    request: SignupRequest
):

    # ========================================================
    # CLEAN INPUT
    # ========================================================

    name = request.name.strip()

    email = (
        request.email
        .lower()
        .strip()
    )


    # ========================================================
    # VALIDATE NAME
    # ========================================================

    if not name:

        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )


    # ========================================================
    # VALIDATE PASSWORD
    # ========================================================

    if len(request.password) < 6:

        raise HTTPException(
            status_code=400,
            detail=(
                "Password must contain "
                "at least 6 characters."
            )
        )


    # ========================================================
    # CHECK EXISTING USER
    # ========================================================

    try:

        existing_user = users_collection.find_one(
            {
                "email": email
            }
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to check existing account."
            )
        )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail=(
                "An account with this email "
                "already exists."
            )
        )


    # ========================================================
    # HASH PASSWORD
    # ========================================================

    hashed_password = hash_password(
        request.password
    )


    # ========================================================
    # CREATE USER
    # ========================================================

    user = {

        "name": name,

        "email": email,

        "password": hashed_password,

        "created_at": datetime.now(
            timezone.utc
        )
    }


    # ========================================================
    # SAVE USER
    # ========================================================

    try:

        result = users_collection.insert_one(
            user
        )

    except Exception as e:

        print(
            "Signup database error:",
            e
        )

        # Duplicate email race condition

        if (
            "duplicate"
            in str(e).lower()
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "An account with this email "
                    "already exists."
                )
            )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not create account."
            )
        )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "message":
            "Account created successfully.",

        "user": {

            "id":
                str(result.inserted_id),

            "name":
                name,

            "email":
                email
        }
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login(
    request: LoginRequest
):

    email = (
        request.email
        .lower()
        .strip()
    )


    # ========================================================
    # FIND USER
    # ========================================================

    try:

        user = users_collection.find_one(
            {
                "email": email
            }
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to access user account."
            )
        )


    if not user:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email or password."
            )
        )


    # ========================================================
    # VERIFY PASSWORD
    # ========================================================

    password_valid = verify_password(
        request.password,
        user.get(
            "password",
            ""
        )
    )


    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email or password."
            )
        )


    # ========================================================
    # CREATE JWT
    # ========================================================

    access_token = create_access_token(
        str(user["_id"]),
        user["email"]
    )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "message":
            "Login successful.",

        "access_token":
            access_token,

        "token_type":
            "bearer",

        "user": {

            "id":
                str(user["_id"]),

            "name":
                user.get(
                    "name",
                    ""
                ),

            "email":
                user["email"]
        }
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me")
def get_me(
    current_user=Depends(
        get_current_user
    )
):

    return {

        "user": {

            "id":
                str(
                    current_user["_id"]
                ),

            "name":
                current_user.get(
                    "name",
                    ""
                ),

            "email":
                current_user.get(
                    "email",
                    ""
                )
        }
    }
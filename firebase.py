from firebase_admin import credentials, initialize_app, storage, get_app
import os
import logging
import tracemalloc
import asyncio

tracemalloc.start()


log_level = logging.DEBUG if os.getenv('ENVIRONMENT') == 'development' else logging.ERROR
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


class Settings(BaseSettings):

    # Environment
    environment: str = "development"
    debug: bool = False

    # Collection names
    ingredients_profile_collection: str = "ingredients_profile"
    products_collection: str = "products"
    users_collection: str = "users"
    indexed_ingredient_field: str = "indexed_ingredient_field"

    # API Keys
    serper_api_key: str
    agentops_api_key: str
    openai_api_key: str
    gemini_api_key: str

    # Firebase settings
    firebase_type: str
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    firebase_auth_uri: str
    firebase_token_uri: str
    firebase_auth_provider_x509_cert_url: str
    firebase_client_x509_cert_url: str
    firebase_universe_domain: str
    firebase_storage_bucket: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Allow extra fields
        env_nested_delimiter="__",  # For nested settings
    )

    def model_post_init(self, _):
        # Clean up the private key after loading
        if hasattr(self, "firebase_private_key"):
            # Remove any surrounding quotes and properly handle newlines
            key = self.firebase_private_key
            if key.startswith('"') and key.endswith('"'):
                key = key[1:-1]
            self.firebase_private_key = key.replace("\\n", "\n")

        self.debug = self.environment in ["development", "local"]

        # Validate environment
        if self.environment not in ["development", "staging", "production", "local"]:
            raise ValueError(f"Invalid environment: {self.environment}")
        # add suffix to all the collection names
        self.ingredients_profile_collection = (
            f"{self.ingredients_profile_collection}_{self.environment}"
        )
        self.products_collection = f"{self.products_collection}_{self.environment}"
        self.users_collection = f"{self.users_collection}_{self.environment}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

class FirebaseService:
    _instance = None
    _initialized = False

    def __new__(cls, settings: Settings):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings):
        if not self._initialized:
            self.settings = settings
            logger.info("Initializing Firebase with credentials:")
            logger.info(f"Project ID: {self.settings.firebase_project_id}")
            logger.info(f"Client Email: {self.settings.firebase_client_email}")
            logger.info(f"Private Key ID exists: {bool(self.settings.firebase_private_key_id)}")
            logger.info(f"Private Key exists: {bool(self.settings.firebase_private_key)}")
            self._app = self._initialize_firebase()
            logger.info("Getting storage bucket...")
            self.bucket = storage.bucket(app=self._app)
            logger.info("Successfully got storage bucket")
            FirebaseService._initialized = True

    def _initialize_firebase(self):
        """Initialize Firebase with credentials from settings"""
        logger.info("Starting Firebase initialization...")
        
        try:
            # Try to get existing app
            return get_app('default')
        except ValueError:
            # If app doesn't exist, create new one
            # Clean and format the private key
            private_key = self.settings.firebase_private_key
            if private_key.startswith('"') and private_key.endswith('"'):
                private_key = private_key[1:-1]  # Remove surrounding quotes
            private_key = private_key.replace('\\n', '\n')  # Replace escaped newlines
            
            firebase_creds = {
                "type": self.settings.firebase_type,
                "project_id": self.settings.firebase_project_id,
                "private_key_id": self.settings.firebase_private_key_id,
                "private_key": private_key,
                "client_email": self.settings.firebase_client_email,
                "client_id": self.settings.firebase_client_id,
                "auth_uri": self.settings.firebase_auth_uri,
                "token_uri": self.settings.firebase_token_uri,
                "auth_provider_x509_cert_url": self.settings.firebase_auth_provider_x509_cert_url,
                "client_x509_cert_url": self.settings.firebase_client_x509_cert_url,
                "universe_domain": self.settings.firebase_universe_domain
            }
            
            # Debug logging
            logger.info("Firebase credentials structure:")
            for key in firebase_creds:
                if key == "private_key":
                    logger.info(f"{key}: [REDACTED, Length: {len(firebase_creds[key])}]")
                    logger.info(f"Private key starts with: {firebase_creds[key][:27]}...")
                    logger.info(f"Private key ends with: ...{firebase_creds[key][-25:]}")
                else:
                    logger.info(f"{key}: {firebase_creds[key]}")
            
            logger.info("Creating Firebase credentials certificate...")
            try:
                cred = credentials.Certificate(firebase_creds)
                logger.info("Successfully created credentials certificate")
                
                logger.info(f"Initializing Firebase app with storage bucket: {self.settings.firebase_storage_bucket}")
                return initialize_app(cred, {
                    'storageBucket': self.settings.firebase_storage_bucket
                }, name='default')
            except Exception as e:
                logger.error(f"Error initializing Firebase: {str(e)}")
                logger.error(f"Error type: {type(e)}")
                if hasattr(e, '__cause__') and e.__cause__:
                    logger.error(f"Caused by: {str(e.__cause__)}")
                raise

    def upload_image(self, file_path: str, directory: str) -> str:
        blob_name = f"uploads/{directory}/{os.path.basename(file_path)}"
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        blob.make_public()
        return blob.public_url

    def delete_directory(self, directory: str):
        """Delete all files within a directory in Firebase Storage"""
        logger.info(f"Deleting directory: {directory}")
        blobs = self.bucket.list_blobs(prefix=f"{directory}/")
        
        deleted_files = []
        for blob in blobs:
            logger.info(f"Deleting file: {blob.name}")
            blob.delete()
            deleted_files.append(blob.name)
        
        if deleted_files:
            logger.info(f"Deleted files: {deleted_files}")
        else:
            logger.info(f"No files found in directory: {directory}")
        return deleted_files


if __name__ == "__main__":
    settings = get_settings()
    firebase = FirebaseService(settings)


    async def main():
        url = await firebase.upload_image("image_blinkit/image40799.jpg", "test")
        print(f"Uploaded image URL: {url}")
    asyncio.run(main())

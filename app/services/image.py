from os import makedirs
from os.path import exists, join
from typing import Literal

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.core.errors import NotFoundError, ValidationError


class ImageService:
    """
    A service class for managing images.
    This class provides methods to upload and retrieve images from the server.

    Attributes:
        IMAGES_DIR (str): The directory where images are stored.
        DIRECTORIES (list): A list of allowed directories for image uploads.

    Methods:
        upload_image(image: UploadFile, filename: str, directory: Literal["event"]) -> str:
            Upload an image to the specified directory and return the file path.
        get_image(image_path: str) -> FileResponse:
            Retrieve an image from the server and return it as a FileResponse.
    """

    IMAGES_DIR = "app/images"

    @classmethod
    async def upload_image(
        cls,
        image: UploadFile,
        filename: str
    ) -> str:
        """
        Upload an image to the specified directory and return the file path.

        Args:
            image (UploadFile): The image file to upload.
            filename (str): The name of the file.
            directory (str): The directory where the file will be saved.

        Returns:
            str: The file path of the uploaded image.
        """

        file_path = ""

        filename = filename + ".jpg"


        if not exists(cls.IMAGES_DIR):
            makedirs(cls.IMAGES_DIR, exist_ok=True)
        
        file_path = join(cls.IMAGES_DIR, filename)

        content = await image.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        return join("/images", filename)

    def get_image(image_path: str) -> FileResponse:
        """
        Coleta uma imagem do servidor e a envia no formato FileResponse

        - Args:
            - folder:: Literal["event", "client"]: Indica se o arquivo é para eventos, clientes ou marketing
            - master_id:: str: ID do objeto principal que contem este que o arquivo. (Se for um client, então é o client.id, se for Evento, logo event.id)

        - Returns:
            - FileResponse:: Imagem Encontrada
        """

        if not exists(image_path):
            raise NotFoundError(
                detail="Imagem não encontrada",
                local="services/image/ImageService/get_image",
            )

        return FileResponse(image_path, media_type="image/jpeg")
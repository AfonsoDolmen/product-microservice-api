from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        """
        Remove os valores nulos do dicionário
        """
        d = super().dict(*args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}

        return d

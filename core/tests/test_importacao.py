import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_importacao_csv_file_upload(tmp_path):
    client = APIClient()
    content = b"nome,area\nX,AreaX\n"
    upload = SimpleUploadedFile(
        name="disc.csv",
        content=content,
        content_type="text/csv",
    )

    url = reverse("importacao-list")
    resp = client.post(url, {"file": upload}, format="multipart")
    assert resp.status_code == 201, resp.content

    data = resp.json()
    assert data["status"] in ("pending", "processing", "done")
    assert "registros_total" in data
    assert isinstance(data["registros_total"], int)

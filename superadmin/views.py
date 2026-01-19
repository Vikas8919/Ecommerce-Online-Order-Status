import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from sympy.integrals.meijerint_doc import category
from torch.cpu import is_available

from products.models import Product, Category

def excel_upload(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        file = request.FILES["excel_file"]
        df = pd.read_excel(file)

        preview_data = df.to_dict(orient="records")
        request.session["excel_data"] = preview_data

        return render(request, "File upload/excel_preview.html", {
            "data": preview_data,
            "columns": df.columns
        })

    return render(request, "File upload/excel_upload.html")


@transaction.atomic
def excel_confirm(request):
    data = request.session.get("excel_data")

    if not data:
        return redirect("excel_upload")

    try:
        category = get_object_or_404(Category, id=1)
        for row in data:
            if Product.objects.filter(name=row["name"]).exists():
                continue  # skip duplicates

            image_path = None
            if row.get("image"):
                img = str(row["image"])
                image_path = f"products/{img}"

            Product.objects.create(
                category = category,
                name=row.get("name"),
                price=row.get("price"),
                stock=row.get("stock"),
                description=row.get("description"),
                image=image_path,
                is_available = row.get("is_available", True)
            )

        del request.session["excel_data"]
        return render(request, "File upload/excel_success.html")

    except Exception as e:
        return render(request, "File upload/excel_error.html", {"error": str(e)})

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from common.json import ModelEncoder
from .models import BinVO, Shoe
import json

# Create your views here.


class BinVOEncoder(ModelEncoder):
    model = BinVO
    properties = [
        "import_id",
        "closet_name",
    ]

class ShoeListEncoder(ModelEncoder):
    model = Shoe
    properties = [
        "manufacturer",
        "model_name",
        "color",
        "picture_url",
        "id",
    ]

    def get_extra_data(self, o):
        return {"bin": o.bin.closet_name}


class ShoeDetailEncoder(ModelEncoder):
    model = Shoe
    properties = [
        "manufacturer",
        "model_name",
        "color",
        "picture_url",
        "bin",
    ]
    encoders = {
        "bin": BinVOEncoder(),
    }

@require_http_methods(["GET", "POST"])
def api_list_shoes(request):
    shoes = Shoe.objects.order_by("id")
    if request.method == "GET":
        shoes = Shoe.objects.all()
        return JsonResponse(
            {"shoes": shoes},
            encoder=ShoeListEncoder,
        )
    # POST
    else:
        content = json.loads(request.body)

        try:
            bin = BinVO.objects.get(import_id=content["bin"])
            print(content["bin"])
            print(bin)
            content["bin"] = bin
        except BinVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid bin id"},
                status=400,
            )
        
        shoes = Shoe.objects.create(**content)
        return JsonResponse(
            shoes,
            encoder=ShoeDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE","GET", "PUT"])
def api_show_shoe(request, pk):
    # Show details of shoe
    if request.method == "GET":
        shoe = Shoe.objects.get(id=pk)
        return JsonResponse(
            shoe,
            encoder=ShoeDetailEncoder,
            safe=False,
        )
    # Delete shoe
    elif request.method == "DELETE":
        try:
            shoe = Shoe.objects.get(id=pk)
            shoe.delete()
            return JsonResponse(
                shoe,
                encoder=ShoeDetailEncoder,
                safe=False,
            )
        except Shoe.DoesNotExist:
            return JsonResponse({"message": "Does not exist"})
    # Update shoe
    else:
        content = json.loads(request.body)
        Shoe.objects.filter(id=pk).update(**content)
        shoe = Shoe.objects.get(id=pk)
        return JsonResponse(
            shoe,
            encoder=ShoeDetailEncoder,
            safe=False,
        )

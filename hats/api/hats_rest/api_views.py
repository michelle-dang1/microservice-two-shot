from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from common.json import ModelEncoder
from .models import LocationVO, Hat

class LocationVODetailEncoder(ModelEncoder):
    model = LocationVO
    properties = ["closet_name", "import_id"]

class HatListEncoder(ModelEncoder):
    model = Hat
    properties = ["fabric", "style_name", "color", "picture_url", "id"]

    def get_extra_data(self, o):
        return {"location": o.location.closet_name}
    
class HatDetailEncoder(ModelEncoder):
    model = Hat
    properties = [
        "fabric",
        "style_name",
        "color",
        "picture_url",
    ]
    encoders = {
        "location": LocationVODetailEncoder(),
    }

@require_http_methods(["GET", "POST"])
def api_list_hats(request):
    hats = Hat.objects.order_by("id")
    if request.method == "GET":
        return JsonResponse(
            {"hats": hats},
            encoder=HatListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            location = LocationVO.objects.get(id=content["location"])
            content["location"] = location
        except LocationVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400
            )
        hats = Hat.objects.create(**content)
        return JsonResponse(
            hats,
            encoder=HatDetailEncoder,
            safe=False
        )

@require_http_methods(["DELETE", "GET", "PUT"])
def api_hat_details(request, pk):
    try:
        hat = Hat.objects.get(id=pk)
        if request.method == "GET":
            return JsonResponse(
                {"hat": hat},
                encoder=HatListEncoder,
                safe=False,
            )
        elif request.method == "DELETE":
            count, _ = Hat.objects.filter(id=pk).delete()
            return JsonResponse({"Deleted": count > 0})
        else:
            content = json.loads(request.body)
            try:
                hat = Hat.objects.get(id=pk)
            except Hat.DoesNotExist:
                return JsonResponse(
                    {"message": "Invalid hat id"},
                    status=400,
                )
            Hat.objects.filter(id=pk).update(**content)
            hat = Hat.objects.get(id=pk)
            print(hat)
            return JsonResponse(
                hat,
                encoder=HatDetailEncoder,
                safe=False,
            )
    except Hat.DoesNotExist:
        return JsonResponse(
            {"message": "Hat does not exist"},
            status=400,
        )

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesDetailSerializer, PropertiesListSerializer, ReservationsListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])

def properties_list(request):
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations =  property.reservations.all()

    serializer = ReservationsListSerializer(reservations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        return JsonResponse({
            'success': True
        })
    else:
        print('errores: ', form.errors, form.non_field_errors)

        return JsonResponse({
            'errores: ', form.errors.as_json()
        }, status=400)
    
@api_view(['POST'])
def book_property(request, pk):
    try:
        data = request.data

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        number_of_nights = int(data.get('number_of_nights', 1))
        total_price = float(data.get('total_price', 0))
        guests = int(data.get('guests', 1))

        property = Property.objects.get(pk=pk)

        reservation = Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )

        return JsonResponse({'success': True, 'reservation_id': str(reservation.id)})
    
    except Exception as e:
        print('Error', e)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


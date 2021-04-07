from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import ProductSerializer, ReviewSerializer
from .models import Product


class Index(APIView):
    def get(self, request):
        query = request.query_params.get('keyword')
        page = request.query_params.get('page')

        if query is None:
            query = ''

        products = Product.objects.all().filter(
            name__icontains=query).order_by('-createdAt')

        paginator = Paginator(products, 5)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        page = int(page)

        serializer = ProductSerializer(products, many=True)

        return Response(
            {
                'products': serializer.data, 'page': page,
                'pages': paginator.num_pages
            }
        )


class Create(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        product = Product.objects.create(
            user=request.user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category='Sample Category',
            description=''
        )
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class Show(APIView):
    def get(self, request, pk):
        products = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(products, many=False)
        return Response(serializer.data)


class Update(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {'detail': 'Data is Not Valid'},
            status=HTTP_400_BAD_REQUEST
        )


class Delete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=HTTP_200_OK)


class TopProducts(APIView):
    def get(self, request):
        product = Product.objects.filter(rating__gte=4).order_by('-rating')[:5]
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class UploadImage(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        product = get_object_or_404(Product, id=request.data['product_id'])
        product.image = request.FILES.get('image')
        product.save()
        return Response('image Uploaded')


class CreateReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        isReviewd = Product.objects.filter(user=user).exists()

        if isReviewd:
            return Response(
                'Product Already Reviewd',
                status=HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=user, name=user.first_name)

            reviews = product.review_set.all()

            total = 0
            for review in reviews:
                total += review.rating

            product.numReviews = len(reviews)
            product.rating = total / product.numReviews
            product.save()

            return Response('Review Added', status=HTTP_200_OK)

        return Response('Data is Not Valid', status=HTTP_400_BAD_REQUEST)

from myapp.viewsets import userviewsets, register
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user',userviewsets,basename='user_api')
router.register('register',register,basename='user_register_api')

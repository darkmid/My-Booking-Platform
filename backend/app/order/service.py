from typing import List

from flask_jwt_extended import get_current_user

from app.core.page import paginate
from app.core.service import BaseService
from app.course.model import Course
from app.exceptions.permission_exceptions import PermissionDenied
from app.order.model import Order
from app.order.schema import OrderCreateSchema, OrderPaymentSchema
from app.user.model import Student, User


class OrderService(BaseService):
    def __init__(self, user):
        super().__init__(OrderService.__name__, user)

    def get_order_query(self, **kwargs):
        if self.user._cls == "User.Admin" and "order_admin" in self.user.permissions:
            return Order.objects(**kwargs)
        else:
            return Order.objects(student=self.user, **kwargs)

    def place_order(self, order: OrderCreateSchema) -> Order:
        if (
            self.user._cls == "User.Admin" and "order_admin" in self.user.permissions
        ) or (str(self.user.id) == order.student):
            self.logger.info("Placing orders", order.dict())
            Student.objects(id=order.student).first_or_404("Student not exists")
            course = Course.objects(id=order.course).first_or_404("Course not exsists")
            order.original_price = course.original_price
            return Order(**order.dict(exclude_none=True)).save()
        else:
            raise PermissionDenied()

    def list_orders(
        self,
        user: str = None,
        course: str = None,
        campus: str = None,
        paid: str = None,
        page: int = 1,
    ) -> List[Order]:
        self.logger.info("Fetching orders")
        querys = {}
        if user is not None:
            querys["user"] = user
        if course is not None:
            querys["course"] = course
        if campus is not None:
            querys["campus"] = campus
        if paid is not None:
            querys["paid"] = paid.lower() == "true"
        return paginate(self.get_order_query(**querys), page_num=page)

    def get_order(self, order_id) -> Order:
        return self.get_order_query(id=order_id).first_or_404("Order not exists")

    def delete_order(self, order_id) -> int:
        order = Order.objects(id=order_id).first_or_404("Order not exists")
        return order.delete()

    def pay_order(self, order_id, payment_info: OrderPaymentSchema):
        order: Order = Order.objects(id=order_id).first_or_404("Order not exists")
        if payment_info.paid_price is None:
            payment_info.paid_price = order.original_price
        order_updated = order.update(**payment_info.dict())
        order.reload()
        if order.paid:
            order.course.update(add_to_set__enrolled_students=order.student)
            order.student.update(add_to_set__enrolled_courses=order.course)
        return order_updated


def order_service():
    return OrderService(get_current_user())

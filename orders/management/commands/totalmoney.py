from django.core.management.base import BaseCommand, CommandError
from orders.models import Order, OrderItem
from django.db.models import Count

class Command(BaseCommand):
	help = 'Displays the total amount of money made from orders'

	def handle(self, *args, **options):
		order_list = Order.objects.all().annotate(num_items=Count('movies'))
		sum_cost = 0
		order_count = 0
		item_count = 0
		for order in order_list:
			sum_cost += order.get_total_cost()
			item_count += order.num_items
			order_count += 1
		self.stdout.write("Total revenue is £" + str(sum_cost) + " over " + str(item_count) + " items in " + str(order_count) + " orders")


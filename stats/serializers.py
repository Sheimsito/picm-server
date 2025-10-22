from rest_framework import serializers


class TopProductsSalesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_sales = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    category_name = serializers.CharField()


class TopProductsEntriesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_entries = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    category_name = serializers.CharField()


class ProductMovementsVolumeSerializer(serializers.Serializer):
    entries = serializers.IntegerField()
    sales = serializers.IntegerField()
    net_movement = serializers.IntegerField()
    period = serializers.CharField()
    total_movements = serializers.IntegerField()


class MonthlyMovementsSerializer(serializers.Serializer):
    month = serializers.CharField()
    month_number = serializers.IntegerField()
    entries = serializers.IntegerField()
    sales = serializers.IntegerField()
    net_movement = serializers.IntegerField()


class MonthlyMovementsResponseSerializer(serializers.Serializer):
    data = MonthlyMovementsSerializer(many=True)
    year = serializers.IntegerField()
    total_entries = serializers.IntegerField()
    total_sales = serializers.IntegerField()


class TopSuppliesSalesSerializer(serializers.Serializer):
    supply_id = serializers.IntegerField()
    supply_name = serializers.CharField()
    total_sales = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    supplier_name = serializers.CharField()


class TopSuppliesEntriesSerializer(serializers.Serializer):
    supply_id = serializers.IntegerField()
    supply_name = serializers.CharField()
    total_entries = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    supplier_name = serializers.CharField()


class SupplyMovementsVolumeSerializer(serializers.Serializer):
    entries = serializers.IntegerField()
    sales = serializers.IntegerField()
    net_movement = serializers.IntegerField()
    period = serializers.CharField()
    total_movements = serializers.IntegerField()


class CategoryDistributionSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    total_stock = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_movements = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class CategoryDistributionResponseSerializer(serializers.Serializer):
    data = CategoryDistributionSerializer(many=True)
    total_categories = serializers.IntegerField()
    metric = serializers.CharField()


class StatisticsResponseSerializer(serializers.Serializer):
    data = serializers.ListField()
    period = serializers.CharField(required=False)
    total_products = serializers.IntegerField(required=False)
    total_supplies = serializers.IntegerField(required=False)

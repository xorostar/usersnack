import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useOrders } from "../hooks";

const OrdersPage = () => {
  const { orders, formatDate, getStatusColor } = useOrders();

  if (orders.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📋</div>
        <h1 className="text-2xl font-bold mb-2">No Orders Yet</h1>
        <p className="text-muted-foreground mb-6">
          You haven't placed any orders yet. Start by browsing our delicious
          menu!
        </p>
        <a
          href="/"
          className="inline-flex items-center px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
        >
          Browse Menu
        </a>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">My Orders</h1>
        <p className="text-muted-foreground">
          Track your order history and delivery status
        </p>
      </div>

      <div className="space-y-4">
        {orders.map((order, orderIndex) => (
          <Card
            key={order.id}
            className="overflow-hidden hover:shadow-md transition-shadow"
          >
            <CardHeader className="bg-gradient-to-r from-muted/30 to-muted/10 pb-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="text-primary font-semibold text-sm">
                      #{orderIndex + 1}
                    </span>
                  </div>
                  <div>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <span>Order #{order.id.slice(0, 8)}</span>
                      <Badge
                        variant="secondary"
                        className={getStatusColor(order.status)}
                      >
                        {order.status}
                      </Badge>
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {formatDate(order.created_at)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-primary">
                    €{order.total_amount}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {order.currency}
                  </p>
                </div>
              </div>

              {/* Customer Information */}
              <div className="mt-4 pt-4 border-t border-border">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-muted-foreground font-medium mb-1">
                      Customer
                    </p>
                    <p className="text-sm font-medium">{order.customer_name}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground font-medium mb-1">
                      Delivery Address
                    </p>
                    <p className="text-sm">{order.customer_address}</p>
                  </div>
                </div>
              </div>
            </CardHeader>

            <CardContent className="p-0">
              <div className="divide-y divide-border">
                {order.items.map((item, index) => (
                  <div
                    key={index}
                    className="p-4 hover:bg-muted/30 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="font-semibold text-base truncate">
                            {item.food_item_name}
                          </span>
                          <Badge
                            variant="outline"
                            className="text-xs flex-shrink-0"
                          >
                            x{item.quantity}
                          </Badge>
                        </div>

                        {item.extras.length > 0 && (
                          <div className="mb-2">
                            <p className="text-xs text-muted-foreground mb-1 font-medium">
                              Extras:
                            </p>
                            <div className="flex flex-wrap gap-1">
                              {item.extras.map((extra) => (
                                <Badge
                                  key={extra.id}
                                  variant="secondary"
                                  className="text-xs"
                                >
                                  {extra.name}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        )}

                        <p className="text-sm text-muted-foreground">
                          €{item.unit_price} each
                        </p>
                      </div>

                      <div className="text-right ml-4 flex-shrink-0">
                        <p className="font-semibold text-lg">
                          €{item.line_total}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default OrdersPage;

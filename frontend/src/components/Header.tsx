import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";

const Header = () => {
  const getOrderCount = () => {
    try {
      const orders = JSON.parse(localStorage.getItem("orders") || "[]");
      return orders.length;
    } catch {
      return 0;
    }
  };

  const orderCount = getOrderCount();

  return (
    <header className="bg-background border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-primary">
            Usersnack
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="text-muted-foreground hover:text-foreground font-medium transition-colors"
            >
              Menu
            </Link>

            <Link
              to="/orders"
              className="flex items-center space-x-2 bg-muted px-3 py-2 rounded-lg hover:bg-muted/80 transition-colors"
            >
              <span className="font-medium">My Orders</span>
              {orderCount > 0 && (
                <Badge
                  variant="secondary"
                  className="bg-primary text-primary-foreground"
                >
                  {orderCount}
                </Badge>
              )}
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

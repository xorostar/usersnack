import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="text-center max-w-md mx-auto">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-primary mb-4">404</h1>
          <h2 className="text-2xl font-semibold text-foreground mb-4">
            Page Not Found
          </h2>
          <p className="text-muted-foreground mb-8">
            Sorry, the page you're looking for doesn't exist or has been moved.
          </p>
        </div>

        <div className="space-y-4">
          <Button asChild className="w-full">
            <Link to="/">Back to Menu</Link>
          </Button>

          <Button variant="outline" asChild className="w-full">
            <Link to="/orders">View My Orders</Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;

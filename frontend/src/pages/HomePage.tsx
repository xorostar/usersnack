import FoodCard from "../components/FoodCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { Button } from "@/components/ui/button";
import { useFoodItems } from "../hooks";

const HomePage = () => {
  const { foodItems, loading, error, refetch } = useFoodItems();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-destructive text-lg mb-4">{error}</div>
        <Button onClick={refetch}>Try Again</Button>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to UserSnack!
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Explore our delicious menu and customize your favorite snacks. Click
          any item to add extras and place your order!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {foodItems.map((foodItem) => (
          <FoodCard key={foodItem.id} foodItem={foodItem} />
        ))}
      </div>

      {foodItems.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-muted-foreground text-lg">
            No food items available at the moment.
          </p>
        </div>
      )}
    </div>
  );
};

export default HomePage;

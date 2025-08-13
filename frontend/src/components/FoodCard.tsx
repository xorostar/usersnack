import { useState } from "react";
import { Link } from "react-router-dom";
import type { FoodItem } from "../types";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface FoodCardProps {
  foodItem: FoodItem;
}

const FoodCard = ({ foodItem }: FoodCardProps) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  // Generate Unsplash URL based on food item name
  const getUnsplashImageUrl = (foodName: string) => {
    const searchTerm = encodeURIComponent(
      foodName.toLowerCase().replace(/[^a-z0-9\s]/g, "")
    );
    return `https://source.unsplash.com/400x300/?${searchTerm},food`;
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoading(false);
  };

  const handleImageLoad = () => {
    setImageLoading(false);
  };

  return (
    <Link to={`/product/${foodItem.id}`} className="block group">
      <Card className="overflow-hidden pt-0 hover:shadow-lg transition-shadow duration-300">
        <div className="aspect-w-16 aspect-h-9 bg-muted relative">
          {imageLoading && (
            <div className="absolute inset-0 flex items-center justify-center bg-muted">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          )}

          {foodItem.image && !imageError ? (
            <img
              src={foodItem.image}
              alt={foodItem.name}
              className={`w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300 ${
                imageLoading ? "opacity-0" : "opacity-100"
              }`}
              onError={handleImageError}
              onLoad={handleImageLoad}
            />
          ) : (
            <img
              src={getUnsplashImageUrl(foodItem.name)}
              alt={foodItem.name}
              className={`w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300 ${
                imageLoading ? "opacity-0" : "opacity-100"
              }`}
              onError={handleImageError}
              onLoad={handleImageLoad}
            />
          )}

          {imageError && !imageLoading && (
            <div className="absolute inset-0 flex items-center justify-center bg-muted">
              <div className="text-center">
                <span className="text-muted-foreground text-4xl mb-2 block">
                  🍕
                </span>
                <p className="text-muted-foreground text-sm">
                  Image unavailable
                </p>
              </div>
            </div>
          )}
        </div>

        <CardHeader className="pb-2">
          <h3 className="text-lg font-semibold group-hover:text-primary transition-colors">
            {foodItem.name}
          </h3>
          <p className="text-2xl font-bold text-primary">
            €{foodItem.base_price}
          </p>
        </CardHeader>

        <CardContent className="pt-0">
          <p className="text-sm text-muted-foreground mb-2">Ingredients:</p>
          <div className="relative">
            <div className="flex gap-1 overflow-x-auto scrollbar-hide pb-2">
              {foodItem.ingredients.map((ingredient) => (
                <Badge
                  key={ingredient.id}
                  variant="secondary"
                  className="text-xs whitespace-nowrap flex-shrink-0"
                >
                  {ingredient.name}
                </Badge>
              ))}
            </div>
            <div className="absolute right-0 top-0 bottom-2 w-8 bg-gradient-to-l from-background to-transparent pointer-events-none"></div>
          </div>
        </CardContent>

        <CardFooter className="pt-0">
          <div className="flex items-center justify-between w-full">
            <span className="text-sm text-muted-foreground capitalize">
              {foodItem.category}
            </span>
            <span className="text-primary font-medium group-hover:underline">
              Order Now →
            </span>
          </div>
        </CardFooter>
      </Card>
    </Link>
  );
};

export default FoodCard;

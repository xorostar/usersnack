import { useState } from "react";
import type { FoodItem } from "../types";
import { Card } from "@/components/ui/card";

interface ProductImageProps {
  foodItem: FoodItem;
}

const ProductImage = ({ foodItem }: ProductImageProps) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  const getUnsplashImageUrl = (foodName: string) => {
    const searchTerm = encodeURIComponent(
      foodName.toLowerCase().replace(/[^a-z0-9\s]/g, "")
    );
    return `https://source.unsplash.com/600x400/?${searchTerm},food`;
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoading(false);
  };

  const handleImageLoad = () => {
    setImageLoading(false);
  };

  return (
    <Card className="overflow-hidden py-0">
      <div className="relative">
        {imageLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-muted z-10">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        )}

        {foodItem.image && !imageError ? (
          <img
            src={foodItem.image}
            alt={foodItem.name}
            className={`w-full h-64 object-cover ${
              imageLoading ? "opacity-0" : "opacity-100"
            }`}
            onError={handleImageError}
            onLoad={handleImageLoad}
          />
        ) : (
          <img
            src={getUnsplashImageUrl(foodItem.name)}
            alt={foodItem.name}
            className={`w-full h-64 object-cover ${
              imageLoading ? "opacity-0" : "opacity-100"
            }`}
            onError={handleImageError}
            onLoad={handleImageLoad}
          />
        )}

        {imageError && !imageLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-muted">
            <div className="text-center">
              <span className="text-muted-foreground text-6xl mb-4 block">
                🍕
              </span>
              <p className="text-muted-foreground">Image unavailable</p>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default ProductImage;

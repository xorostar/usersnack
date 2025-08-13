import { useState, useEffect } from "react";
import type { FoodItem } from "../types";
import { apiService } from "../services/api";
import { ApiError } from "../sdk";

export const useFoodItems = () => {
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFoodItems = async () => {
      try {
        setLoading(true);
        const items = await apiService.getFoodItems();
        setFoodItems(items);
      } catch (err: unknown) {
        console.error("Error fetching food items:", err);

        if (err instanceof ApiError) {
          if (err.status === 404) {
            setError("No food items found. Please try again later.");
          } else {
            setError(
              err.message ||
                "Failed to load food items. Please try again later."
            );
          }
        } else {
          setError("Failed to load food items. Please try again later.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchFoodItems();
  }, []);

  const refetch = () => {
    window.location.reload();
  };

  return {
    foodItems,
    loading,
    error,
    refetch,
  };
};

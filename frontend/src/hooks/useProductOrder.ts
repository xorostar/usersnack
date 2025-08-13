import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import type { FoodItem, Extra, CustomerInfo } from "../types";
import { apiService } from "../services/api";
import { Currency, ApiError } from "../sdk";

interface UseProductOrderProps {
  productId: string | undefined;
}

export const useProductOrder = ({ productId }: UseProductOrderProps) => {
  const navigate = useNavigate();

  const [foodItem, setFoodItem] = useState<FoodItem | null>(null);
  const [extras, setExtras] = useState<Extra[]>([]);
  const [selectedExtras, setSelectedExtras] = useState<Extra[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [orderLoading, setOrderLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch product data and extras
  useEffect(() => {
    const fetchData = async () => {
      if (!productId) return;

      try {
        setLoading(true);
        const [foodItemData, extrasData] = await Promise.all([
          apiService.getFoodItem(productId),
          apiService.getExtras(),
        ]);

        setFoodItem(foodItemData);
        setExtras(extrasData);
      } catch (err: unknown) {
        console.error("Error fetching product data:", err);

        const defaultMsg =
          "Failed to load product information. Please try again later.";
        let message = defaultMsg;

        if (err instanceof ApiError) {
          if (err.status === 404) {
            navigate("/404");
            return;
          }
          if (err.message) message = err.message;
        }

        setError(message);
        toast.error(message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [productId, navigate]);

  // Calculate unit price (base price + extras)
  const calculateUnitPrice = (): number => {
    if (!foodItem) return 0;

    const basePrice = parseFloat(foodItem.base_price);
    const extrasPrice = selectedExtras.reduce(
      (sum, extra) => sum + parseFloat(extra.price),
      0
    );
    return basePrice + extrasPrice;
  };

  // Calculate total price (unit price * quantity)
  const calculateTotalPrice = (): number => {
    return calculateUnitPrice() * quantity;
  };

  // Handle order placement
  const handlePlaceOrder = async (customerInfo: CustomerInfo) => {
    if (!foodItem) return;

    try {
      setOrderLoading(true);

      const order = {
        items: [
          {
            food_item_id: foodItem.id,
            quantity,
            extra_ids: selectedExtras.map((extra) => extra.id),
          },
        ],
        currency: Currency.EUR,
        customer_name: customerInfo.name,
        customer_address: customerInfo.address,
      };

      const orderResponse = await apiService.createOrder(order);

      // Save order to localStorage
      try {
        const existingOrders = JSON.parse(
          localStorage.getItem("orders") || "[]"
        );
        const updatedOrders = [orderResponse, ...existingOrders];
        localStorage.setItem("orders", JSON.stringify(updatedOrders));
      } catch (error) {
        console.error("Error saving order to localStorage:", error);
      }

      // Show success message and redirect
      toast.success(
        `Order placed successfully! Thank you for your order, ${customerInfo.name}.`
      );
      navigate("/");
    } catch (err: unknown) {
      console.error("Error placing order:", err);

      if (err instanceof ApiError) {
        toast.error(err.message || "Failed to place order. Please try again.");
      } else {
        toast.error("Failed to place order. Please try again.");
      }
    } finally {
      setOrderLoading(false);
    }
  };

  return {
    // State
    foodItem,
    extras,
    selectedExtras,
    quantity,
    loading,
    orderLoading,
    error,

    // Actions
    setSelectedExtras,
    setQuantity,
    handlePlaceOrder,

    // Computed values
    calculateUnitPrice,
    calculateTotalPrice,
  };
};

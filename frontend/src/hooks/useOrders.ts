import { useState, useEffect } from "react";
import type { OrderResponse } from "../types";

export const useOrders = () => {
  const [orders, setOrders] = useState<OrderResponse[]>([]);

  useEffect(() => {
    try {
      const storedOrders = JSON.parse(localStorage.getItem("orders") || "[]");
      setOrders(storedOrders);
    } catch (error) {
      console.error("Error loading orders:", error);
      setOrders([]);
    }
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "created":
        return "bg-blue-100 text-blue-800";
      case "confirmed":
        return "bg-green-100 text-green-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return {
    orders,
    formatDate,
    getStatusColor,
  };
};

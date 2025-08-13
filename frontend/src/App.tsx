import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import HomePage from "./pages/HomePage";
import ProductOrderPage from "./pages/ProductOrderPage";
import OrdersPage from "./pages/OrdersPage";
import NotFoundPage from "./pages/NotFoundPage";
import Header from "./components/Header";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/product/:id" element={<ProductOrderPage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/404" element={<NotFoundPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </div>
      <Toaster />
    </Router>
  );
}

export default App;
